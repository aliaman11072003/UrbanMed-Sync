from backend.extensions import db
from flask_login import UserMixin
from sqlalchemy.orm import Mapped, relationship
from datetime import datetime
from typing import List, Optional

class City(db.Model):
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    name: Mapped[str] = db.Column(db.String(100), nullable=False)
    hospitals: Mapped[List["Hospital"]] = relationship('Hospital', backref='city', lazy=True)

class Hospital(db.Model):
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    name: Mapped[str] = db.Column(db.String(100), nullable=False)
    address: Mapped[str] = db.Column(db.String(200))
    total_beds: Mapped[int] = db.Column(db.Integer, default=0)
    available_beds: Mapped[int] = db.Column(db.Integer, default=0)
    city_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    patients: Mapped[List["Patient"]] = relationship('Patient', backref='hospital', lazy=True)
    opd_queues: Mapped[List["OPDQueue"]] = relationship('OPDQueue', backref='hospital', lazy=True)
    inventories: Mapped[List["Inventory"]] = relationship('Inventory', backref='hospital', lazy=True)
    expenses: Mapped[List["Expense"]] = relationship('Expense', backref='hospital', lazy=True)
    medicines: Mapped[List["Medicine"]] = relationship("Medicine", back_populates="hospital")

class Patient(db.Model):
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    name: Mapped[str] = db.Column(db.String(100), nullable=False)
    age: Mapped[int] = db.Column(db.Integer)
    gender: Mapped[str] = db.Column(db.String(10))
    hospital_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)
    department_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    opd_queues: Mapped[List["OPDQueue"]] = relationship('OPDQueue', backref='patient', lazy=True)

class OPDQueue(db.Model):
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    patient_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    hospital_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)
    timestamp: Mapped[datetime] = db.Column(db.DateTime, default=datetime.utcnow)
    status: Mapped[str] = db.Column(db.String(20), default='Waiting')

class Inventory(db.Model):
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    hospital_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)
    item_name: Mapped[str] = db.Column(db.String(100), nullable=False)
    quantity: Mapped[int] = db.Column(db.Integer, default=0)
    unit_price: Mapped[float] = db.Column(db.Float, default=0.0)

class Expense(db.Model):
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    hospital_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)
    description: Mapped[str] = db.Column(db.String(200), nullable=False)
    amount: Mapped[float] = db.Column(db.Float, nullable=False)
    date: Mapped[datetime] = db.Column(db.Date, default=datetime.utcnow().date)

class User(UserMixin, db.Model):
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    username: Mapped[str] = db.Column(db.String(80), unique=True, nullable=False)
    password: Mapped[str] = db.Column(db.String(120), nullable=False)
    role: Mapped[str] = db.Column(db.String(20), nullable=False)

class Department(db.Model):
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    name: Mapped[str] = db.Column(db.String(50), unique=True, nullable=False)
    patients: Mapped[List["Patient"]] = relationship('Patient', backref='department', lazy='dynamic')
    doctors: Mapped[List["Doctor"]] = relationship('Doctor', backref='department', lazy='dynamic')

class Doctor(db.Model):
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    name: Mapped[str] = db.Column(db.String(100), nullable=False)
    department_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    is_available: Mapped[bool] = db.Column(db.Boolean, default=True, index=True)

class Bed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bed_number = db.Column(db.String(50), nullable=False)  # Change this line
    is_available = db.Column(db.Boolean, default=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)

class Medicine(db.Model):
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    name: Mapped[str] = db.Column(db.String(100), nullable=False)
    quantity: Mapped[int] = db.Column(db.Integer, default=0)
    unit: Mapped[str] = db.Column(db.String(20), nullable=False)
    hospital_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)
    hospital: Mapped["Hospital"] = relationship("Hospital", back_populates="medicines")
    
# You can remove the Queue model as it's replaced by OPDQueue

# Add other model classes as needed
