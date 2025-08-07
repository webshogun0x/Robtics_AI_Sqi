#!/usr/bin/env python3
"""
Export logs from the inventory database to CSV and optionally email them
"""
import sqlite3
import csv
import os
from datetime import datetime
from email_report import send_email
from dotenv import load_dotenv

load_dotenv()

def export_logs_to_csv(db_path="../instance/inventory.db", output_dir="output"):
    """Export all logs from database to CSV file"""
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return None
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{output_dir}/inventory_logs_{timestamp}.csv"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all logs with proper column names
        cursor.execute("""
            SELECT user, action, component, quantity, timestamp 
            FROM log 
            ORDER BY timestamp DESC
        """)
        
        rows = cursor.fetchall()
        
        with open(filename, mode="w", newline="", encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["User", "Action", "Component", "Quantity", "Timestamp"])
            writer.writerows(rows)
        
        conn.close()
        
        print(f"📊 Exported {len(rows)} log entries to {filename}")
        return filename
        
    except Exception as e:
        print(f"❌ Error exporting logs: {e}")
        return None

def export_inventory_to_csv(db_path="../instance/inventory.db", output_dir="output"):
    """Export current inventory to CSV file"""
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return None
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{output_dir}/current_inventory_{timestamp}.csv"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT name, category, quantity, consumable 
            FROM inventory 
            ORDER BY category, name
        """)
        
        rows = cursor.fetchall()
        
        with open(filename, mode="w", newline="", encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Category", "Quantity", "Consumable"])
            writer.writerows(rows)
        
        conn.close()
        
        print(f"📦 Exported {len(rows)} inventory items to {filename}")
        return filename
        
    except Exception as e:
        print(f"❌ Error exporting inventory: {e}")
        return None

def main():
    print("📤 Starting data export...")
    
    # Export logs
    logs_file = export_logs_to_csv()
    
    # Export current inventory
    inventory_file = export_inventory_to_csv()
    
    # Send email with both files if configured
    if logs_file or inventory_file:
        files_exported = []
        if logs_file:
            files_exported.append(f"- Activity logs: {os.path.basename(logs_file)}")
        if inventory_file:
            files_exported.append(f"- Current inventory: {os.path.basename(inventory_file)}")
        
        body = f"""Data Export Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

The following files have been exported:

{chr(10).join(files_exported)}

Files are attached to this email for your review."""
        
        # Send email with the most recent file (logs take priority)
        attachment = logs_file if logs_file else inventory_file
        
        if send_email(
            "📊 Inventory Data Export",
            body,
            attachment_path=attachment
        ):
            print("📧 Export report sent via email")
    
    print("✅ Export complete!")

if __name__ == "__main__":
    main()