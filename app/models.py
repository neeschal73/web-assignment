from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

"""
Database Models for Online Bookstore
Defines the structure of database tables and relationships
"""

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """
    User Model - Stores user information and authentication details
    Relationships:
    - One-to-Many with Order
    - One-to-Many with Review
    """
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    city = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    orders = db.relationship('Order', backref='user', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set user password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Book(db.Model):
    """
    Book Model - Stores book information and inventory
    Relationships:
    - Many-to-One with Category
    - One-to-Many with Review
    - Many-to-Many with Order (through OrderItem)
    """
    __tablename__ = 'book'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    author = db.Column(db.String(120), nullable=False, index=True)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    cover_image = db.Column(db.String(255))
    publisher = db.Column(db.String(120))
    publication_year = db.Column(db.Integer)
    pages = db.Column(db.Integer)
    language = db.Column(db.String(50), default='English')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    category = db.relationship('Category', backref='books')
    reviews = db.relationship('Review', backref='book', lazy=True, cascade='all, delete-orphan')
    order_items = db.relationship('OrderItem', backref='book', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Book {self.title}>'


class Category(db.Model):
    """
    Category Model - Stores book categories
    Relationships:
    - One-to-Many with Book
    """
    __tablename__ = 'category'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Category {self.name}>'


class Order(db.Model):
    """
    Order Model - Stores customer orders
    Relationships:
    - Many-to-One with User
    - One-to-Many with OrderItem
    """
    __tablename__ = 'order'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Pending')  # Pending, Processing, Shipped, Delivered, Cancelled
    shipping_address = db.Column(db.String(255))
    shipping_city = db.Column(db.String(100))
    shipping_postal = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order_items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Order {self.id}>'


class OrderItem(db.Model):
    """
    OrderItem Model - Stores individual items in an order (Join table for Order-Book relationship)
    Relationships:
    - Many-to-One with Order
    - Many-to-One with Book
    """
    __tablename__ = 'order_item'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False, index=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_purchase = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f'<OrderItem Order:{self.order_id} Book:{self.book_id}>'


class Review(db.Model):
    """
    Review Model - Stores user reviews for books
    Relationships:
    - Many-to-One with User
    - Many-to-One with Book
    """
    __tablename__ = 'review'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False, index=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Review {self.id}>'
