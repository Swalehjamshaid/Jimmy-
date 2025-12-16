
import os
import smtplib
from email.mime.text import MIMEText
EMAIL_API_KEY = os.getenv("EMAIL_API_KEY", "")
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.sendgrid.net")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "apikey")

def send_email(to_email: str, subject: str, html_body: str, from_email: str = "noreply@webaudit.app"):
    msg = MIMEText(html_body, 'html')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, EMAIL_API_KEY)
        server.sendmail(from_email, [to_email], msg.as_string())
