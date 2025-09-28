#!/usr/bin/env python3
"""
Simple run script for NSAKCET College Chatbot
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

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

def download_nltk_data():
    """Download required NLTK data"""
    try:
        import nltk
        print("📥 Downloading NLTK data...")
        nltk.download('punkt', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('omw-1.4', quiet=True)
        print("✅ NLTK data downloaded")
    except Exception as e:
        print(f"⚠️ Warning: Could not download NLTK data: {e}")

def check_files():
    """Check if required files exist"""
    required_files = [
        "app.py",
        "intents.json",
        "requirements.txt",
        "templates/index.html",
        "static/css/style.css",
        "static/js/script.js"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print("✅ All required files found")
    return True

def main():
    """Main function to run the chatbot"""
    print("🚀 Starting NSAKCET College Chatbot...")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Check if files exist
    if not check_files():
        print("❌ Please ensure all required files are present")
        sys.exit(1)
    
    # Check and install dependencies
    if not check_dependencies():
        print("❌ Please install dependencies manually: pip install -r requirements.txt")
        sys.exit(1)
    
    # Download NLTK data
    download_nltk_data()
    
    print("=" * 50)
    print("🎉 Setup complete! Starting the chatbot...")
    print("🌐 The chatbot will be available at: http://localhost:5000")
    print("⏹️ Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Run the Flask app
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Chatbot stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error starting the chatbot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
