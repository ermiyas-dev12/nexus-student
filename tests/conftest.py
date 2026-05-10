import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from run import app as flask_app
from database.models import db, User, Post
from werkzeug.security import generate_password_hash


@pytest.fixture
def app():
    """Create a test Flask app with an in-memory SQLite database."""
    flask_app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SECRET_KEY': 'test-secret-key',
        'WTF_CSRF_ENABLED': False,
        'MAIL_SUPPRESS_SEND': True,
        'LOGIN_DISABLED': False,
    })

    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Return a test client."""
    return app.test_client()


@pytest.fixture
def regular_user(app):
    """Create and return a regular (non-admin) user id."""
    with app.app_context():
        user = User(
            username='testuser',
            email='test@example.com',
            password=generate_password_hash('password123'),
            is_verified=True,
            is_admin=False
        )
        db.session.add(user)
        db.session.commit()
        return user.id


@pytest.fixture
def admin_user(app):
    """Create and return an admin user id."""
    with app.app_context():
        user = User(
            username='adminuser',
            email='admin@example.com',
            password=generate_password_hash('adminpass123'),
            is_verified=True,
            is_admin=True
        )
        db.session.add(user)
        db.session.commit()
        return user.id


@pytest.fixture
def sample_post(app):
    """Create and return a sample post id."""
    with app.app_context():
        post = Post(title='Test Post', body='Test body content', author='testuser')
        db.session.add(post)
        db.session.commit()
        return post.id


@pytest.fixture
def login(client):
    """Fixture that returns a login helper function."""
    def _login(email, password):
        return client.post('/login', data={
            'email': email,
            'password': password
        }, follow_redirects=True)
    return _login