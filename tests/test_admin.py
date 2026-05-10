from database.models import db, User, Post


class TestAdminRoutes:

    def test_admin_dashboard_requires_login(self, client):
        response = client.get('/admin', follow_redirects=True)
        assert response.status_code == 200
        assert b'log in' in response.data.lower()

    def test_admin_dashboard_blocked_for_regular_user(self, client, login, regular_user):
        login('test@example.com', 'password123')
        response = client.get('/admin', follow_redirects=True)
        # admin_required redirects to home — verify user is NOT on the admin page
        assert response.status_code == 200
        assert b'admin' not in response.request.path.encode()

    def test_admin_dashboard_loads_for_admin(self, client, login, admin_user):
        login('admin@example.com', 'adminpass123')
        response = client.get('/admin')
        assert response.status_code == 200

    def test_delete_user_as_admin(self, client, login, admin_user, regular_user, app):
        login('admin@example.com', 'adminpass123')
        response = client.post(f'/admin/delete-user/{regular_user}', follow_redirects=True)
        assert response.status_code == 200
        with app.app_context():
            user = User.query.filter_by(id=regular_user).first()
            assert user is None

    def test_cannot_delete_admin_user(self, client, login, admin_user, app):
        login('admin@example.com', 'adminpass123')
        response = client.post(f'/admin/delete-user/{admin_user}', follow_redirects=True)
        assert response.status_code == 200
        with app.app_context():
            user = User.query.filter_by(id=admin_user).first()
            assert user is not None

    def test_toggle_admin_status(self, client, login, admin_user, regular_user, app):
        login('admin@example.com', 'adminpass123')
        client.post(f'/admin/toggle-admin/{regular_user}')
        with app.app_context():
            user = User.query.filter_by(id=regular_user).first()
            assert user.is_admin is True

    def test_delete_post_as_admin(self, client, login, admin_user, sample_post, app):
        login('admin@example.com', 'adminpass123')
        response = client.post(f'/admin/delete-post/{sample_post}', follow_redirects=True)
        assert response.status_code == 200
        with app.app_context():
            post = Post.query.filter_by(id=sample_post).first()
            assert post is None

    def test_delete_user_as_regular_user_blocked(self, client, login, regular_user, admin_user):
        login('test@example.com', 'password123')
        response = client.post(f'/admin/delete-user/{admin_user}', follow_redirects=True)
        # Regular user gets redirected away from admin — verify they land on a non-admin page
        assert response.status_code == 200
        assert b'/admin' not in response.request.path.encode()
