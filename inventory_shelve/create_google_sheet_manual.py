#!/usr/bin/env python3
"""
Manual Google Sheets creation guide and CSV template generator
"""
import csv
import os
from datetime import datetime

def create_google_sheets_template():
    """Create CSV templates that can be imported into Google Sheets"""
    
    # Create templates directory
    os.makedirs("google_sheets_templates", exist_ok=True)
    
    # Create inventory template
    inventory_template = "google_sheets_templates/inventory_template.csv"
    with open(inventory_template, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'category', 'quantity', 'consumable', 'last_updated'])
        
        # Sample data
        sample_data = [
            ['Arduino Uno', 'Electronics', 10, 'FALSE', ''],
            ['Raspberry Pi 4', 'Electronics', 5, 'FALSE', ''],
            ['Resistor 220Ω', 'Electronics', 100, 'TRUE', ''],
            ['LED Red', 'Electronics', 50, 'TRUE', ''],
            ['Breadboard', 'Electronics', 15, 'FALSE', ''],
            ['Servo Motor', 'Mechanical', 8, 'FALSE', ''],
            ['Stepper Motor', 'Mechanical', 6, 'FALSE', ''],
            ['Screws M3x10', 'Mechanical', 200, 'TRUE', ''],
            ['Bearings 608', 'Mechanical', 20, 'FALSE', ''],
            ['Multimeter', 'Tools', 3, 'FALSE', ''],
            ['Soldering Iron', 'Tools', 4, 'FALSE', ''],
            ['Wire Strippers', 'Tools', 2, 'FALSE', '']
        ]
        
        writer.writerows(sample_data)
    
    # Create logs template
    logs_template = "google_sheets_templates/logs_template.csv"
    with open(logs_template, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['user', 'action', 'component', 'quantity', 'timestamp'])
        
        # Sample log entries
        sample_logs = [
            ['John Doe', 'take', 'Arduino Uno', 2, '2025-08-07 10:30:00'],
            ['Jane Smith', 'return', 'Multimeter', 1, '2025-08-07 11:15:00'],
            ['Bob Wilson', 'take', 'LED Red', 10, '2025-08-07 14:20:00']
        ]
        
        writer.writerows(sample_logs)
    
    print("✅ Created Google Sheets templates:")
    print(f"   📊 {inventory_template}")
    print(f"   📋 {logs_template}")
    
    return inventory_template, logs_template

def print_manual_setup_instructions():
    """Print step-by-step manual setup instructions"""
    
    instructions = """
🚀 MANUAL GOOGLE SHEETS SETUP INSTRUCTIONS

📋 Step 1: Create Google Sheets
1. Go to https://sheets.google.com
2. Create a new spreadsheet
3. Name it "Lab Inventory Management"
4. Create two sheets:
   - Sheet 1: Rename to "Inventory"
   - Sheet 2: Rename to "Logs" (Insert > Sheet)

📊 Step 2: Setup Inventory Sheet
1. In the "Inventory" sheet, add these headers in row 1:
   A1: name
   B1: category  
   C1: quantity
   D1: consumable
   E1: last_updated

2. Import the inventory template:
   - File > Import > Upload > Select inventory_template.csv
   - Choose "Replace current sheet"
   - OR manually copy data from the CSV file

📋 Step 3: Setup Logs Sheet  
1. In the "Logs" sheet, add these headers in row 1:
   A1: user
   B1: action
   C1: component
   D1: quantity
   E1: timestamp

2. Import the logs template:
   - File > Import > Upload > Select logs_template.csv
   - Choose "Replace current sheet"
   - OR manually copy data from the CSV file

🔗 Step 4: Get Sheet ID
1. Look at the URL of your Google Sheet
2. Copy the ID from the URL (between /d/ and /edit):
   https://docs.google.com/spreadsheets/d/[SHEET_ID_HERE]/edit
3. Update your .env file:
   GOOGLE_SHEET_ID=your-actual-sheet-id

📧 Step 5: Email Configuration
1. For Gmail users:
   - Enable 2-Factor Authentication
   - Generate App Password: Google Account > Security > App passwords
   - Use the 16-digit app password (no spaces)

2. Update .env file:
   EMAIL_SENDER=your-email@gmail.com
   EMAIL_RECEIVER=recipient@gmail.com
   EMAIL_USERNAME=your-email@gmail.com
   EMAIL_PASSWORD=your-16-digit-app-password
   EMAIL_SMTP_SERVER=smtp.gmail.com
   EMAIL_SMTP_PORT=587

🔧 Step 6: Test the System
1. Test email: python test_email.py
2. Export logs: python reconciliation/export_logs.py
3. Run web app: python run.py

⚠️  Note: Without service account setup, Google Sheets integration 
   will be read-only. For full automation, follow the service account 
   setup in setup_instructions.md

✅ Manual sync process:
1. Export data using: python reconciliation/export_logs.py
2. Manually import CSV files into Google Sheets
3. Email reports will be sent automatically
"""
    
    print(instructions)

def main():
    print("📋 Creating Google Sheets templates and setup guide...")
    
    # Create templates
    inventory_file, logs_file = create_google_sheets_template()
    
    # Print instructions
    print_manual_setup_instructions()
    
    print(f"""
🎯 QUICK START:
1. Use the generated CSV templates to create your Google Sheets
2. Update the GOOGLE_SHEET_ID in .env file
3. Configure email credentials in .env file
4. Run: python test_email.py
5. Run: python reconciliation/export_logs.py

📁 Template files created in: google_sheets_templates/
""")

if __name__ == "__main__":
    main()