import resend
from app.config import settings

if settings.RESEND_API_KEY:
    resend.api_key = settings.RESEND_API_KEY

def send_verification_email(to_email: str, username: str, token: str):
    if not settings.RESEND_API_KEY:
        print(f"[DEV] Verify: {settings.FRONTEND_URL}/verify-email?token={token}")
        return
    html = f"""
    <h2>Welcome {username}!</h2>
    <p>Verify your email:</p>
    <a href="{settings.FRONTEND_URL}/verify-email?token={token}">Verify Email</a>
    <p>Expires in {settings.VERIFICATION_TOKEN_EXPIRE_HOURS}h.</p>
    """
    resend.Emails.send({
        "from": f"{settings.EMAIL_FROM_NAME} <{settings.EMAIL_FROM}>",
        "to": to_email,
        "subject": "Verify your email",
        "html": html,
    })

def send_password_reset_email(to_email: str, token: str):
    if not settings.RESEND_API_KEY:
        print(f"[DEV] Reset: {settings.FRONTEND_URL}/reset-password?token={token}")
        return
    html = f"""
    <h2>Password Reset</h2>
    <a href="{settings.FRONTEND_URL}/reset-password?token={token}">Reset Password</a>
    <p>Expires in {settings.PASSWORD_RESET_TOKEN_EXPIRE_HOURS}h.</p>
    """
    resend.Emails.send({
        "from": f"{settings.EMAIL_FROM_NAME} <{settings.EMAIL_FROM}>",
        "to": to_email,
        "subject": "Reset your password",
        "html": html,
    })
