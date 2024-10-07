from flask import Blueprint, request, jsonify, render_template
from models import db, City, Hospital, Patient, OPDQueue, Inventory, Expense
from extensions import socketio
import requests
from datetime import datetime, timedelta

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return "Welcome to SwasthyaFlow API!"

@main_bp.route('/api/cities', methods=['GET', 'POST'])
def manage_cities():
    if request.method == 'GET':
        cities = City.query.all()
        return jsonify([{'id': c.id, 'name': c.name} for c in cities])
    elif request.method == 'POST':
        data = request.json
        new_city = City(name=data['name'])
        db.session.add(new_city)
        db.session.commit()
        return jsonify({'message': 'City added successfully', 'id': new_city.id}), 201

@main_bp.route('/api/hospitals', methods=['GET', 'POST'])
def manage_hospitals():
    if request.method == 'GET':
        hospitals = Hospital.query.all()
        return jsonify([{
            'id': h.id, 
            'name': h.name, 
            'address': h.address,
            'total_beds': h.total_beds, 
            'available_beds': h.available_beds,
            'city_id': h.city_id
        } for h in hospitals])
    elif request.method == 'POST':
        data = request.json
        new_hospital = Hospital(
            name=data['name'], 
            address=data['address'],
            total_beds=data['total_beds'], 
            available_beds=data['total_beds'],
            city_id=data['city_id']
        )
        db.session.add(new_hospital)
        db.session.commit()
        socketio.emit('hospital_update', {
            'id': new_hospital.id, 
            'name': new_hospital.name, 
            'available_beds': new_hospital.available_beds
        }, namespace='/socket')
        return jsonify({'message': 'Hospital added successfully', 'id': new_hospital.id}), 201

@main_bp.route('/api/patients', methods=['GET', 'POST'])
def manage_patients():
    if request.method == 'GET':
        patients = Patient.query.all()
        return jsonify([{
            'id': p.id, 
            'name': p.name, 
            'age': p.age,
            'gender': p.gender, 
            'hospital_id': p.hospital_id
        } for p in patients])
    elif request.method == 'POST':
        data = request.json
        new_patient = Patient(
            name=data['name'], 
            age=data['age'],
            gender=data['gender'], 
            hospital_id=data['hospital_id']
        )
        db.session.add(new_patient)
        db.session.commit()
        socketio.emit('patient_update', {
            'id': new_patient.id, 
            'name': new_patient.name, 
            'hospital_id': new_patient.hospital_id
        }, namespace='/socket')
        return jsonify({'message': 'Patient registered successfully', 'id': new_patient.id}), 201

@main_bp.route('/api/opd/queue', methods=['GET', 'POST'])
def manage_opd_queue():
    if request.method == 'GET':
        hospital_id = request.args.get('hospital_id')
        queues = OPDQueue.query.filter_by(hospital_id=hospital_id, status='Waiting').order_by(OPDQueue.timestamp).all()
        queue_data = [{
            'id': q.id,
            'patient_id': q.patient_id,
            'queue_number': q.id,
            'wait_time': (datetime.utcnow() - q.timestamp).total_seconds() // 60
        } for q in queues]
        return jsonify({
            'queue': queue_data,
            'queue_start_time': queues[0].timestamp.isoformat() if queues else None,
            'estimated_wait_time': len(queues) * 15,  # Assuming 15 minutes per patient
            'patients_queuing': len(queues)
        })
    elif request.method == 'POST':
        data = request.json
        new_queue_entry = OPDQueue(patient_id=data['patient_id'], hospital_id=data['hospital_id'])
        db.session.add(new_queue_entry)
        db.session.commit()
        socketio.emit('queue_update', {
            'queue_number': new_queue_entry.id,
            'hospital_id': data['hospital_id'],
            'patients_queuing': OPDQueue.query.filter_by(hospital_id=data['hospital_id'], status='Waiting').count()
        }, namespace='/socket')
        return jsonify({'message': 'Added to OPD queue', 'queue_number': new_queue_entry.id}), 201

@main_bp.route('/api/beds/<int:hospital_id>', methods=['PUT'])
def update_beds(hospital_id):
    hospital = Hospital.query.get_or_404(hospital_id)
    data = request.json
    hospital.available_beds = data['available_beds']
    db.session.commit()
    socketio.emit('bed_update', {'hospital_id': hospital_id, 'available_beds': hospital.available_beds}, namespace='/socket')
    return jsonify({'message': 'Bed availability updated successfully'})

@main_bp.route('/api/inventory/<int:hospital_id>', methods=['GET', 'POST'])
def manage_inventory(hospital_id):
    if request.method == 'GET':
        inventory = Inventory.query.filter_by(hospital_id=hospital_id).all()
        return jsonify([{'item': item.item_name, 'quantity': item.quantity, 'unit_price': item.unit_price} for item in inventory])
    elif request.method == 'POST':
        data = request.json
        item = Inventory.query.filter_by(hospital_id=hospital_id, item_name=data['item_name']).first()
        if item:
            item.quantity += data['quantity']
            item.unit_price = data['unit_price']
        else:
            item = Inventory(hospital_id=hospital_id, item_name=data['item_name'], quantity=data['quantity'], unit_price=data['unit_price'])
            db.session.add(item)
        db.session.commit()
        socketio.emit('inventory_update', {
            'hospital_id': hospital_id, 
            'item': data['item_name'], 
            'quantity': item.quantity, 
            'unit_price': item.unit_price
        }, namespace='/socket')
        return jsonify({'message': 'Inventory updated successfully'}), 200

@main_bp.route('/api/expenses/<int:hospital_id>', methods=['GET', 'POST'])
def manage_expenses(hospital_id):
    if request.method == 'GET':
        expenses = Expense.query.filter_by(hospital_id=hospital_id).all()
        return jsonify([{
            'id': e.id, 
            'description': e.description, 
            'amount': e.amount, 
            'date': e.date.isoformat()
        } for e in expenses])
    elif request.method == 'POST':
        data = request.json
        new_expense = Expense(
            hospital_id=hospital_id, 
            description=data['description'], 
            amount=data['amount'], 
            date=datetime.strptime(data['date'], '%Y-%m-%d').date()
        )
        db.session.add(new_expense)
        db.session.commit()
        socketio.emit('expense_update', {
            'hospital_id': hospital_id, 
            'expense_id': new_expense.id, 
            'amount': new_expense.amount
        }, namespace='/socket')
        return jsonify({'message': 'Expense added successfully', 'id': new_expense.id}), 201

@main_bp.route('/api/opd/queue/history')
def get_queue_history():
    hospital_id = request.args.get('hospital_id', 1, type=int)
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=24)
    
    queue_history = db.session.query(
        OPDQueue.timestamp,
        db.func.count(OPDQueue.id).label('queue_length')
    ).filter(
        OPDQueue.hospital_id == hospital_id,
        OPDQueue.timestamp.between(start_time, end_time)
    ).group_by(
        db.func.strftime('%Y-%m-%d %H:00:00', OPDQueue.timestamp)
    ).order_by(OPDQueue.timestamp).all()
    
    return jsonify([
        {'timestamp': entry.timestamp.isoformat(), 'length': entry.queue_length}
        for entry in queue_history
    ])

@socketio.on('connect', namespace='/socket')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect', namespace='/socket')
def handle_disconnect():
    print('Client disconnected')
