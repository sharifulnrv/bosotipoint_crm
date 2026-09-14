"""
run.py — Project Root Local Development Server Wrapper
Run with: python run.py
(NOT for production — use backend/passenger_wsgi.py or backend/wsgi.py instead)
"""

import os
import sys

# Add the backend directory to Python path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend")
sys.path.insert(0, BACKEND_DIR)

from dotenv import load_dotenv

# Load .env from project root
load_dotenv(os.path.join(PROJECT_ROOT, '.env'))
# Also try loading from backend/.env just in case
load_dotenv(os.path.join(BACKEND_DIR, '.env'))

from app import create_app

app = create_app(os.environ.get('FLASK_CONFIG', 'development'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # use_reloader=False prevents APScheduler jobs from running twice in dev
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)
