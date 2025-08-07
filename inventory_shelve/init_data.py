#!/usr/bin/env python3
from inventory_web import create_app, db
from inventory_web.models import Inventory

def init_sample_data():
    app = create_app()
    with app.app_context():
        # Clear existing data
        Inventory.query.delete()
        
        # Sample inventory items
        items = [
            # Electronics
            Inventory(name='Arduino Uno', category='Electronics', quantity=10, consumable=False),
            Inventory(name='Raspberry Pi 4', category='Electronics', quantity=5, consumable=False),
            Inventory(name='Resistor 220Ω', category='Electronics', quantity=100, consumable=True),
            Inventory(name='LED Red', category='Electronics', quantity=50, consumable=True),
            Inventory(name='Breadboard', category='Electronics', quantity=15, consumable=False),
            
            # Mechanical
            Inventory(name='Servo Motor', category='Mechanical', quantity=8, consumable=False),
            Inventory(name='Stepper Motor', category='Mechanical', quantity=6, consumable=False),
            Inventory(name='Screws M3x10', category='Mechanical', quantity=200, consumable=True),
            Inventory(name='Bearings 608', category='Mechanical', quantity=20, consumable=False),
            
            # Tools
            Inventory(name='Multimeter', category='Tools', quantity=3, consumable=False),
            Inventory(name='Soldering Iron', category='Tools', quantity=4, consumable=False),
            Inventory(name='Wire Strippers', category='Tools', quantity=2, consumable=False),
        ]
        
        for item in items:
            db.session.add(item)
        
        db.session.commit()
        print(f"Added {len(items)} sample inventory items")

if __name__ == '__main__':
    init_sample_data()