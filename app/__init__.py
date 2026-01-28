from flask import Flask, render_template
from config import DevelopmentConfig
from app.models import db
from app.auth import login_manager
from app.routes_auth import auth_bp
from app.routes_main import main_bp
from app.routes_admin import admin_bp

"""
Flask Application Factory
Initializes and configures the Flask application with all blueprints and extensions
"""


def create_app(config_class=DevelopmentConfig):
    """
    Application factory function
    
    Args:
        config_class: Configuration class to use
    
    Returns:
        Flask application instance
    """
    app = Flask(__name__, 
                template_folder='app/templates',
                static_folder='app/static')
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def page_not_found(error):
        """Handle 404 errors"""
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(403)
    def forbidden(error):
        """Handle 403 errors"""
        return render_template('errors/403.html'), 403
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Initialize sample data
    with app.app_context():
        initialize_sample_data(app)
    
    return app


def initialize_sample_data(app):
    """
    Initialize database with sample data
    This function runs once when the app starts
    """
    # Check if data already exists
    if Category.query.first() is not None:
        return
    
    from app.models import Category, Book, User
    
    # Create categories
    categories = [
        Category(name='Fiction', description='Fiction novels and stories'),
        Category(name='Science Fiction', description='Science fiction and futuristic tales'),
        Category(name='Mystery', description='Mystery and detective novels'),
        Category(name='Self-Help', description='Self-help and personal development'),
        Category(name='Technology', description='Technology and programming books'),
    ]
    
    for cat in categories:
        db.session.add(cat)
    
    db.session.commit()
    
    # Create sample books
    sample_books = [
        {
            'title': 'The Great Gatsby',
            'author': 'F. Scott Fitzgerald',
            'isbn': '978-0743273565',
            'description': 'A classic American novel set in the Jazz Age.',
            'price': 12.99,
            'stock': 50,
            'category_id': 1,
            'publisher': 'Scribner',
            'publication_year': 1925,
            'pages': 180,
            'language': 'English'
        },
        {
            'title': 'To Kill a Mockingbird',
            'author': 'Harper Lee',
            'isbn': '978-0061120084',
            'description': 'A gripping tale of racial inequality and childhood innocence.',
            'price': 14.99,
            'stock': 45,
            'category_id': 1,
            'publisher': 'J.B. Lippincott',
            'publication_year': 1960,
            'pages': 324,
            'language': 'English'
        },
        {
            'title': '1984',
            'author': 'George Orwell',
            'isbn': '978-0451524935',
            'description': 'A dystopian novel about totalitarianism.',
            'price': 13.99,
            'stock': 40,
            'category_id': 2,
            'publisher': 'Signet Classic',
            'publication_year': 1949,
            'pages': 328,
            'language': 'English'
        },
        {
            'title': 'The Hobbit',
            'author': 'J.R.R. Tolkien',
            'isbn': '978-0547928227',
            'description': 'An adventure fantasy novel about a hobbit\'s unexpected journey.',
            'price': 15.99,
            'stock': 55,
            'category_id': 2,
            'publisher': 'Houghton Mifflin Harcourt',
            'publication_year': 1937,
            'pages': 310,
            'language': 'English'
        },
        {
            'title': 'The Girl with the Dragon Tattoo',
            'author': 'Stieg Larsson',
            'isbn': '978-0307454546',
            'description': 'A thrilling mystery novel set in Sweden.',
            'price': 16.99,
            'stock': 35,
            'category_id': 3,
            'publisher': 'Knopf',
            'publication_year': 2005,
            'pages': 465,
            'language': 'English'
        },
        {
            'title': 'Atomic Habits',
            'author': 'James Clear',
            'isbn': '978-0735211292',
            'description': 'Transform your habits and build systems for success.',
            'price': 17.99,
            'stock': 60,
            'category_id': 4,
            'publisher': 'Avery',
            'publication_year': 2018,
            'pages': 320,
            'language': 'English'
        },
        {
            'title': 'Clean Code',
            'author': 'Robert C. Martin',
            'isbn': '978-0132350884',
            'description': 'A handbook for writing readable, maintainable code.',
            'price': 32.99,
            'stock': 30,
            'category_id': 5,
            'publisher': 'Prentice Hall',
            'publication_year': 2008,
            'pages': 464,
            'language': 'English'
        },
        {
            'title': 'Python Crash Course',
            'author': 'Eric Matthes',
            'isbn': '978-1593279288',
            'description': 'A hands-on introduction to programming with Python.',
            'price': 35.99,
            'stock': 25,
            'category_id': 5,
            'publisher': 'No Starch Press',
            'publication_year': 2015,
            'pages': 544,
            'language': 'English'
        },
    ]
    
    for book_data in sample_books:
        book = Book(**book_data)
        db.session.add(book)
    
    db.session.commit()
    
    # Create sample admin user
    admin_user = User.query.filter_by(email='admin@bookstore.com').first()
    if not admin_user:
        admin = User(
            username='admin',
            email='admin@bookstore.com',
            full_name='Admin User',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
