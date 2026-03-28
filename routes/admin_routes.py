from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from database.models import db, User, Post
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required.', 'error')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

def register_admin_routes(app):

    # ---------- ADMIN DASHBOARD ----------
    @app.route('/admin')
    @login_required
    @admin_required
    def admin_dashboard():
        users = User.query.order_by(User.created_at.desc()).all()
        posts = Post.query.order_by(Post.created_at.desc()).all()
        total_users = User.query.count()
        verified_users = User.query.filter_by(is_verified=True).count()
        total_posts = Post.query.count()
        return render_template('admin.html',
                               users=users,
                               posts=posts,
                               total_users=total_users,
                               verified_users=verified_users,
                               total_posts=total_posts)

    # ---------- DELETE USER ----------
    @app.route('/admin/delete-user/<int:user_id>', methods=['POST'])
    @login_required
    @admin_required
    def delete_user(user_id):
        user = User.query.get_or_404(user_id)
        if user.is_admin:
            flash('Cannot delete admin users.', 'error')
            return redirect(url_for('admin_dashboard'))
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully.', 'success')
        return redirect(url_for('admin_dashboard'))

    # ---------- TOGGLE ADMIN ----------
    @app.route('/admin/toggle-admin/<int:user_id>', methods=['POST'])
    @login_required
    @admin_required
    def toggle_admin(user_id):
        user = User.query.get_or_404(user_id)
        user.is_admin = not user.is_admin
        db.session.commit()
        flash(f'Admin status updated for {user.username}.', 'success')
        return redirect(url_for('admin_dashboard'))

    # ---------- DELETE POST ----------
    @app.route('/admin/delete-post/<int:post_id>', methods=['POST'])
    @login_required
    @admin_required
    def delete_post(post_id):
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully.', 'success')
        return redirect(url_for('admin_dashboard'))