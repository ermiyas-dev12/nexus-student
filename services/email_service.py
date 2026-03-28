from flask_mail import Message

def send_verification_email(mail, user, s):
    token = s.dumps(user.email, salt='email-verify')
    link = f"http://127.0.0.1:5000/verify/{token}"

    msg = Message(
        subject='Verify your NexusStudent email',
        recipients=[user.email]
    )
    msg.body = f"""
Hi {user.username},

Please verify your email by clicking the link below:

{link}

This link expires in 1 hour.

— NexusStudent Team
"""
    mail.send(msg)


def send_reset_email(mail, user, s):
    token = s.dumps(user.email, salt='password-reset')
    link = f"http://127.0.0.1:5000/reset-password/{token}"

    msg = Message(
        subject='Reset your NexusStudent password',
        recipients=[user.email]
    )
    msg.body = f"""
Hi {user.username},

Click the link below to reset your password:

{link}

This link expires in 1 hour.

If you did not request this, ignore this email.

— NexusStudent Team
"""
    mail.send(msg)