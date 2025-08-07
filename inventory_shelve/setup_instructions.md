# Lab Inventory System Setup Instructions

## 🚀 Quick Setup Guide

### 1. Google Sheets Integration

#### Step 1: Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the following APIs:
   - Google Sheets API
   - Google Drive API

#### Step 2: Create Service Account
1. Go to "IAM & Admin" > "Service Accounts"
2. Click "Create Service Account"
3. Give it a name like "inventory-service"
4. Click "Create and Continue"
5. Skip role assignment for now
6. Click "Done"

#### Step 3: Generate Key File
1. Click on your service account
2. Go to "Keys" tab
3. Click "Add Key" > "Create New Key"
4. Choose "JSON" format
5. Download the file
6. Rename it to `service_account.json`
7. Move it to the `reconciliation/` folder

#### Step 4: Run Setup Script
```bash
cd /home/web_shogun/Documents/challenge/inventory_shelve
/home/web_shogun/Documents/challenge/inventory_shelve/venv_now/bin/python setup_google_sheets.py
```

### 2. Email Configuration

#### For Gmail Users:
1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account settings
   - Security > 2-Step Verification > App passwords
   - Generate password for "Mail"
3. Update `.env` file with your credentials:
   ```
   EMAIL_SENDER=your-email@gmail.com
   EMAIL_RECEIVER=recipient@gmail.com
   EMAIL_USERNAME=your-email@gmail.com
   EMAIL_PASSWORD=your-16-digit-app-password
   EMAIL_SMTP_SERVER=smtp.gmail.com
   EMAIL_SMTP_PORT=587
   ```

#### For Other Email Providers:
Update the SMTP settings in `.env` accordingly:
- **Outlook/Hotmail**: smtp-mail.outlook.com:587
- **Yahoo**: smtp.mail.yahoo.com:587
- **Custom SMTP**: Use your provider's settings

### 3. Test the System

#### Run the Web Application:
```bash
/home/web_shogun/Documents/challenge/inventory_shelve/venv_now/bin/python run.py
```

#### Test Reconciliation:
```bash
cd reconciliation
/home/web_shogun/Documents/challenge/inventory_shelve/venv_now/bin/python compare_inventory.py
```

#### Export Logs:
```bash
cd reconciliation
/home/web_shogun/Documents/challenge/inventory_shelve/venv_now/bin/python export_logs.py
```

### 4. Automation (Optional)

#### Set up Cron Job for Daily Reconciliation:
```bash
# Edit crontab
crontab -e

# Add this line for daily reconciliation at 6 PM
0 18 * * * cd /home/web_shogun/Documents/challenge/inventory_shelve/reconciliation && /home/web_shogun/Documents/challenge/inventory_shelve/venv_now/bin/python compare_inventory.py

# Add this line for weekly log export on Sundays at 8 PM
0 20 * * 0 cd /home/web_shogun/Documents/challenge/inventory_shelve/reconciliation && /home/web_shogun/Documents/challenge/inventory_shelve/venv_now/bin/python export_logs.py
```

## 🔧 Troubleshooting

### Common Issues:

1. **"Service account file not found"**
   - Make sure `service_account.json` is in the `reconciliation/` folder
   - Check file permissions

2. **"Email authentication failed"**
   - Verify app password is correct (16 digits, no spaces)
   - Check if 2FA is enabled for Gmail
   - Verify SMTP settings

3. **"Google Sheet access denied"**
   - Make sure the sheet is shared with the service account email
   - Check if APIs are enabled in Google Cloud Console

4. **"Database not found"**
   - Run the web app first to create the database
   - Check if `inventory.db` exists in the root folder

## 📊 Features

- **Web Interface**: Add/remove inventory items
- **Google Sheets Sync**: Automatic synchronization
- **Email Reports**: Daily reconciliation reports
- **Log Export**: CSV export of all activities
- **ESP32 Integration**: Shelf locking mechanism

## 🔐 Security Notes

- Keep `service_account.json` secure and never commit to version control
- Use app passwords instead of regular passwords for email
- Regularly rotate credentials
- Limit service account permissions to minimum required