import sqlite3
import json
from google_auth import get_sheet
from email_report import send_email
from generate_report import generate_csv
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_path) as f:
        config = json.load(f)
    
    # Override with environment variables if available
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    if sheet_id and sheet_id != "your-google-sheet-id":
        config["google_sheet_id"] = sheet_id
    
    return config

def get_sqlite_inventory(sqlite_path):
    if not os.path.exists(sqlite_path):
        print(f"❌ Database not found: {sqlite_path}")
        return {}
    
    conn = sqlite3.connect(sqlite_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name, quantity FROM inventory")
    rows = cursor.fetchall()
    conn.close()
    return {name: qty for name, qty in rows}

def get_sheet_inventory(sheet):
    try:
        records = sheet.get_all_records()
        return {row['name']: int(row['quantity']) for row in records if 'name' in row and 'quantity' in row}
    except Exception as e:
        print(f"❌ Error reading Google Sheet: {e}")
        return {}

def compare(local_inv, sheet_inv):
    all_keys = set(local_inv.keys()).union(sheet_inv.keys())
    discrepancies = []

    for key in sorted(all_keys):
        local_qty = local_inv.get(key, 0)
        sheet_qty = sheet_inv.get(key, 0)
        if local_qty != sheet_qty:
            discrepancies.append({
                "component": key,
                "sqlite_qty": local_qty,
                "sheet_qty": sheet_qty,
                "difference": local_qty - sheet_qty
            })
    return discrepancies

def main():
    print(f"🔄 Starting inventory reconciliation at {datetime.now()}")
    
    try:
        config = load_config()
        
        if config["google_sheet_id"] == "your-google-sheet-id":
            print("❌ Google Sheet ID not configured. Please run setup_google_sheets.py first.")
            return
        
        print(f"📊 Connecting to Google Sheet: {config['google_sheet_id']}")
        sheet = get_sheet(config["google_sheet_id"], config["sheet_name"])
        
        print(f"💾 Reading local database: {config['sqlite_path']}")
        local = get_sqlite_inventory(config["sqlite_path"])
        
        print("📋 Reading Google Sheet data...")
        sheet_data = get_sheet_inventory(sheet)
        
        print(f"🔍 Comparing {len(local)} local items with {len(sheet_data)} sheet items")
        mismatches = compare(local, sheet_data)

        if mismatches:
            print(f"⚠️  Found {len(mismatches)} discrepancies:")
            for m in mismatches:
                print(f"  {m['component']}: Local={m['sqlite_qty']} | Sheet={m['sheet_qty']} | Δ={m['difference']}")
            
            csv_path = generate_csv(mismatches)
            print(f"📄 Generated report: {csv_path}")
            
            body = f"""Inventory Reconciliation Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Found {len(mismatches)} discrepancies between local database and Google Sheet.

Discrepancies:
"""
            for m in mismatches:
                body += f"\n- {m['component']}: Local={m['sqlite_qty']}, Sheet={m['sheet_qty']}, Difference={m['difference']}"
            
            body += "\n\nPlease see the attached CSV report for details."
            
            if send_email(
                "🚨 Inventory Mismatch Report",
                body,
                attachment_path=csv_path
            ):
                print("📧 Email report sent successfully")
        else:
            print("✅ Inventory matches exactly!")
            send_email(
                "✅ Inventory Reconciliation Report", 
                f"Inventory reconciliation completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\nAll inventory items match between local database and Google Sheet. No discrepancies found."
            )
            
    except Exception as e:
        print(f"❌ Reconciliation failed: {e}")
        send_email(
            "❌ Inventory Reconciliation Error",
            f"Inventory reconciliation failed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\nError: {str(e)}"
        )

if __name__ == "__main__":
    main()
