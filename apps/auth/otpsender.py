from .baseotp import BaseOtpEmailSender

class LoginOtpSender(BaseOtpEmailSender):

    def send(self):
        otp=self.generate_otp()
        subject = "SakSin Login OTP"
        text_content = f"Your OTP for SakSin login is: {otp}"

        self.send_email(subject, text_content)
        return otp
    

class forgetPasswordOtpSender(BaseOtpEmailSender):

    def send(self):
        otp = self.generate_otp()
        subject = "SakSin Password Reset OTP"
        text_content = f"Your OTP for SakSin password reset is: {otp}"

        self.send_email(subject, text_content)
        return otp

class RegistrationOtpSender(BaseOtpEmailSender):

    def send(self):
        otp = self.generate_otp()
        subject = "SakSin Registration OTP"
        text_content = f"Your OTP for SakSin registration is: {otp}"

        self.send_email(subject, text_content)
        return otp