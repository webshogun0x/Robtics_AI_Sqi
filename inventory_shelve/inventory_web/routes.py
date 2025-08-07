from flask import render_template, request, jsonify, redirect, current_app
from . import db
from .models import Inventory, Log
from flask import current_app as app
import requests

@app.route('/')
def index():
    categories = db.session.query(Inventory.category).distinct().all()
    return render_template('index.html', categories=[c[0] for c in categories])

@app.route('/components/<category>')
def get_components(category):
    components = Inventory.query.filter_by(category=category).all()
    return jsonify([{ 'id': c.id, 'name': c.name } for c in components])

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form
    user = data.get('user')
    action = data.get('action')
    component_id = data.get('component_id')
    quantity = int(data.get('quantity'))

    component = Inventory.query.get(component_id)
    if not component:
        return 'Component not found', 400

    if action == 'take' and component.quantity < quantity:
        return 'Not enough stock', 400

    component.quantity += quantity if action == 'return' else -quantity
    db.session.add(Log(user=user, action=action, component=component.name, quantity=quantity))
    db.session.commit()

    try:
        requests.get(app.config['ESP32_UNLOCK_URL'])
    except Exception as e:
        print(f'ESP32 Unlock Error: {e}')

    return redirect('/')

@app.route('/logs')
def view_logs():
    logs = Log.query.order_by(Log.timestamp.desc()).limit(50).all()
    return render_template('logs.html', logs=logs)

@app.route('/export')
def export_logs():
    import csv
    from io import StringIO

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['User', 'Action', 'Component', 'Quantity', 'Timestamp'])

    for log in Log.query.order_by(Log.timestamp.desc()).all():
        writer.writerow([log.user, log.action, log.component, log.quantity, log.timestamp])

    output.seek(0)
    return output.getvalue(), 200, {
        'Content-Type': 'text/csv',
        'Content-Disposition': 'attachment; filename=logs.csv'
    }
