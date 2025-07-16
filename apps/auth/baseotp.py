import random
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings
from django.core.cache import cache  


# KEY: otp:register:kishan@gmail.com
# VALUE: 841392
# TTL: 300 seconds





class BaseOtpEmailSender:
    def __init__(self, email, purpose):
        """
        purpose: 'register', 'login', 'forget', 'update'
        """
        self.email = email
        self.purpose = purpose
        self.key = f"otp:{purpose}:{email}"
        self.api_client = self._setup_brevo_client()
        self.api_instance = sib_api_v3_sdk.TransactionalEmailsApi(self.api_client)

    def _setup_brevo_client(self):
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = settings.BREVO_API_KEY_EMAIL
        return sib_api_v3_sdk.ApiClient(configuration)

    def generate_otp(self):
        """
        Generates and stores a 6-digit OTP in Redis with 5-minute TTL.
        """
        otp = str(random.randint(100000, 999999))
        cache.set(self.key, otp, timeout=300)  # 🧠5 min TTL

        print("the otp genrated is ",cache.get(self.key)) 
        print('se',self.key) # Debugging line to check OTP storage
        return otp

    def validate_otp(self, input_otp):
        """
        Validates and clears OTP if matched.
        """
        stored_otp = cache.get(self.key)
        if stored_otp == input_otp:
            cache.delete(self.key)
            return True
        return False

    def invalidate_otp(self):
        """
        Manually clears OTP (e.g., after multiple failures).
        """
        cache.delete(self.key)

    def send_email(self, subject, text_content, html_content=None):
        """
        Sends the email using Brevo (SMTP).
        """
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            sender={"name": "Sākṣin", "email": settings.FORWARDING_EMAIL},
            to=[{"email": self.email}],
            subject=subject,
            text_content=text_content,
            html_content=html_content
        )

        try:
            self.api_instance.send_transac_email(send_smtp_email)
        except ApiException as e:
            print(f"[Brevo] Failed to send email: {e}")
            raise e


print(cache.keys('*'))