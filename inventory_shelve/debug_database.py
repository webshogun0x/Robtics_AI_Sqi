#!/usr/bin/env python3
"""
Debug script to check database content and operations
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from inventory_web import create_app, db
from inventory_web.models import Inventory, Log
from datetime import datetime

def check_database():
    app = create_app()
    with app.app_context():
        print("🔍 Database Debug Information")
        print("=" * 50)
        
        # Check inventory items
        print("\n📦 INVENTORY ITEMS:")
        inventory_items = Inventory.query.all()
        for item in inventory_items:
            print(f"  ID: {item.id} | {item.name} ({item.category}) | Qty: {item.quantity} | Consumable: {item.consumable}")
        
        print(f"\nTotal inventory items: {len(inventory_items)}")
        
        # Check logs
        print("\n📋 LOG ENTRIES:")
        logs = Log.query.order_by(Log.timestamp.desc()).all()
        for log in logs:
            print(f"  ID: {log.id} | {log.user} | {log.action} | {log.component} | Qty: {log.quantity} | Time: {log.timestamp}")
        
        print(f"\nTotal log entries: {len(logs)}")
        
        # Test adding a log entry
        print("\n🧪 TESTING LOG CREATION:")
        test_log = Log(
            user="Test User",
            action="take", 
            component="Arduino Uno",
            quantity=1
        )
        
        try:
            db.session.add(test_log)
            db.session.commit()
            print("✅ Test log entry created successfully")
            
            # Verify it was added
            new_logs = Log.query.order_by(Log.timestamp.desc()).limit(1).all()
            if new_logs:
                latest = new_logs[0]
                print(f"✅ Latest log: {latest.user} | {latest.action} | {latest.component} | {latest.timestamp}")
            
        except Exception as e:
            print(f"❌ Error creating test log: {e}")
            db.session.rollback()

def simulate_transaction():
    """Simulate a take/return transaction"""
    app = create_app()
    with app.app_context():
        print("\n🔄 SIMULATING TRANSACTION:")
        
        # Get an inventory item
        item = Inventory.query.first()
        if not item:
            print("❌ No inventory items found")
            return
        
        print(f"📦 Selected item: {item.name} (Current qty: {item.quantity})")
        
        # Simulate taking 1 item
        original_qty = item.quantity
        item.quantity -= 1
        
        # Create log entry
        log_entry = Log(
            user="Debug User",
            action="take",
            component=item.name,
            quantity=1
        )
        
        try:
            db.session.add(log_entry)
            db.session.commit()
            
            print(f"✅ Transaction completed:")
            print(f"   - {item.name} quantity: {original_qty} → {item.quantity}")
            print(f"   - Log entry created: {log_entry.id}")
            
            # Verify log was saved
            saved_log = Log.query.get(log_entry.id)
            if saved_log:
                print(f"✅ Log verified: {saved_log.user} {saved_log.action} {saved_log.component}")
            else:
                print("❌ Log not found after commit")
                
        except Exception as e:
            print(f"❌ Transaction failed: {e}")
            db.session.rollback()

if __name__ == "__main__":
    check_database()
    simulate_transaction()
    
    print("\n" + "=" * 50)
    print("🔍 Re-checking database after simulation:")
    check_database()