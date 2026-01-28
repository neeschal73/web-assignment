"""
Online Bookstore - Main Application Entry Point
Run this file to start the Flask development server
"""
from app import create_app, db

if __name__ == '__main__':
    app = create_app()
    
    # Create database tables and sample data
    with app.app_context():
        db.create_all()
    
    # Run development server
    app.run(debug=True, host='0.0.0.0', port=5000)
