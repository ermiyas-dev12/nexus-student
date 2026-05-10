from unittest.mock import MagicMock
from itsdangerous import URLSafeTimedSerializer
from database.models import db, User


class TestEmailService:

    def test_send_verification_email(self, app):
        """Verification email is sent without errors."""
        from services.email_service import send_verification_email
        with app.app_context():
            user = User(username='emailuser', email='emailuser@example.com', password='hashed')
            db.session.add(user)
            db.session.commit()

            s = URLSafeTimedSerializer('test-secret-key')
            mock_mail = MagicMock()
            send_verification_email(mock_mail, user, s)
            mock_mail.send.assert_called_once()

    def test_send_verification_email_content(self, app):
        """Verification email contains correct subject, recipient and body."""
        from services.email_service import send_verification_email
        with app.app_context():
            user = User(username='verifyuser', email='verifyuser@example.com', password='hashed')
            db.session.add(user)
            db.session.commit()

            s = URLSafeTimedSerializer('test-secret-key')
            mock_mail = MagicMock()
            send_verification_email(mock_mail, user, s)

            msg = mock_mail.send.call_args[0][0]
            assert 'verifyuser' in msg.body
            assert '/verify/' in msg.body
            assert msg.subject == 'Verify your NexusStudent email'
            assert 'verifyuser@example.com' in msg.recipients

    def test_send_reset_email(self, app):
        """Reset email is sent without errors."""
        from services.email_service import send_reset_email
        with app.app_context():
            user = User(username='resetuser', email='resetuser@example.com', password='hashed')
            db.session.add(user)
            db.session.commit()

            s = URLSafeTimedSerializer('test-secret-key')
            mock_mail = MagicMock()
            send_reset_email(mock_mail, user, s)
            mock_mail.send.assert_called_once()

    def test_send_reset_email_content(self, app):
        """Reset email contains correct subject, recipient and body."""
        from services.email_service import send_reset_email
        with app.app_context():
            user = User(username='resetuser2', email='resetuser2@example.com', password='hashed')
            db.session.add(user)
            db.session.commit()

            s = URLSafeTimedSerializer('test-secret-key')
            mock_mail = MagicMock()
            send_reset_email(mock_mail, user, s)

            msg = mock_mail.send.call_args[0][0]
            assert 'resetuser2' in msg.body
            assert '/reset-password/' in msg.body
            assert msg.subject == 'Reset your NexusStudent password'
            assert 'resetuser2@example.com' in msg.recipients

    def test_verification_token_is_unique_per_call(self, app):
        """Each call generates a different token/link."""
        from services.email_service import send_verification_email
        with app.app_context():
            user = User(username='tokenuser', email='tokenuser@example.com', password='hashed')
            db.session.add(user)
            db.session.commit()

            s = URLSafeTimedSerializer('test-secret-key')
            mock_mail = MagicMock()

            send_verification_email(mock_mail, user, s)
            msg1 = mock_mail.send.call_args[0][0].body

            send_verification_email(mock_mail, user, s)
            msg2 = mock_mail.send.call_args[0][0].body

            assert msg1 != msg2
