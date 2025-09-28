#!/usr/bin/env python3
"""
WSGI entry point for NSAKCET College Chatbot
Production-ready server configuration
"""

import os
import sys
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

# Import the Flask app
from app import app

# Configure for production
if __name__ == "__main__":
    # Production configuration
    app.config['DEBUG'] = False
    app.config['TESTING'] = False
    
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app
    app.run(host='0.0.0.0', port=port)
