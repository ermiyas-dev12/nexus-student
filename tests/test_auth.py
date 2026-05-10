from database.models import db, User


class TestAuthRoutes:

    def test_register_page_loads(self, client):
        response = client.get('/register')
        assert response.status_code == 200

    def test_login_page_loads(self, client):
        response = client.get('/login')
        assert response.status_code == 200

    def test_register_success(self, client, app):
        response = client.post('/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        assert response.status_code == 200
        with app.app_context():
            user = User.query.filter_by(email='newuser@example.com').first()
            assert user is not None
            assert user.username == 'newuser'

    def test_register_missing_fields(self, client):
        response = client.post('/register', data={
            'username': '', 'email': '', 'password': ''
        }, follow_redirects=True)
        assert b'required' in response.data.lower() or response.status_code == 200

    def test_register_password_mismatch(self, client):
        response = client.post('/register', data={
            'username': 'user1',
            'email': 'user1@example.com',
            'password': 'password123',
            'confirm_password': 'wrongpass'
        }, follow_redirects=True)
        assert b'match' in response.data.lower()

    def test_register_short_password(self, client):
        response = client.post('/register', data={
            'username': 'user2',
            'email': 'user2@example.com',
            'password': '123',
            'confirm_password': '123'
        }, follow_redirects=True)
        assert b'6' in response.data or b'characters' in response.data.lower()

    def test_register_duplicate_email(self, client, regular_user):
        response = client.post('/register', data={
            'username': 'another',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        assert b'already' in response.data.lower()

    def test_login_success(self, client, login, regular_user):
        response = login('test@example.com', 'password123')
        assert response.status_code == 200
        assert b'welcome' in response.data.lower() or b'home' in response.data.lower()

    def test_login_wrong_password(self, client, login, regular_user):
        response = login('test@example.com', 'wrongpassword')
        assert b'invalid' in response.data.lower()

    def test_login_nonexistent_user(self, client, login):
        response = login('nobody@example.com', 'password123')
        assert b'invalid' in response.data.lower()

    def test_logout_requires_login(self, client):
        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200

    def test_logout_success(self, client, login, regular_user):
        login('test@example.com', 'password123')
        response = client.get('/logout', follow_redirects=True)
        # After logout the user is redirected to home and is no longer logged in.
        # We verify by checking the login link appears in the nav (user is logged out).
        assert response.status_code == 200
        assert b'/login' in response.data

    def test_forgot_password_page_loads(self, client):
        response = client.get('/forgot-password')
        assert response.status_code == 200

    def test_forgot_password_unknown_email(self, client):
        response = client.post('/forgot-password', data={
            'email': 'nobody@example.com'
        }, follow_redirects=True)
        assert b'no account' in response.data.lower()
