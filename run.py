#!/usr/bin/env python3
"""
PDF Flashcard Generator - Web Application
Run with: python run.py
"""

import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_directories():
    """Create necessary directories"""
    directories = [
        "static/uploads",
        "static/downloads",
        "templates"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Directory created/verified: {directory}")

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        "fastapi",
        "uvicorn",
        "pandas",
        "reportlab",
        "openpyxl"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("⚠ Missing packages:", ", ".join(missing_packages))
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Main entry point"""
    print("=" * 60)
    print("PDF Flashcard Generator - Web Application")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Please install missing dependencies first")
        return
    
    # Create directories
    create_directories()
    
    # Configuration
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("RELOAD", "true").lower() == "true"
    
    print(f"\n🚀 Starting server on: http://{host}:{port}")
    print(f"📁 Upload directory: static/uploads")
    print(f"📁 Download directory: static/downloads")
    print(f"🔄 Auto-reload: {'Enabled' if reload else 'Disabled'}")
    print("\n⚡ Press Ctrl+C to stop")
    print("=" * 60)
    
    # Start server
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
