import sys
import os
import shutil
from backend.app import app, socketio, create_app  # Ensure this imports socketio correctly
from backend.database import init_db  # Import the init_db function from database.py
from backend.extensions import db  # Import db from extensions.py

# Add the backend directory to the Python path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.append(backend_dir)

# Copy contents of frontend/build to backend/static 
frontend_build = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend', 'build')
if os.path.exists(frontend_build):
    # You can keep this if you want to copy build files to a specific location
    for item in os.listdir(frontend_build):
        s = os.path.join(frontend_build, item)
        
        d = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend', 'build', item)  # Adjust as needed
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)
    print(f"Copied frontend build files to {frontend_build}")
else:
    print(f"Frontend build directory not found: {frontend_build}")

if __name__ == '__main__':
    print("Current working directory:", os.getcwd())
    
    print("Files in frontend build directory:", os.listdir(frontend_build))
    print("Index.html exists:", os.path.exists(os.path.join(frontend_build, 'index.html')))

    app, socketio = create_app()  # Ensure this is correct

    with app.app_context():  # This should work now
        db.create_all()  # This creates the database tables
        try:
            init_db()  # Call the init_db function from database.py
            print("Database initialized successfully")
        except Exception as e:
            print(f"An error occurred while initializing the database: {str(e)}")
    
    print("Starting Flask server...")
    print("Server running on http://localhost:5000")
    socketio.run(app, debug=True)  # Start the application with socketio

    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule.rule}")