from protonmail import ProtonMail

from app.tasks import celery_app
from app.core.config import settings

@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_confirmation_email(self, to_email: str, token: str):
    proton = ProtonMail()
    proton.login(settings.email_user, settings.email_password)
    
    subject = "Confirm your registration"
    link = f"{settings.frontend_url}/api/auth/confirm/{token}"
    body = f"Hello!<br>To confirm your registration, follow the link: {link}"

    message = proton.create_message(
        recipients=[to_email],
        subject=subject,
        body=body,
    )

    try:
        proton.send_message(message)
    except Exception as exc:
        raise self.retry(exc=exc)