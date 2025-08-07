#!/usr/bin/env python3
"""
Script to create and setup Google Sheets for inventory management
"""
import gspread
from google.oauth2.service_account import Credentials
import json
import os
from dotenv import load_dotenv

load_dotenv()

def create_service_account_template():
    """Create a template for service account credentials"""
    template = {
        "type": "service_account",
        "project_id": "your-project-id",
        "private_key_id": "your-private-key-id",
        "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_HERE\n-----END PRIVATE KEY-----\n",
        "client_email": "your-service-account@your-project.iam.gserviceaccount.com",
        "client_id": "your-client-id",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
    }
    
    with open('reconciliation/service_account_template.json', 'w') as f:
        json.dump(template, f, indent=2)
    
    print("📝 Created service_account_template.json")
    print("🔧 Please:")
    print("   1. Go to Google Cloud Console")
    print("   2. Create a new project or select existing")
    print("   3. Enable Google Sheets API and Google Drive API")
    print("   4. Create a service account")
    print("   5. Download the JSON key file")
    print("   6. Replace service_account_template.json with your actual credentials")
    print("   7. Rename it to service_account.json")

def setup_google_sheet():
    """Create and setup the Google Sheet with proper headers"""
    try:
        # Check if service account file exists
        if not os.path.exists('reconciliation/service_account.json'):
            print("❌ service_account.json not found!")
            create_service_account_template()
            return None
        
        # Setup credentials
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        
        creds = Credentials.from_service_account_file(
            'reconciliation/service_account.json', 
            scopes=scope
        )
        client = gspread.authorize(creds)
        
        # Create new spreadsheet
        sheet_name = "Lab Inventory Management"
        spreadsheet = client.create(sheet_name)
        
        # Get the first worksheet
        worksheet = spreadsheet.sheet1
        worksheet.update_title("Inventory")
        
        # Setup headers
        headers = ["name", "category", "quantity", "consumable", "last_updated"]
        worksheet.update('A1:E1', [headers])
        
        # Add sample data from database
        from inventory_web import create_app, db
        from inventory_web.models import Inventory
        
        app = create_app()
        with app.app_context():
            items = Inventory.query.all()
            data = []
            for item in items:
                data.append([
                    item.name,
                    item.category, 
                    item.quantity,
                    str(item.consumable),
                    ""  # last_updated will be filled by reconciliation script
                ])
            
            if data:
                worksheet.update(f'A2:E{len(data)+1}', data)
        
        # Share with your email (make it editable)
        email = os.getenv('EMAIL_SENDER', 'your-email@example.com')
        try:
            spreadsheet.share(email, perm_type='user', role='writer')
            print(f"📧 Shared spreadsheet with {email}")
        except Exception as e:
            print(f"⚠️  Could not share with {email}: {e}")
        
        sheet_id = spreadsheet.id
        sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}"
        
        print(f"✅ Created Google Sheet: {sheet_name}")
        print(f"📊 Sheet ID: {sheet_id}")
        print(f"🔗 URL: {sheet_url}")
        
        # Update .env file with sheet ID
        update_env_file(sheet_id)
        
        return sheet_id
        
    except Exception as e:
        print(f"❌ Error creating Google Sheet: {e}")
        create_service_account_template()
        return None

def update_env_file(sheet_id):
    """Update .env file with the Google Sheet ID"""
    env_path = '.env'
    
    # Read existing .env content
    env_content = []
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            env_content = f.readlines()
    
    # Update or add GOOGLE_SHEET_ID
    updated = False
    for i, line in enumerate(env_content):
        if line.startswith('GOOGLE_SHEET_ID='):
            env_content[i] = f'GOOGLE_SHEET_ID={sheet_id}\n'
            updated = True
            break
    
    if not updated:
        env_content.append(f'GOOGLE_SHEET_ID={sheet_id}\n')
    
    # Write back to .env
    with open(env_path, 'w') as f:
        f.writelines(env_content)
    
    print(f"📝 Updated .env with GOOGLE_SHEET_ID={sheet_id}")

if __name__ == '__main__':
    print("🚀 Setting up Google Sheets integration...")
    sheet_id = setup_google_sheet()
    
    if sheet_id:
        print("\n✅ Setup complete!")
        print("📋 Next steps:")
        print("   1. Check your Google Drive for the new spreadsheet")
        print("   2. Verify the data looks correct")
        print("   3. Run the reconciliation script to test")
    else:
        print("\n❌ Setup failed. Please check the instructions above.")