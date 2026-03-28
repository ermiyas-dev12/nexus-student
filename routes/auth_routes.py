import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database.models import db, User
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask_mail import Message

SECRET_KEY = os.getenv('SECRET_KEY', 'nexus-secret-key-2024')
s = URLSafeTimedSerializer(SECRET_KEY)

# ---------- EMAIL FUNCTIONS (inline) ----------
def send_verification_email(mail, user, s):
    token = s.dumps(user.email, salt='email-verify')
    link = f"http://127.0.0.1:5000/verify/{token}"
    msg = Message(
        subject='Verify your NexusStudent email',
        recipients=[user.email]
    )
    msg.body = f"Hi {user.username},\n\nVerify your email:\n{link}\n\nExpires in 1 hour.\n\n— NexusStudent Team"
    mail.send(msg)

def send_reset_email(mail, user, s):
    token = s.dumps(user.email, salt='password-reset')
    link = f"http://127.0.0.1:5000/reset-password/{token}"
    msg = Message(
        subject='Reset your NexusStudent password',
        recipients=[user.email]
    )
    msg.body = f"Hi {user.username},\n\nReset your password:\n{link}\n\nExpires in 1 hour.\n\n— NexusStudent Team"
    mail.send(msg)

# ---------- ROUTES ----------
def register_auth_routes(app, mail):

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '').strip()
            confirm = request.form.get('confirm_password', '').strip()
            if not username or not email or not password:
                flash('All fields are required.', 'error')
                return render_template('auth/register.html')
            if password != confirm:
                flash('Passwords do not match.', 'error')
                return render_template('auth/register.html')
            if len(password) < 6:
                flash('Password must be at least 6 characters.', 'error')
                return render_template('auth/register.html')
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Email already registered.', 'error')
                return render_template('auth/register.html')
            hashed_password = generate_password_hash(password)
            user = User(username=username, email=email, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            try:
                send_verification_email(mail, user, s)
                flash('Account created! Please check your email to verify.', 'success')
            except Exception as e:
                print(f"[Email Error] {e}")
                flash('Account created! Email verification unavailable.', 'warning')
            return redirect(url_for('login'))
        return render_template('auth/register.html')

    @app.route('/verify/<token>')
    def verify_email(token):
        try:
            email = s.loads(token, salt='email-verify', max_age=3600)
            user = User.query.filter_by(email=email).first()
            if user:
                user.is_verified = True
                db.session.commit()
                flash('Email verified! You can now log in.', 'success')
            return redirect(url_for('login'))
        except SignatureExpired:
            flash('Verification link expired.', 'error')
            return redirect(url_for('login'))
        except BadSignature:
            flash('Invalid verification link.', 'error')
            return redirect(url_for('login'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        if request.method == 'POST':
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '').strip()
            remember = request.form.get('remember_me') == 'on'
            user = User.query.filter_by(email=email).first()
            if not user or not check_password_hash(user.password, password):
                flash('Invalid email or password.', 'error')
                return render_template('auth/login.html')
            login_user(user, remember=remember)
            flash(f'Welcome back, {user.username}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        return render_template('auth/login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Logged out successfully.', 'success')
        return redirect(url_for('home'))

    @app.route('/forgot-password', methods=['GET', 'POST'])
    def forgot_password():
        if request.method == 'POST':
            email = request.form.get('email', '').strip()
            user = User.query.filter_by(email=email).first()
            if user:
                try:
                    send_reset_email(mail, user, s)
                    flash('Password reset link sent to your email.', 'success')
                except Exception as e:
                    print(f"[Email Error] {e}")
                    flash('Could not send email. Try again later.', 'error')
            else:
                flash('No account found with that email.', 'error')
        return render_template('auth/forgot.html')

    @app.route('/reset-password/<token>', methods=['GET', 'POST'])
    def reset_password(token):
        try:
            email = s.loads(token, salt='password-reset', max_age=3600)
        except (SignatureExpired, BadSignature):
            flash('Reset link is invalid or expired.', 'error')
            return redirect(url_for('forgot_password'))
        user = User.query.filter_by(email=email).first()
        if request.method == 'POST':
            password = request.form.get('password', '').strip()
            confirm = request.form.get('confirm_password', '').strip()
            if password != confirm:
                flash('Passwords do not match.', 'error')
                return render_template('auth/reset.html', token=token)
            if len(password) < 6:
                flash('Password must be at least 6 characters.', 'error')
                return render_template('auth/reset.html', token=token)
            user.password = generate_password_hash(password)
            db.session.commit()
            flash('Password reset successful! Please log in.', 'success')
            return redirect(url_for('login'))
        return render_template('auth/reset.html', token=token)