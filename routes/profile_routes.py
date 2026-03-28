from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from database.models import db
from PIL import Image
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def register_profile_routes(app):

    # ---------- PROFILE ----------
    @app.route('/profile')
    @login_required
    def profile():
        return render_template('profile.html')

    # ---------- EDIT PROFILE ----------
    @app.route('/profile/edit', methods=['POST'])
    @login_required
    def edit_profile():
        username = request.form.get('username', '').strip()
        if username:
            current_user.username = username
            db.session.commit()
            flash('Profile updated successfully.', 'success')
        return redirect(url_for('profile'))

    # ---------- UPLOAD AVATAR ----------
    @app.route('/profile/avatar', methods=['POST'])
    @login_required
    def upload_avatar():
        if 'avatar' not in request.files:
            flash('No file selected.', 'error')
            return redirect(url_for('profile'))

        file = request.files['avatar']

        if file.filename == '':
            flash('No file selected.', 'error')
            return redirect(url_for('profile'))

        if file and allowed_file(file.filename):
            filename = secure_filename(f"user_{current_user.id}.png")
            upload_folder = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)
            filepath = os.path.join(upload_folder, filename)

            # Resize avatar to 200x200
            img = Image.open(file)
            img = img.resize((200, 200))
            img.save(filepath)

            current_user.avatar = filename
            db.session.commit()
            flash('Avatar updated successfully.', 'success')
        else:
            flash('Invalid file type. Use PNG, JPG, or GIF.', 'error')

        return redirect(url_for('profile'))

    # ---------- CHANGE PASSWORD ----------
    @app.route('/profile/change-password', methods=['POST'])
    @login_required
    def change_password():
        from werkzeug.security import check_password_hash
        old = request.form.get('old_password', '').strip()
        new = request.form.get('new_password', '').strip()
        confirm = request.form.get('confirm_password', '').strip()

        if not check_password_hash(current_user.password, old):
            flash('Current password is incorrect.', 'error')
            return redirect(url_for('profile'))

        if new != confirm:
            flash('New passwords do not match.', 'error')
            return redirect(url_for('profile'))

        if len(new) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return redirect(url_for('profile'))

        current_user.password = generate_password_hash(new)
        db.session.commit()
        flash('Password changed successfully.', 'success')
        return redirect(url_for('profile'))