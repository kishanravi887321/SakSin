import random
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings


class BaseOtpEmailSender:
    def __init__(self, email):
        self.email = email
        self.api_client = self._setup_brevo_client()
        self.api_instance = sib_api_v3_sdk.TransactionalEmailsApi(self.api_client)

    def _setup_brevo_client(self):
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = settings.BREVO_API_KEY_EMAIL
        return sib_api_v3_sdk.ApiClient(configuration)

    def generate_otp(self):
        return str(random.randint(100000, 999999))

    def send_email(self, subject, text_content, html_content=None):
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            sender={"name": "Sākṣin", "email": settings.FORWARDING_EMAIL},
            to=[{"email": self.email}],
            subject=subject,
            text_content=text_content,
            html_content=html_content  # ✅ HTML email body (optional)
        )

        try:
            self.api_instance.send_transac_email(send_smtp_email)
        except ApiException as e:
            print(f"[Brevo] Failed to send email: {e}")
            raise e
