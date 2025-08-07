#!/usr/bin/env python3
"""
System status script to show current inventory and logs
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from inventory_web import create_app, db
from inventory_web.models import Inventory, Log
from datetime import datetime, timedelta
import sqlite3

def show_system_status():
    app = create_app()
    with app.app_context():
        print("🏭 LAB INVENTORY SYSTEM STATUS")
        print("=" * 60)
        print(f"📅 Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Inventory Summary
        print("\n📦 INVENTORY SUMMARY:")
        print("-" * 40)
        
        categories = db.session.query(Inventory.category).distinct().all()
        total_items = 0
        total_quantity = 0
        
        for category_tuple in categories:
            category = category_tuple[0]
            items = Inventory.query.filter_by(category=category).all()
            category_qty = sum(item.quantity for item in items)
            total_items += len(items)
            total_quantity += category_qty
            
            print(f"  {category}:")
            for item in items:
                status = "🔴 OUT OF STOCK" if item.quantity == 0 else f"✅ {item.quantity} available"
                consumable = "📝 Consumable" if item.consumable else "🔄 Reusable"
                print(f"    - {item.name}: {status} ({consumable})")
            print(f"    Category Total: {category_qty} items")
            print()
        
        print(f"📊 TOTALS: {total_items} unique items, {total_quantity} total quantity")
        
        # Recent Activity
        print("\n📋 RECENT ACTIVITY (Last 24 hours):")
        print("-" * 40)
        
        yesterday = datetime.now() - timedelta(days=1)
        recent_logs = Log.query.filter(Log.timestamp >= yesterday).order_by(Log.timestamp.desc()).all()
        
        if recent_logs:
            for log in recent_logs:
                action_icon = "📤" if log.action == "take" else "📥"
                print(f"  {action_icon} {log.timestamp.strftime('%H:%M:%S')} | {log.user} | {log.action.upper()} {log.quantity}x {log.component}")
        else:
            print("  No recent activity")
        
        # All-time Activity Summary
        print(f"\n📈 ACTIVITY SUMMARY:")
        print("-" * 40)
        
        all_logs = Log.query.all()
        take_logs = [log for log in all_logs if log.action == "take"]
        return_logs = [log for log in all_logs if log.action == "return"]
        
        total_taken = sum(log.quantity for log in take_logs)
        total_returned = sum(log.quantity for log in return_logs)
        
        print(f"  Total Transactions: {len(all_logs)}")
        print(f"  Items Taken: {total_taken}")
        print(f"  Items Returned: {total_returned}")
        print(f"  Net Items Out: {total_taken - total_returned}")
        
        # Most Active Users
        print(f"\n👥 MOST ACTIVE USERS:")
        print("-" * 40)
        
        user_activity = {}
        for log in all_logs:
            if log.user not in user_activity:
                user_activity[log.user] = {"take": 0, "return": 0, "total": 0}
            user_activity[log.user][log.action] += log.quantity
            user_activity[log.user]["total"] += log.quantity
        
        sorted_users = sorted(user_activity.items(), key=lambda x: x[1]["total"], reverse=True)
        
        for user, activity in sorted_users[:5]:  # Top 5 users
            print(f"  {user}: {activity['total']} total items (↗️{activity['take']} taken, ↩️{activity['return']} returned)")
        
        # Low Stock Alert
        print(f"\n⚠️  LOW STOCK ALERTS:")
        print("-" * 40)
        
        low_stock_items = Inventory.query.filter(Inventory.quantity <= 5).all()
        if low_stock_items:
            for item in low_stock_items:
                if item.quantity == 0:
                    print(f"  🔴 OUT OF STOCK: {item.name}")
                else:
                    print(f"  🟡 LOW STOCK: {item.name} ({item.quantity} remaining)")
        else:
            print("  ✅ All items have adequate stock")
        
        print("\n" + "=" * 60)

def export_status_report():
    """Export status to a text file"""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"system_status_{timestamp}.txt"
    
    # Redirect stdout to file
    import sys
    original_stdout = sys.stdout
    
    with open(filename, 'w') as f:
        sys.stdout = f
        show_system_status()
    
    sys.stdout = original_stdout
    print(f"📄 Status report exported to: {filename}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--export":
        export_status_report()
    else:
        show_system_status()
        print("\n💡 Tip: Use --export flag to save this report to a file")