import pytest
from database.models import db, User, Post, Like, ChatHistory
from werkzeug.security import generate_password_hash


class TestModels:

    def test_user_creation(self, app):
        with app.app_context():
            user = User(
                username='alice',
                email='alice@example.com',
                password=generate_password_hash('secret')
            )
            db.session.add(user)
            db.session.commit()
            fetched = User.query.filter_by(email='alice@example.com').first()
            assert fetched is not None
            assert fetched.username == 'alice'
            assert fetched.is_admin is False
            assert fetched.is_verified is False

    def test_user_defaults(self, app):
        with app.app_context():
            user = User(
                username='bob',
                email='bob@example.com',
                password='hashed'
            )
            db.session.add(user)
            db.session.commit()
            assert user.avatar == 'default.png'
            assert user.is_admin is False
            assert user.is_verified is False

    def test_post_creation(self, app):
        with app.app_context():
            post = Post(title='Hello World', body='Some content', author='alice')
            db.session.add(post)
            db.session.commit()
            fetched = Post.query.filter_by(title='Hello World').first()
            assert fetched is not None
            assert fetched.body == 'Some content'
            assert fetched.author == 'alice'

    def test_post_default_author(self, app):
        with app.app_context():
            post = Post(title='No Author Post')
            db.session.add(post)
            db.session.commit()
            assert post.author == 'Anonymous'

    def test_like_creation_and_unique_constraint(self, app):
        with app.app_context():
            user = User(username='liker', email='liker@example.com', password='pw')
            post = Post(title='Liked Post', body='body')
            db.session.add_all([user, post])
            db.session.commit()

            like = Like(user_id=user.id, post_id=post.id)
            db.session.add(like)
            db.session.commit()
            assert Like.query.count() == 1

            from sqlalchemy.exc import IntegrityError
            with pytest.raises(IntegrityError):
                duplicate = Like(user_id=user.id, post_id=post.id)
                db.session.add(duplicate)
                db.session.commit()

    def test_chat_history_creation(self, app):
        with app.app_context():
            chat = ChatHistory(
                session_id='sess-abc',
                message='Hello',
                response='Hi there!'
            )
            db.session.add(chat)
            db.session.commit()
            fetched = ChatHistory.query.first()
            assert fetched.message == 'Hello'
            assert fetched.response == 'Hi there!'

    def test_post_cascade_delete_likes(self, app):
        with app.app_context():
            user = User(username='u1', email='u1@example.com', password='pw')
            post = Post(title='Cascade Test', body='body')
            db.session.add_all([user, post])
            db.session.commit()

            like = Like(user_id=user.id, post_id=post.id)
            db.session.add(like)
            db.session.commit()
            assert Like.query.count() == 1

            db.session.delete(post)
            db.session.commit()
            assert Like.query.count() == 0
