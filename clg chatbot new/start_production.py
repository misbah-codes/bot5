#!/usr/bin/env python3
"""
Production startup script for NSAKCET College Chatbot
This script provides multiple options for running the app in production
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import flask
        import nltk
        import sklearn
        import numpy
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Installing dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            return False

def run_with_gunicorn(host="0.0.0.0", port=5000, workers=None):
    """Run the app using Gunicorn (recommended for production)"""
    if not check_dependencies():
        return False
    
    # Download NLTK data
    try:
        import nltk
        print("📥 Downloading NLTK data...")
        nltk.download('punkt', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('omw-1.4', quiet=True)
        print("✅ NLTK data ready")
    except Exception as e:
        print(f"⚠️ Warning: Could not download NLTK data: {e}")
    
    # Set environment variables
    os.environ['FLASK_ENV'] = 'production'
    os.environ['FLASK_DEBUG'] = 'False'
    
    # Build gunicorn command
    cmd = [
        'gunicorn',
        '--config', 'gunicorn.conf.py',
        '--bind', f'{host}:{port}',
        'wsgi:app'
    ]
    
    if workers:
        cmd.extend(['--workers', str(workers)])
    
    print(f"🚀 Starting NSAKCET Chatbot with Gunicorn on {host}:{port}")
    print("=" * 60)
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 Chatbot stopped. Goodbye!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting Gunicorn: {e}")
        return False
    
    return True

def run_with_waitress(host="0.0.0.0", port=5000):
    """Run the app using Waitress (Windows-compatible)"""
    if not check_dependencies():
        return False
    
    try:
        from waitress import serve
        from wsgi import app
        
        print(f"🚀 Starting NSAKCET Chatbot with Waitress on {host}:{port}")
        print("=" * 60)
        
        serve(app, host=host, port=port)
        
    except ImportError:
        print("❌ Waitress not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "waitress"])
        from waitress import serve
        from wsgi import app
        serve(app, host=host, port=port)
    except KeyboardInterrupt:
        print("\n👋 Chatbot stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error starting Waitress: {e}")
        return False
    
    return True

def run_development(host="127.0.0.1", port=5000):
    """Run the app in development mode (with warnings)"""
    if not check_dependencies():
        return False
    
    try:
        from app import app
        
        print(f"🚀 Starting NSAKCET Chatbot in DEVELOPMENT mode on {host}:{port}")
        print("⚠️  WARNING: This is a development server. Not suitable for production!")
        print("=" * 60)
        
        app.run(debug=True, host=host, port=port)
        
    except KeyboardInterrupt:
        print("\n👋 Chatbot stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error starting development server: {e}")
        return False
    
    return True

def main():
    """Main function with command line argument parsing"""
    parser = argparse.ArgumentParser(description='NSAKCET College Chatbot - Production Server')
    parser.add_argument('--server', choices=['gunicorn', 'waitress', 'dev'], 
                       default='gunicorn', help='Server type to use')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to')
    parser.add_argument('--workers', type=int, help='Number of worker processes (Gunicorn only)')
    
    args = parser.parse_args()
    
    print("🏛️ NSAKCET College Chatbot - Production Server")
    print("=" * 50)
    
    if args.server == 'gunicorn':
        success = run_with_gunicorn(args.host, args.port, args.workers)
    elif args.server == 'waitress':
        success = run_with_waitress(args.host, args.port)
    elif args.server == 'dev':
        success = run_development(args.host, args.port)
    else:
        print("❌ Invalid server type")
        return 1
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
