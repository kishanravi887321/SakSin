from .baseotp import BaseOtpEmailSender

class LoginOtpSender(BaseOtpEmailSender):
    def __init__(self,email):
        super().__init__(email,purpose="login")


    def send(self):
        otp=self.generate_otp()
        subject = "🔐 Sākṣin - Login Authentication Required"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Login Authentication</title>
            <style>
                @keyframes slideDown {{
                    from {{ transform: translateY(-20px); opacity: 0; }}
                    to {{ transform: translateY(0); opacity: 1; }}
                }}
                @keyframes subtlePulse {{
                    0%, 100% {{ transform: scale(1); }}
                    50% {{ transform: scale(1.02); }}
                }}
                .container {{
                    max-width: 650px;
                    margin: 0 auto;
                    background: #f5f7fa;
                    font-family: 'Arial', sans-serif;
                    padding: 0;
                }}
                .header {{
                    background: linear-gradient(135deg, #1a365d 0%, #2d5aa0 100%);
                    padding: 40px 30px;
                    text-align: center;
                    color: white;
                }}
                .logo {{
                    font-size: 28px;
                    font-weight: 600;
                    margin-bottom: 8px;
                    letter-spacing: 1px;
                }}
                .subtitle {{
                    font-size: 16px;
                    opacity: 0.9;
                    font-weight: 300;
                }}
                .content {{
                    background: white;
                    padding: 50px 40px;
                    animation: slideDown 0.6s ease-out;
                }}
                .security-badge {{
                    width: 60px;
                    height: 60px;
                    background: linear-gradient(135deg, #1a365d, #2d5aa0);
                    border-radius: 50%;
                    margin: 0 auto 30px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 24px;
                    color: white;
                    animation: subtlePulse 3s infinite;
                }}
                .title {{
                    color: #1a365d;
                    font-size: 24px;
                    font-weight: 600;
                    margin: 0 0 20px 0;
                    text-align: center;
                }}
                .description {{
                    color: #4a5568;
                    font-size: 16px;
                    line-height: 1.6;
                    text-align: center;
                    margin-bottom: 35px;
                }}
                .otp-section {{
                    background: linear-gradient(135deg, #edf2f7 0%, #e2e8f0 100%);
                    border: 2px solid #cbd5e0;
                    border-radius: 12px;
                    padding: 30px;
                    margin: 30px 0;
                    text-align: center;
                }}
                .otp-label {{
                    color: #2d3748;
                    font-size: 14px;
                    font-weight: 500;
                    margin-bottom: 15px;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }}
                .otp {{
                    font-size: 32px;
                    font-weight: 700;
                    color: #1a365d;
                    letter-spacing: 6px;
                    font-family: 'Courier New', monospace;
                    margin: 0;
                }}
                .security-notice {{
                    background: #fef5e7;
                    border-left: 4px solid #ed8936;
                    border-radius: 6px;
                    padding: 20px;
                    margin: 30px 0;
                }}
                .notice-title {{
                    color: #c05621;
                    font-weight: 600;
                    margin-bottom: 8px;
                    font-size: 14px;
                }}
                .notice-text {{
                    color: #744210;
                    font-size: 14px;
                    margin: 0;
                }}
                .footer {{
                    background: #2d3748;
                    color: #a0aec0;
                    padding: 30px;
                    text-align: center;
                    font-size: 14px;
                }}
                .footer-link {{
                    color: #63b3ed;
                    text-decoration: none;
                }}
                .divider {{
                    height: 1px;
                    background: #e2e8f0;
                    margin: 30px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="logo">🔐 Sākṣin</div>
                    <div class="subtitle">Secure Authentication Platform</div>
                </div>
                <div class="content">
                    <div class="security-badge">�</div>
                    <h1 class="title">Authentication Required</h1>
                    <p class="description">
                        A login attempt has been detected for your account. Please use the verification code below to complete your authentication.
                    </p>
                    
                    <div class="otp-section">
                        <div class="otp-label">Verification Code</div>
                        <div class="otp">{otp}</div>
                    </div>
                    
                    <div class="security-notice">
                        <div class="notice-title">🛡️ Security Information</div>
                        <p class="notice-text">This code expires in 10 minutes and can only be used once. Never share this code with anyone.</p>
                    </div>
                    
                    <div class="divider"></div>
                    
                    <p style="color: #718096; font-size: 14px; text-align: center; margin: 0;">
                        If you did not initiate this login request, please ignore this email and consider changing your password.
                    </p>
                </div>
                <div class="footer">
                    <p>© 2025 Sākṣin. All rights reserved.</p>
                    <p>Support: <a href="mailto:support@saksin.ai" class="footer-link">support@saksin.ai</a></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"Sākṣin Authentication Code: {otp}\n\nThis verification code expires in 10 minutes. Do not share it with anyone.\n\nIf you did not request this login, please ignore this email."

        self.send_email(subject, text_content, html_content=html_content)
        return otp
    

class forgetPasswordOtpSender(BaseOtpEmailSender):
    def __init__(self,email):
        super().__init__(email,purpose="forget")


    def send(self):
        otp = self.generate_otp()
        subject = "🔑 Sākṣin - Password Reset Verification"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Password Reset</title>
            <style>
                @keyframes slideDown {{
                    from {{ transform: translateY(-20px); opacity: 0; }}
                    to {{ transform: translateY(0); opacity: 1; }}
                }}
                @keyframes subtlePulse {{
                    0%, 100% {{ transform: scale(1); }}
                    50% {{ transform: scale(1.02); }}
                }}
                .container {{
                    max-width: 650px;
                    margin: 0 auto;
                    background: #f5f7fa;
                    font-family: 'Arial', sans-serif;
                    padding: 0;
                }}
                .header {{
                    background: linear-gradient(135deg, #c53030 0%, #e53e3e 100%);
                    padding: 40px 30px;
                    text-align: center;
                    color: white;
                }}
                .logo {{
                    font-size: 28px;
                    font-weight: 600;
                    margin-bottom: 8px;
                    letter-spacing: 1px;
                }}
                .subtitle {{
                    font-size: 16px;
                    opacity: 0.9;
                    font-weight: 300;
                }}
                .content {{
                    background: white;
                    padding: 50px 40px;
                    animation: slideDown 0.6s ease-out;
                }}
                .reset-badge {{
                    width: 60px;
                    height: 60px;
                    background: linear-gradient(135deg, #c53030, #e53e3e);
                    border-radius: 50%;
                    margin: 0 auto 30px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 24px;
                    color: white;
                    animation: subtlePulse 3s infinite;
                }}
                .title {{
                    color: #c53030;
                    font-size: 24px;
                    font-weight: 600;
                    margin: 0 0 20px 0;
                    text-align: center;
                }}
                .description {{
                    color: #4a5568;
                    font-size: 16px;
                    line-height: 1.6;
                    text-align: center;
                    margin-bottom: 35px;
                }}
                .otp-section {{
                    background: linear-gradient(135deg, #fed7d7 0%, #feb2b2 100%);
                    border: 2px solid #fc8181;
                    border-radius: 12px;
                    padding: 30px;
                    margin: 30px 0;
                    text-align: center;
                }}
                .otp-label {{
                    color: #742a2a;
                    font-size: 14px;
                    font-weight: 500;
                    margin-bottom: 15px;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }}
                .otp {{
                    font-size: 32px;
                    font-weight: 700;
                    color: #c53030;
                    letter-spacing: 6px;
                    font-family: 'Courier New', monospace;
                    margin: 0;
                }}
                .critical-notice {{
                    background: #fffaf0;
                    border-left: 4px solid #dd6b20;
                    border-radius: 6px;
                    padding: 20px;
                    margin: 30px 0;
                }}
                .notice-title {{
                    color: #c05621;
                    font-weight: 600;
                    margin-bottom: 8px;
                    font-size: 14px;
                }}
                .notice-text {{
                    color: #744210;
                    font-size: 14px;
                    margin: 0;
                }}
                .steps {{
                    background: #f7fafc;
                    border-radius: 8px;
                    padding: 25px;
                    margin: 30px 0;
                }}
                .step {{
                    display: flex;
                    align-items: center;
                    margin-bottom: 15px;
                    font-size: 14px;
                    color: #4a5568;
                }}
                .step-number {{
                    width: 24px;
                    height: 24px;
                    background: #c53030;
                    color: white;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin-right: 12px;
                    font-weight: 600;
                    font-size: 12px;
                }}
                .footer {{
                    background: #2d3748;
                    color: #a0aec0;
                    padding: 30px;
                    text-align: center;
                    font-size: 14px;
                }}
                .footer-link {{
                    color: #63b3ed;
                    text-decoration: none;
                }}
                .divider {{
                    height: 1px;
                    background: #e2e8f0;
                    margin: 30px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="logo">🔑 Sākṣin</div>
                    <div class="subtitle">Password Recovery Service</div>
                </div>
                <div class="content">
                    <div class="reset-badge">🔓</div>
                    <h1 class="title">Password Reset Request</h1>
                    <p class="description">
                        We received a request to reset your password. Use the verification code below to proceed with creating a new password.
                    </p>
                    
                    <div class="otp-section">
                        <div class="otp-label">Reset Verification Code</div>
                        <div class="otp">{otp}</div>
                    </div>
                    
                    <div class="steps">
                        <h3 style="color: #2d3748; margin: 0 0 20px 0; font-size: 16px;">Next Steps:</h3>
                        <div class="step">
                            <div class="step-number">1</div>
                            <span>Enter the verification code above</span>
                        </div>
                        <div class="step">
                            <div class="step-number">2</div>
                            <span>Create a strong, unique password</span>
                        </div>
                        <div class="step">
                            <div class="step-number">3</div>
                            <span>Log in with your new credentials</span>
                        </div>
                    </div>
                    
                    <div class="critical-notice">
                        <div class="notice-title">⚠️ Security Alert</div>
                        <p class="notice-text">If you did not request this password reset, please contact our security team immediately. This code expires in 10 minutes.</p>
                    </div>
                    
                    <div class="divider"></div>
                    
                    <p style="color: #718096; font-size: 14px; text-align: center; margin: 0;">
                        For security reasons, this link can only be used once and expires after 10 minutes.
                    </p>
                </div>
                <div class="footer">
                    <p>© 2025 Sākṣin. All rights reserved.</p>
                    <p>Security: <a href="mailto:security@saksin.ai" class="footer-link">security@saksin.ai</a></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"Sākṣin Password Reset Code: {otp}\n\nUse this code to reset your password. This code expires in 10 minutes.\n\nIf you did not request this reset, please contact security@saksin.ai immediately."

        self.send_email(subject, text_content, html_content=html_content)
        return otp

class RegistrationOtpSender(BaseOtpEmailSender):
    def __init__(self,email):
        super().__init__(email,purpose="register")


    def send(self):
        otp = self.generate_otp()
        subject = "📧 Sākṣin - Account Verification Required"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Account Verification</title>
            <style>
                @keyframes slideDown {{
                    from {{ transform: translateY(-20px); opacity: 0; }}
                    to {{ transform: translateY(0); opacity: 1; }}
                }}
                @keyframes subtlePulse {{
                    0%, 100% {{ transform: scale(1); }}
                    50% {{ transform: scale(1.02); }}
                }}
                .container {{
                    max-width: 650px;
                    margin: 0 auto;
                    background: #f5f7fa;
                    font-family: 'Arial', sans-serif;
                    padding: 0;
                }}
                .header {{
                    background: linear-gradient(135deg, #2b6cb0 0%, #3182ce 100%);
                    padding: 40px 30px;
                    text-align: center;
                    color: white;
                }}
                .logo {{
                    font-size: 28px;
                    font-weight: 600;
                    margin-bottom: 8px;
                    letter-spacing: 1px;
                }}
                .subtitle {{
                    font-size: 16px;
                    opacity: 0.9;
                    font-weight: 300;
                }}
                .content {{
                    background: white;
                    padding: 50px 40px;
                    animation: slideDown 0.6s ease-out;
                }}
                .verify-badge {{
                    width: 60px;
                    height: 60px;
                    background: linear-gradient(135deg, #2b6cb0, #3182ce);
                    border-radius: 50%;
                    margin: 0 auto 30px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 24px;
                    color: white;
                    animation: subtlePulse 3s infinite;
                }}
                .title {{
                    color: #2b6cb0;
                    font-size: 24px;
                    font-weight: 600;
                    margin: 0 0 20px 0;
                    text-align: center;
                }}
                .description {{
                    color: #4a5568;
                    font-size: 16px;
                    line-height: 1.6;
                    text-align: center;
                    margin-bottom: 35px;
                }}
                .otp-section {{
                    background: linear-gradient(135deg, #ebf8ff 0%, #bee3f8 100%);
                    border: 2px solid #90cdf4;
                    border-radius: 12px;
                    padding: 30px;
                    margin: 30px 0;
                    text-align: center;
                }}
                .otp-label {{
                    color: #2c5282;
                    font-size: 14px;
                    font-weight: 500;
                    margin-bottom: 15px;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }}
                .otp {{
                    font-size: 32px;
                    font-weight: 700;
                    color: #2b6cb0;
                    letter-spacing: 6px;
                    font-family: 'Courier New', monospace;
                    margin: 0;
                }}
                .progress-section {{
                    background: #f7fafc;
                    border-radius: 8px;
                    padding: 25px;
                    margin: 30px 0;
                }}
                .progress-title {{
                    color: #2d3748;
                    font-weight: 600;
                    margin-bottom: 20px;
                    font-size: 16px;
                    text-align: center;
                }}
                .progress-steps {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    position: relative;
                }}
                .progress-step {{
                    text-align: center;
                    flex: 1;
                }}
                .step-circle {{
                    width: 36px;
                    height: 36px;
                    border-radius: 50%;
                    margin: 0 auto 8px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: 600;
                    font-size: 14px;
                }}
                .step-completed {{
                    background: #48bb78;
                    color: white;
                }}
                .step-active {{
                    background: #3182ce;
                    color: white;
                }}
                .step-pending {{
                    background: #e2e8f0;
                    color: #a0aec0;
                }}
                .step-text {{
                    font-size: 12px;
                    color: #718096;
                    font-weight: 500;
                }}
                .progress-line {{
                    position: absolute;
                    top: 18px;
                    left: 25%;
                    right: 25%;
                    height: 2px;
                    background: #e2e8f0;
                    z-index: 1;
                }}
                .progress-fill {{
                    height: 100%;
                    background: #48bb78;
                    width: 50%;
                }}
                .welcome-notice {{
                    background: #f0fff4;
                    border-left: 4px solid #48bb78;
                    border-radius: 6px;
                    padding: 20px;
                    margin: 30px 0;
                }}
                .notice-title {{
                    color: #276749;
                    font-weight: 600;
                    margin-bottom: 8px;
                    font-size: 14px;
                }}
                .notice-text {{
                    color: #2f855a;
                    font-size: 14px;
                    margin: 0;
                }}
                .features {{
                    background: #f7fafc;
                    border-radius: 8px;
                    padding: 25px;
                    margin: 30px 0;
                }}
                .feature {{
                    display: flex;
                    align-items: center;
                    margin-bottom: 12px;
                    font-size: 14px;
                    color: #4a5568;
                }}
                .feature-icon {{
                    margin-right: 12px;
                    font-size: 16px;
                }}
                .footer {{
                    background: #2d3748;
                    color: #a0aec0;
                    padding: 30px;
                    text-align: center;
                    font-size: 14px;
                }}
                .footer-link {{
                    color: #63b3ed;
                    text-decoration: none;
                }}
                .divider {{
                    height: 1px;
                    background: #e2e8f0;
                    margin: 30px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="logo">📧 Sākṣin</div>
                    <div class="subtitle">Professional Interview Platform</div>
                </div>
                <div class="content">
                    <div class="verify-badge">✓</div>
                    <h1 class="title">Complete Your Registration</h1>
                    <p class="description">
                        Welcome to Sākṣin! You're one step away from accessing our professional interview platform. Please verify your email address using the code below.
                    </p>
                    
                    <div class="progress-section">
                        <div class="progress-title">Registration Progress</div>
                        <div class="progress-steps">
                            <div class="progress-line">
                                <div class="progress-fill"></div>
                            </div>
                            <div class="progress-step">
                                <div class="step-circle step-completed">✓</div>
                                <div class="step-text">Account Created</div>
                            </div>
                            <div class="progress-step">
                                <div class="step-circle step-active">2</div>
                                <div class="step-text">Email Verification</div>
                            </div>
                            <div class="progress-step">
                                <div class="step-circle step-pending">3</div>
                                <div class="step-text">Complete Setup</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="otp-section">
                        <div class="otp-label">Verification Code</div>
                        <div class="otp">{otp}</div>
                    </div>
                    
                    <div class="features">
                        <h3 style="color: #2d3748; margin: 0 0 20px 0; font-size: 16px;">What's waiting for you:</h3>
                        <div class="feature">
                            <div class="feature-icon">🎯</div>
                            <span>AI-powered interview simulations</span>
                        </div>
                        <div class="feature">
                            <div class="feature-icon">📊</div>
                            <span>Detailed performance analytics</span>
                        </div>
                        <div class="feature">
                            <div class="feature-icon">🏆</div>
                            <span>Industry-specific question banks</span>
                        </div>
                        <div class="feature">
                            <div class="feature-icon">📈</div>
                            <span>Progress tracking and improvement insights</span>
                        </div>
                    </div>
                    
                    <div class="welcome-notice">
                        <div class="notice-title">🎯 Professional Development</div>
                        <p class="notice-text">This verification code expires in 10 minutes. Keep this information confidential and secure.</p>
                    </div>
                    
                    <div class="divider"></div>
                    
                    <p style="color: #718096; font-size: 14px; text-align: center; margin: 0;">
                        If you didn't create this account, please ignore this email or contact our support team.
                    </p>
                </div>
                <div class="footer">
                    <p>© 2025 Sākṣin. All rights reserved.</p>
                    <p>Support: <a href="mailto:support@saksin.ai" class="footer-link">support@saksin.ai</a></p>
                    <p style="margin-top: 15px; font-size: 12px;">
                        <a href="#" class="footer-link">Privacy Policy</a> | 
                        <a href="#" class="footer-link">Terms of Service</a> | 
                        <a href="#" class="footer-link">Help Center</a>
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

        text_content = f"Welcome to Sākṣin!\n\nVerification Code: {otp}\n\nPlease use this code to complete your account verification. This code expires in 10 minutes.\n\nIf you didn't create this account, please ignore this email."

        self.send_email(subject, text_content, html_content=html_content)
        return otp
class UpdatePasswordOtpSender(BaseOtpEmailSender):
    def __init__(self,email):
        super().__init__(email,purpose="update")


    def send(self):
        otp = self.generate_otp()
        subject = "🔐 Sākṣin - Password Update Authorization"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Password Update</title>
            <style>
                @keyframes slideDown {{
                    from {{ transform: translateY(-20px); opacity: 0; }}
                    to {{ transform: translateY(0); opacity: 1; }}
                }}
                @keyframes subtlePulse {{
                    0%, 100% {{ transform: scale(1); }}
                    50% {{ transform: scale(1.02); }}
                }}
                .container {{
                    max-width: 650px;
                    margin: 0 auto;
                    background: #f5f7fa;
                    font-family: 'Arial', sans-serif;
                    padding: 0;
                }}
                .header {{
                    background: linear-gradient(135deg, #553c9a 0%, #6b46c1 100%);
                    padding: 40px 30px;
                    text-align: center;
                    color: white;
                }}
                .logo {{
                    font-size: 28px;
                    font-weight: 600;
                    margin-bottom: 8px;
                    letter-spacing: 1px;
                }}
                .subtitle {{
                    font-size: 16px;
                    opacity: 0.9;
                    font-weight: 300;
                }}
                .content {{
                    background: white;
                    padding: 50px 40px;
                    animation: slideDown 0.6s ease-out;
                }}
                .security-badge {{
                    width: 60px;
                    height: 60px;
                    background: linear-gradient(135deg, #553c9a, #6b46c1);
                    border-radius: 50%;
                    margin: 0 auto 30px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 24px;
                    color: white;
                    animation: subtlePulse 3s infinite;
                }}
                .title {{
                    color: #553c9a;
                    font-size: 24px;
                    font-weight: 600;
                    margin: 0 0 20px 0;
                    text-align: center;
                }}
                .description {{
                    color: #4a5568;
                    font-size: 16px;
                    line-height: 1.6;
                    text-align: center;
                    margin-bottom: 35px;
                }}
                .otp-section {{
                    background: linear-gradient(135deg, #f3f0ff 0%, #ddd6fe 100%);
                    border: 2px solid #c4b5fd;
                    border-radius: 12px;
                    padding: 30px;
                    margin: 30px 0;
                    text-align: center;
                }}
                .otp-label {{
                    color: #44337a;
                    font-size: 14px;
                    font-weight: 500;
                    margin-bottom: 15px;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }}
                .otp {{
                    font-size: 32px;
                    font-weight: 700;
                    color: #553c9a;
                    letter-spacing: 6px;
                    font-family: 'Courier New', monospace;
                    margin: 0;
                }}
                .progress-container {{
                    background: #f7fafc;
                    border-radius: 8px;
                    padding: 25px;
                    margin: 30px 0;
                }}
                .progress-title {{
                    color: #2d3748;
                    font-weight: 600;
                    margin-bottom: 20px;
                    font-size: 16px;
                    text-align: center;
                }}
                .timeline {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    position: relative;
                }}
                .timeline-step {{
                    text-align: center;
                    flex: 1;
                    position: relative;
                    z-index: 2;
                }}
                .timeline-circle {{
                    width: 40px;
                    height: 40px;
                    border-radius: 50%;
                    margin: 0 auto 10px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: 600;
                    font-size: 14px;
                }}
                .step-completed {{
                    background: #48bb78;
                    color: white;
                }}
                .step-active {{
                    background: #6b46c1;
                    color: white;
                    animation: subtlePulse 2s infinite;
                }}
                .step-pending {{
                    background: #e2e8f0;
                    color: #a0aec0;
                }}
                .step-label {{
                    font-size: 12px;
                    color: #718096;
                    font-weight: 500;
                }}
                .progress-line {{
                    position: absolute;
                    top: 20px;
                    left: 15%;
                    right: 15%;
                    height: 2px;
                    background: #e2e8f0;
                    z-index: 1;
                }}
                .progress-fill {{
                    height: 100%;
                    background: #48bb78;
                    width: 50%;
                    border-radius: 1px;
                }}
                .security-tips {{
                    background: #f0f9ff;
                    border-left: 4px solid #0ea5e9;
                    border-radius: 6px;
                    padding: 20px;
                    margin: 30px 0;
                }}
                .tips-title {{
                    color: #0c4a6e;
                    font-weight: 600;
                    margin-bottom: 15px;
                    font-size: 14px;
                }}
                .tip-item {{
                    display: flex;
                    align-items: flex-start;
                    margin-bottom: 8px;
                    font-size: 14px;
                    color: #0369a1;
                }}
                .tip-bullet {{
                    margin-right: 8px;
                    margin-top: 2px;
                }}
                .security-notice {{
                    background: #fffaf0;
                    border-left: 4px solid #dd6b20;
                    border-radius: 6px;
                    padding: 20px;
                    margin: 30px 0;
                }}
                .notice-title {{
                    color: #c05621;
                    font-weight: 600;
                    margin-bottom: 8px;
                    font-size: 14px;
                }}
                .notice-text {{
                    color: #744210;
                    font-size: 14px;
                    margin: 0;
                }}
                .footer {{
                    background: #2d3748;
                    color: #a0aec0;
                    padding: 30px;
                    text-align: center;
                    font-size: 14px;
                }}
                .footer-link {{
                    color: #63b3ed;
                    text-decoration: none;
                }}
                .divider {{
                    height: 1px;
                    background: #e2e8f0;
                    margin: 30px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="logo">🔐 Sākṣin</div>
                    <div class="subtitle">Account Security Center</div>
                </div>
                <div class="content">
                    <div class="security-badge">🔄</div>
                    <h1 class="title">Password Update Request</h1>
                    <p class="description">
                        You have requested to update your account password. Please use the authorization code below to proceed with this security-sensitive operation.
                    </p>
                    
                    <div class="progress-container">
                        <div class="progress-title">Security Process</div>
                        <div class="timeline">
                            <div class="progress-line">
                                <div class="progress-fill"></div>
                            </div>
                            <div class="timeline-step">
                                <div class="timeline-circle step-completed">✓</div>
                                <div class="step-label">Request Initiated</div>
                            </div>
                            <div class="timeline-step">
                                <div class="timeline-circle step-active">2</div>
                                <div class="step-label">Email Verification</div>
                            </div>
                            <div class="timeline-step">
                                <div class="timeline-circle step-pending">3</div>
                                <div class="step-label">Password Update</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="otp-section">
                        <div class="otp-label">Authorization Code</div>
                        <div class="otp">{otp}</div>
                    </div>
                    
                    <div class="security-tips">
                        <div class="tips-title">🛡️ Password Security Best Practices</div>
                        <div class="tip-item">
                            <div class="tip-bullet">•</div>
                            <span>Use a combination of uppercase, lowercase, numbers, and symbols</span>
                        </div>
                        <div class="tip-item">
                            <div class="tip-bullet">•</div>
                            <span>Create a password that's at least 12 characters long</span>
                        </div>
                        <div class="tip-item">
                            <div class="tip-bullet">•</div>
                            <span>Avoid using personal information or dictionary words</span>
                        </div>
                        <div class="tip-item">
                            <div class="tip-bullet">•</div>
                            <span>Consider enabling two-factor authentication</span>
                        </div>
                    </div>
                    
                    <div class="security-notice">
                        <div class="notice-title">⚠️ Important Security Information</div>
                        <p class="notice-text">This authorization code expires in 10 minutes. If you did not request this password change, please contact our security team immediately and do not share this code.</p>
                    </div>
                    
                    <div class="divider"></div>
                    
                    <p style="color: #718096; font-size: 14px; text-align: center; margin: 0;">
                        This request was initiated from your account. If this was not you, please secure your account immediately.
                    </p>
                </div>
                <div class="footer">
                    <p>© 2025 Sākṣin. All rights reserved.</p>
                    <p>Security Team: <a href="mailto:security@saksin.ai" class="footer-link">security@saksin.ai</a></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"Sākṣin Password Update Authorization\n\nAuthorization Code: {otp}\n\nThis code expires in 10 minutes. Use it to complete your password update.\n\nIf you did not request this change, contact security@saksin.ai immediately."

        self.send_email(subject, text_content, html_content=html_content)
        return otp
    




















