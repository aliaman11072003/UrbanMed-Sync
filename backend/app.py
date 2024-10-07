from __future__ import annotations
import os
import math
import logging
import numpy as np
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from queue import PriorityQueue
from dataclasses import dataclass

from flask import Flask, send_from_directory, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from werkzeug.exceptions import HTTPException
from marshmallow import Schema, fields, validate
from sqlalchemy import func
from sqlalchemy.orm import Mapped, relationship

from backend.extensions import db
from backend.models import User, Department, Patient, Doctor, Bed, Inventory, City, Hospital, OPDQueue, Expense, Medicine

# Create the Flask application
def create_app():
    app = Flask(__name__, static_folder='../frontend/build/static', static_url_path='/static')  # Adjust if needed
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///swasthyaflow.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'your_secret_key_here'

    db.init_app(app)
    socketio = SocketIO(app, cors_allowed_origins="*")  # Create an instance of SocketIO
    CORS(app)

    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Thread pool for concurrent processing
    thread_pool = ThreadPoolExecutor(max_workers=4)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/login', methods=['POST'])
    def login():
        data = request.json
        user = User.query.filter_by(username=data['username']).first()
        if user and check_password_hash(user.password, data['password']):
            login_user(user)
            return jsonify({'message': 'Logged in successfully'})
        return jsonify({'error': 'Invalid username or password'}), 401

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return jsonify({'message': 'Logged out successfully'})

    # Example of a protected route
    @app.route('/api/staff_only')
    @login_required
    def staff_only():
        if not current_user.is_staff:
            return jsonify({'error': 'Access denied'}), 403
        return jsonify({'message': 'Welcome, staff member!'})

    class QueuingModel:
        def __init__(self, num_doctors: int, num_beds: int, arrival_rate: float, service_rate: float):
            self.num_doctors = num_doctors
            self.num_beds = num_beds
            self.arrival_rate = arrival_rate
            self.service_rate = service_rate

        def calculate_wait_time(self) -> float:
            rho = self.arrival_rate / (self.num_doctors * self.service_rate)
            if rho >= 1:
                return float('inf')  # System is unstable
            
            p0 = 1 / (sum([
                (self.num_doctors * rho) ** n / math.factorial(n)
                for n in range(self.num_doctors)
            ]) + (self.num_doctors * rho) ** self.num_doctors / (
                math.factorial(self.num_doctors) * (1 - rho)
            ))
            
            lq = (p0 * (self.num_doctors * rho) ** self.num_doctors * rho) / (
                math.factorial(self.num_doctors) * (1 - rho) ** 2
            )
            
            wq = lq / self.arrival_rate
            return wq * 60  # Convert to minutes

        def calculate_utilization(self) -> float:
            return self.arrival_rate / (self.num_doctors * self.service_rate)

        def calculate_probability_of_waiting(self) -> float:
            rho = self.arrival_rate / (self.num_doctors * self.service_rate)
            if rho >= 1:
                return 1.0  # System is unstable
            
            p0 = 1 / (sum([
                (self.num_doctors * rho) ** n / math.factorial(n)
                for n in range(self.num_doctors)
            ]) + (self.num_doctors * rho) ** self.num_doctors / (
                math.factorial(self.num_doctors) * (1 - rho)
            ))
            
            return (self.num_doctors * rho) ** self.num_doctors * p0 / (
                math.factorial(self.num_doctors) * (1 - rho)
            )

    @app.route('/api/queue_data')
    def get_queue_data() -> Dict[str, Any]:
        """API endpoint to get queue data for all departments."""
        departments = db.session.execute(db.select(Department)).scalars().all()
        queue_data = []

        for dept in departments:
            num_doctors = db.session.execute(db.select(func.count(Doctor.id)).filter_by(department_id=dept.id, is_available=True)).scalar()
            patients = db.session.execute(db.select(Patient).filter_by(department_id=dept.id, status='Waiting')).scalars().all()
            num_patients = len(patients)
            
            if num_doctors > 0 and num_patients > 0:
                arrival_times = [p.arrival_time for p in patients]
                arrival_intervals = np.diff([t.timestamp() for t in arrival_times])
                arrival_rate = 1 / np.mean(arrival_intervals) if len(arrival_intervals) > 0 else 0
                
                service_rate = 1 / 15  # Assume average service time of 15 minutes
                
                model = QueuingModel(num_doctors, 0, arrival_rate, service_rate)
                wait_time = model.calculate_wait_time()
                utilization = model.calculate_utilization()
                prob_of_waiting = model.calculate_probability_of_waiting()
            else:
                wait_time = 0
                utilization = 0
                prob_of_waiting = 0

            queue_data.append({
                'department': dept.name,
                'waiting_patients': num_patients,
                'available_doctors': num_doctors,
                'estimated_wait_time': round(wait_time, 2),
                'utilization': round(utilization, 2),
                'probability_of_waiting': round(prob_of_waiting, 2)
            })

        return jsonify(queue_data)

    def simple_trend(x, y):
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(x[i] * y[i] for i in range(n))
        sum_xx = sum(x[i] ** 2 for i in range(n))
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x ** 2)
        return slope

    @app.route('/api/patient_flow')
    def get_patient_flow() -> Dict[str, Any]:
        """API endpoint to get patient flow data for the last 7 days."""
        start_date = datetime.utcnow() - timedelta(days=7)
        patients = db.session.execute(db.select(Patient).filter(Patient.arrival_time >= start_date)).scalars().all()

        daily_flow = defaultdict(lambda: defaultdict(int))
        for patient in patients:
            day = patient.arrival_time.date()
            dept = db.session.get(Department, patient.department_id).name
            daily_flow[str(day)][dept] += 1

        # Calculate statistics
        dept_totals = defaultdict(list)
        for day_data in daily_flow.values():
            for dept, count in day_data.items():
                dept_totals[dept].append(count)

        statistics = {}
        for dept, counts in dept_totals.items():
            statistics[dept] = {
                'mean': sum(counts) / len(counts),
                'median': sorted(counts)[len(counts) // 2],
                'std_dev': (sum((x - (sum(counts) / len(counts))) ** 2 for x in counts) / len(counts)) ** 0.5,
                'min': min(counts),
                'max': max(counts),
                'trend': simple_trend(range(len(counts)), counts)
            }

        return jsonify({
            'daily_flow': dict(daily_flow),
            'statistics': statistics
        })

    @app.route('/api/update_inventory', methods=['POST'])
    def update_inventory() -> Dict[str, Any]:
        """API endpoint to update inventory."""
        data = request.json
        medicine_count = data.get('medicines')
        consumables_count = data.get('consumables')
        
        inventory = db.session.execute(db.select(Inventory).limit(1)).scalar_one_or_none()
        if inventory:
            inventory.medicines = medicine_count
            inventory.consumables = consumables_count
            db.session.commit()
            return jsonify({"message": "Inventory updated successfully"}), 200
        else:
            return jsonify({"error": "Inventory not found"}), 404

    @socketio.on('connect')
    def handle_connect():
        """Handle new WebSocket connections."""
        logger.info("New client connected")
        emit_updates()

    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle WebSocket disconnections."""
        logger.info("Client disconnected")

    @socketio.on('new_patient')
    def handle_new_patient(data: Dict[str, Any]):
        """Handle new patient arrival."""
        try:
            thread_pool.submit(process_new_patient, data)
        except Exception as e:
            logger.error(f"Error submitting new patient task: {str(e)}")
            socketio.emit('error', {'message': 'Failed to process new patient'})

    def process_new_patient(data: Dict[str, Any]):
        """Process new patient data in a separate thread."""
        try:
            with app.app_context():
                patient = Patient(name=data['name'], department_id=data['department_id'])
                db.session.add(patient)
                db.session.commit()

                queue = db.session.execute(db.select(OPDQueue).order_by(OPDQueue.id.desc()).limit(1)).scalar_one_or_none()
                if queue:
                    queue.length += 1
                else:
                    queue = OPDQueue(length=1)
                db.session.add(queue)
                db.session.commit()

                update_wait_times()
                socketio.emit('patient_added', {'name': patient.name, 'department': patient.department.name})
        except Exception as e:
            logger.error(f"Error processing new patient: {str(e)}")
            socketio.emit('error', {'message': 'Failed to add new patient'})

    @socketio.on('update_bed_status')
    def handle_bed_status(data: Dict[str, Any]):
        """Handle bed status update."""
        thread_pool.submit(process_bed_status_update, data)

    def process_bed_status_update(data: Dict[str, Any]):
        """Process bed status update in a separate thread."""
        try:
            bed = db.session.execute(db.select(Bed).limit(1)).scalar_one_or_none()
            if bed:
                bed.available = data['available']
                db.session.commit()
                socketio.emit('bed_status_updated', {'available': bed.available, 'occupied': bed.total - bed.available}, broadcast=True)
        except Exception as e:
            logger.error(f"Error updating bed status: {str(e)}")
            db.session.rollback()

    def emit_updates():
        """Emit updates to all connected clients."""
        try:
            queue = db.session.execute(db.select(OPDQueue).order_by(OPDQueue.id.desc()).limit(1)).scalar_one_or_none()
            bed = db.session.execute(db.select(Bed).limit(1)).scalar_one_or_none()
            inventory = db.session.execute(db.select(Inventory).limit(1)).scalar_one_or_none()
            
            socketio.emit('queue_update', {'length': queue.length if queue else 0})
            socketio.emit('bed_update', {'available': bed.available if bed else 0})
            socketio.emit('inventory_update', {
                'medicines': inventory.medicines if inventory else 0,
                'consumables': inventory.consumables if inventory else 0
            })
        except Exception as e:
            logger.error(f"Error emitting updates: {str(e)}")

    def update_wait_times():
        """Recalculate and broadcast updated wait times."""
        try:
            departments = db.session.execute(db.select(Department)).scalars().all()
            for dept in departments:
                num_doctors = db.session.execute(db.select(func.count(Doctor.id)).filter_by(department_id=dept.id, is_available=True)).scalar()
                num_patients = db.session.execute(db.select(func.count(Patient.id)).filter_by(department_id=dept.id, status='Waiting')).scalar()
                
                if num_doctors > 0:
                    arrival_rate = num_patients / 60  # Assume patients arrived over the last hour
                    service_rate = 1 / 15  # Assume average service time of 15 minutes
                    
                    model = QueuingModel(num_doctors, 0, arrival_rate, service_rate)
                    wait_time = model.calculate_wait_time()
                    
                    socketio.emit('wait_time_updated', {'department': dept.name, 'wait_time': round(wait_time, 2)})
        except Exception as e:
            logger.error(f"Error updating wait times: {str(e)}")

    @app.route('/api/bed_availability')
    def get_bed_availability():
        beds = Bed.query.all()
        availability = {
            'total': len(beds),
            'available': sum(1 for bed in beds if bed.is_available),
            'occupied': sum(1 for bed in beds if not bed.is_available)
        }
        return jsonify(availability)

    @app.route('/api/allocate_bed', methods=['POST'])
    def allocate_bed():
        data = request.json
        patient_id = data['patient_id']
        department_id = data['department_id']
        
        available_bed = Bed.query.filter_by(department_id=department_id, is_available=True).first()
        if not available_bed:
            return jsonify({'error': 'No beds available in the selected department'}), 400
        
        available_bed.is_available = False
        patient = Patient.query.get(patient_id)
        patient.bed_id = available_bed.id
        db.session.commit()
        
        return jsonify({'message': 'Bed allocated successfully', 'bed_number': available_bed.bed_number})

    class PatientSchema(Schema):
        name = fields.Str(required=True)
        age = fields.Int(required=True)
        gender = fields.Str(required=True)

    patient_schema = PatientSchema()

    @app.route('/api/admit_patient', methods=['POST'])
    @login_required
    def admit_patient():
        data = request.json
        errors = patient_schema.validate(data)
        if errors:
            return jsonify(errors), 400
        
        patient = Patient(name=data['name'], age=data['age'], gender=data['gender'])
        db.session.add(patient)
        db.session.commit()
        
        # Allocate bed
        available_bed = Bed.query.filter_by(is_available=True).first()
        if available_bed:
            available_bed.is_available = False
            available_bed.patient_id = patient.id
            db.session.commit()
        
        return jsonify({"message": "Patient admitted successfully", "patient_id": patient.id}), 201

    @app.route('/api/generate_bill/<int:patient_id>')
    def generate_bill(patient_id):
        patient = Patient.query.get_or_404(patient_id)
        
        if not patient.bed:
            return jsonify({'error': 'Patient not currently admitted'}), 400
        
        # Calculate bill (this is a simple example, you'd need to implement your own billing logic)
        days_admitted = (datetime.utcnow() - patient.admission_date).days
        daily_rate = 1000  # Example daily rate
        total_bill = days_admitted * daily_rate
        
        return jsonify({
            'patient_name': patient.name,
            'days_admitted': days_admitted,
            'total_bill': total_bill
        })

    @app.route('/api/join_queue', methods=['POST'])
    def join_queue():
        data = request.json
        department = Department.query.get_or_404(data['department_id'])
        patient = Patient.query.get_or_404(data['patient_id'])
        
        last_queue = OPDQueue.query.filter_by(department_id=department.id).order_by(OPDQueue.sequence_number.desc()).first()
        sequence_number = (last_queue.sequence_number + 1) if last_queue else 1
        
        # Estimate wait time (simple example, you'd need to implement your own logic)
        estimated_time = datetime.utcnow() + timedelta(minutes=15 * sequence_number)
        
        queue_entry = OPDQueue(
            department_id=department.id,
            patient_id=patient.id,
            sequence_number=sequence_number,
            estimated_time=estimated_time
        )
        db.session.add(queue_entry)
        db.session.commit()
        
        return jsonify({
            'message': 'Joined queue successfully',
            'sequence_number': sequence_number,
            'estimated_time': estimated_time.isoformat()
        })

    @app.route('/api/queue_status/<int:department_id>')
    def queue_status(department_id):
        queue = OPDQueue.query.filter_by(department_id=department_id, status='Waiting').order_by(OPDQueue.sequence_number).all()
        return jsonify([{
            'patient_name': q.patient.name,
            'sequence_number': q.sequence_number,
            'estimated_time': q.estimated_time.isoformat()
        } for q in queue])

    def get_patient_flow_data():
        # Implement your logic to get patient flow data
        # This is just a placeholder
        return {"labels": ["Mon", "Tue", "Wed"], "data": [10, 15, 8]}

    def get_bed_occupancy_data():
        # Implement your logic to get bed occupancy data
        # This is just a placeholder
        return {"labels": ["ICU", "General", "Emergency"], "data": [80, 60, 40]}

    @app.route('/api/analytics/patient_flow')
    @login_required
    def patient_flow_analytics():
        patient_flow_data = get_patient_flow_data()
        return jsonify({"data": patient_flow_data}), 200

    @app.route('/api/analytics/bed_occupancy')
    @login_required
    def bed_occupancy_analytics():
        bed_occupancy_data = get_bed_occupancy_data()
        return jsonify({"data": bed_occupancy_data}), 200

    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return jsonify(error=str(e)), e.code
        return jsonify(error="An unexpected error occurred"), 500

    class PriorityPatientQueue:
        def __init__(self):
            self.queue = PriorityQueue()
            self.order = 0

        def add_patient(self, patient, priority):
            self.order += 1
            self.queue.put((priority, self.order, patient))

        def get_next_patient(self):
            if not self.queue.empty():
                return self.queue.get()[2]
            return None

    patient_queue = PriorityPatientQueue()

    @app.route('/api/queue/add', methods=['POST'])
    @login_required
    def add_to_queue():
        data = request.json
        patient = Patient.query.get(data['patient_id'])
        priority = data['priority']
        patient_queue.add_patient(patient, priority)
        return jsonify({"message": "Patient added to queue"}), 200

    @app.route('/api/queue/next')
    @login_required
    def get_next_patient():
        patient = patient_queue.get_next_patient()
        if patient:
            return jsonify({"patient_id": patient.id, "name": patient.name}), 200
        return jsonify({"message": "Queue is empty"}), 404

    @app.route('/api/check_login')
    def check_login():
        if current_user.is_authenticated:
            return jsonify({'user': {'id': current_user.id, 'username': current_user.username, 'role': current_user.role}})
        return jsonify({'user': None}), 401

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            # Serve index.html from the public folder
            return send_from_directory('../frontend/public', 'index.html')

    @app.errorhandler(404)
    def not_found(e):
        return send_from_directory('../frontend/public', 'index.html')

    @app.route('/api/expenses', methods=['POST'])
    @login_required
    def create_expense():
        data = request.json
        new_expense = Expense(
            hospital_id=data['hospital_id'],
            description=data['description'],
            amount=data['amount'],
            date=datetime.strptime(data['date'], '%Y-%m-%d').date() if 'date' in data else None
        )
        db.session.add(new_expense)
        db.session.commit()
        return jsonify({'message': 'Expense created successfully', 'id': new_expense.id}), 201

    @app.route('/api/expenses', methods=['GET'])
    @login_required
    def get_expenses():
        expenses = Expense.query.all()
        return jsonify([{
            'id': e.id,
            'hospital_id': e.hospital_id,
            'description': e.description,
            'amount': e.amount,
            'date': e.date.isoformat()
        } for e in expenses]), 200

    return app, socketio

# Create an instance of your Flask app and socketio
app, socketio = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True)
