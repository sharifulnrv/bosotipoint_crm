"""
reset_db.py — Root Level Database Reset Wrapper
Run with: python reset_db.py
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
load_dotenv(os.path.join(BACKEND_DIR, '.env'))

def confirm_reset():
    print("=" * 60)
    print("WARNING: DANGEROUS OPERATION")
    print("=" * 60)
    print("You are about to DROP ALL TABLES and recreate the database.")
    print("This will PERMANENTLY DELETE all leads, users, and settings.")
    print("=" * 60)
    
    first = input("Are you ABSOLUTELY sure you want to proceed? (yes/no): ")
    if first.lower() != 'yes':
        print("Operation cancelled.")
        sys.exit(0)
        
    second = input("Type 'RESET' to confirm: ")
    if second != 'RESET':
        print("Operation cancelled.")
        sys.exit(0)

if __name__ == '__main__':
    confirm_reset()
    
    # Import and run the backend reset_db logic
    try:
        # Import the reset_db script from backend and run it by importing
        # This allows us to keep the actual logic in one place
        sys.path.insert(0, BACKEND_DIR)
        
        # We need to run it as a script, so let's execute the file
        reset_script = os.path.join(BACKEND_DIR, "reset_db.py")
        print(f"Running backend script: {reset_script}")
        
        # Create a subprocess to run the backend reset_db.py so it runs correctly
        import subprocess
        result = subprocess.run([sys.executable, reset_script], cwd=BACKEND_DIR)
        sys.exit(result.returncode)
    except Exception as e:
        print(f"Error resetting database: {e}")
        sys.exit(1)
