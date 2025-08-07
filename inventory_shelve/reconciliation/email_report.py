import smtplib
from email.message import EmailMessage
import mimetypes
import os
from dotenv import load_dotenv

load_dotenv()

def send_email(subject, body, attachment_path=None):
    sender_mail = os.getenv("EMAIL_SENDER")
    receiver_mail = os.getenv("EMAIL_RECEIVER")
    username = os.getenv("EMAIL_USERNAME") or sender_mail
    password = os.getenv("EMAIL_PASSWORD")
    smtp_server = os.getenv("EMAIL_SMTP_SERVER")
    smtp_port = int(os.getenv("EMAIL_SMTP_PORT", 587))
    
    if not all([sender_mail, receiver_mail, password, smtp_server]):
        print("❌ Email configuration incomplete. Check .env file.")
        return False
    
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_mail
    msg['To'] = receiver_mail
    msg.set_content(body)

    if attachment_path and os.path.isfile(attachment_path):
        mime_type, _ = mimetypes.guess_type(attachment_path)
        if mime_type:
            mime_type, mime_subtype = mime_type.split('/')
            with open(attachment_path, 'rb') as f:
                msg.add_attachment(f.read(),
                                   maintype=mime_type,
                                   subtype=mime_subtype,
                                   filename=os.path.basename(attachment_path))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(username, password)
            server.send_message(msg)
        print("✅ Email sent successfully.")
        return True
    except Exception as e:
        print(f"❌ Email failed: {e}")
        return False
