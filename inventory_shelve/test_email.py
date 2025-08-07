#!/usr/bin/env python3
"""
Test script to verify email configuration
"""
from reconciliation.email_report import send_email
from datetime import datetime
import os

def test_email():
    print("📧 Testing email configuration...")
    
    # Check if email credentials are set
    sender = os.getenv("EMAIL_SENDER")
    receiver = os.getenv("EMAIL_RECEIVER")
    password = os.getenv("EMAIL_PASSWORD")
    
    if not sender or not receiver or not password:
        print("❌ Email credentials not configured in .env file")
        print("Please update the following in .env:")
        print("- EMAIL_SENDER")
        print("- EMAIL_RECEIVER") 
        print("- EMAIL_PASSWORD")
        return False
    
    print(f"📤 Sending test email from {sender} to {receiver}")
    
    subject = "🧪 Lab Inventory System - Test Email"
    body = f"""Test Email from Lab Inventory System

This is a test email to verify the email configuration is working correctly.

Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

If you received this email, the email integration is working properly!

System Details:
- Sender: {sender}
- SMTP Server: {os.getenv('EMAIL_SMTP_SERVER')}
- SMTP Port: {os.getenv('EMAIL_SMTP_PORT')}

Next steps:
1. Run the inventory reconciliation script
2. Check Google Sheets integration
3. Test the web application

Best regards,
Lab Inventory Management System"""
    
    success = send_email(subject, body)
    
    if success:
        print("✅ Test email sent successfully!")
        print("📬 Check your inbox to confirm delivery")
        return True
    else:
        print("❌ Test email failed")
        print("💡 Common solutions:")
        print("   - Check your app password (Gmail users need 16-digit app password)")
        print("   - Verify SMTP settings in .env file")
        print("   - Ensure 2FA is enabled for Gmail")
        return False

if __name__ == "__main__":
    test_email()