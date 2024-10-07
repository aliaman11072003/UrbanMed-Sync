from backend.extensions import db
from backend.app import create_app  # Import create_app from app.py
from backend.models import User, Department, Patient, Doctor, Bed, Inventory, City, Hospital, OPDQueue

def init_db():
    app = create_app()  # Create an instance of your Flask app
    with app.app_context():  # Push the application context
        try:
            db.drop_all()  # Uncomment this line if you want to drop all tables before creating them
            db.create_all()
            
            # Add cities
            cities = ['Kanpur', 'Lucknow', 'Delhi', 'Noida', 'New York', 'Los Angeles', 'Chicago', 'Houston']
            for city_name in cities:
                if not City.query.filter_by(name=city_name).first():
                    db.session.add(City(name=city_name))
            db.session.commit()

            # Add hospitals
            hospitals = [
                {'name': 'Central Hospital', 'address': '123 Main St', 'total_beds': 200, 'available_beds': 50, 'city': 'Kanpur'},
                {'name': 'West Medical Center', 'address': '456 Oak Ave', 'total_beds': 150, 'available_beds': 30, 'city': 'Lucknow'},
            ]
            for hospital in hospitals:
                city = City.query.filter_by(name=hospital['city']).first()
                if city and not Hospital.query.filter_by(name=hospital['name']).first():
                    db.session.add(Hospital(name=hospital['name'], address=hospital['address'], 
                                            total_beds=hospital['total_beds'], available_beds=hospital['available_beds'], 
                                            city_id=city.id))
            db.session.commit()

            # Add departments
            departments = ['Emergency', 'Cardiology', 'Pediatrics', 'Orthopedics']
            for dept_name in departments:
                if not Department.query.filter_by(name=dept_name).first():
                    db.session.add(Department(name=dept_name))
            db.session.commit()
            
            # Add doctors
            doctors = [
                {'name': 'Dr. Smith', 'department': 'Emergency'},
                {'name': 'Dr. Johnson', 'department': 'Cardiology'},
                {'name': 'Dr. Williams', 'department': 'Pediatrics'},
                {'name': 'Dr. Brown', 'department': 'Orthopedics'}
            ]
            for doc in doctors:
                dept = Department.query.filter_by(name=doc['department']).first()
                if dept and not Doctor.query.filter_by(name=doc['name']).first():
                    db.session.add(Doctor(name=doc['name'], department_id=dept.id))
            db.session.commit()
            
            # Add beds
            departments = Department.query.all()  # Fetch all departments
            hospital = Hospital.query.first()  # Assuming we're adding beds to the first hospital
            if hospital and departments:
                for dept in departments:
                    for i in range(1, 11):  # Assuming 10 beds per department
                        bed = Bed(bed_number=f"Bed-{dept.name}-{i}", department_id=dept.id)
                        db.session.add(bed)
                db.session.commit()
            
            # Add inventory items
            inventory_items = [
                {'item_name': 'Paracetamol', 'quantity': 1000, 'unit_price': 0.5},
                {'item_name': 'Bandages', 'quantity': 500, 'unit_price': 1.0},
                {'item_name': 'Syringes', 'quantity': 200, 'unit_price': 0.75}
            ]
            if hospital:
                for item in inventory_items:
                    if not Inventory.query.filter_by(hospital_id=hospital.id, item_name=item['item_name']).first():
                        db.session.add(Inventory(hospital_id=hospital.id, **item))
                db.session.commit()

            print("Database initialized successfully.")
        
        except Exception as e:
            db.session.rollback()  # Rollback the session in case of error
            print(f"An error occurred: {e}")

if __name__ == '__main__':
    init_db()
