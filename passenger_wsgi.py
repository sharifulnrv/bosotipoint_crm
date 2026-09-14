"""
passenger_wsgi.py — cPanel Entry Point
=======================================
This file is used by cPanel's Passenger/WSGI to start the Flask app.
"""

import sys
import os

# Add the root directory to Python path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

# Add the backend directory to Python path
BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend")
sys.path.insert(0, BACKEND_DIR)

# Load .env file from root
from dotenv import load_dotenv
load_dotenv(os.path.join(PROJECT_ROOT, '.env'))

# Set the Flask config to production
os.environ.setdefault('FLASK_CONFIG', 'production')

# Import and create the app from backend
from app import create_app
application = create_app('production')
