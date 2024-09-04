from flask import Flask, jsonify, request, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os
import logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital_system.db'
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)

# Database models
class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    beds = db.Column(db.Integer, default=0)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'))

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'))
    status = db.Column(db.String(20), default='Waiting')

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    app.logger.debug("Rendering index.html")
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        hospital_id = request.form['hospital_id']
        
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, role=role, hospital_id=hospital_id)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    if user.role == 'staff':
        hospitals = Hospital.query.all()
        return render_template('dashboard.html', user=user, hospitals=hospitals)
    elif user.role == 'doctor':
        patients = Patient.query.filter_by(hospital_id=user.hospital_id).all()
        return render_template('dashboard.html', user=user, patients=patients)
    else:
        return render_template('dashboard.html', user=user)

@app.route('/api/hospital', methods=['POST'])
@login_required
def create_hospital():
    data = request.form
    new_hospital = Hospital(name=data['name'], beds=data['beds'])
    db.session.add(new_hospital)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/api/patient', methods=['POST'])
@login_required
def add_patient():
    data = request.form
    new_patient = Patient(name=data['name'], hospital_id=data['hospital_id'])
    db.session.add(new_patient)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/api/update_patient_status', methods=['POST'])
@login_required
def update_patient_status():
    data = request.form
    patient = Patient.query.get(data['patient_id'])
    if patient:
        patient.status = data['status']
        db.session.commit()
    return redirect(url_for('dashboard'))

# Add this block to create test users
def create_test_users():
    with app.app_context():
        if User.query.filter_by(username='teststaff').first() is None:
            test_staff = User(username='teststaff', 
                              password=generate_password_hash('staffpass'),
                              role='staff',
                              hospital_id=1)
            db.session.add(test_staff)
            
        if User.query.filter_by(username='testdoctor').first() is None:
            test_doctor = User(username='testdoctor', 
                               password=generate_password_hash('doctorpass'),
                               role='doctor',
                               hospital_id=1)
            db.session.add(test_doctor)
            
        if User.query.filter_by(username='testpatient').first() is None:
            test_patient = User(username='testpatient', 
                                password=generate_password_hash('patientpass'),
                                role='patient',
                                hospital_id=1)
            db.session.add(test_patient)
        
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This will create any new tables if models have changed
        create_test_users()  # This will add test users if they don't exist
    app.run(debug=True)