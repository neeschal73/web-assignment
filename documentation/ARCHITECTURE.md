# Architecture & Code Standards - Online Bookstore

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Project Structure](#project-structure)
3. [Code Standards](#code-standards)
4. [Design Patterns](#design-patterns)
5. [Database Schema](#database-schema)
6. [API Design](#api-design)
7. [Security Architecture](#security-architecture)
8. [Testing Strategy](#testing-strategy)

## Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Frontend Layer (HTML/CSS/JS)               │
│  - Jinja2 Templates with Bootstrap 5 responsive design          │
│  - Client-side form validation with JavaScript                 │
│  - Static assets (CSS, JavaScript, images)                      │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP Requests/Responses
┌─────────────────────────┴────────────────────────────────────────┐
│                      Application Layer (Flask)                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Request Routing (Flask Blueprints)                        │ │
│  │  - auth_bp: Authentication routes                          │ │
│  │  - main_bp: Main application routes                        │ │
│  │  - admin_bp: Administrative routes                         │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Business Logic Layer                                      │ │
│  │  - Form validation (Flask-WTF)                             │ │
│  │  - User authentication (Flask-Login)                       │ │
│  │  - Authorization & Access Control                          │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Data Access Layer (SQLAlchemy ORM)                        │ │
│  │  - Models & relationships                                  │ │
│  │  - Database queries                                        │ │
│  │  - Transaction management                                  │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────┬────────────────────────────────────────┘
                         │ SQL Queries
┌─────────────────────────┴────────────────────────────────────────┐
│                    Database Layer (SQLite/PostgreSQL)            │
│  - User table                                                    │
│  - Book catalog                                                  │
│  - Orders & order items                                          │
│  - Reviews & ratings                                             │
│  - Categories                                                    │
└─────────────────────────────────────────────────────────────────┘
```

### MVC Pattern Implementation

- **Model** (`app/models.py`): SQLAlchemy ORM models defining data structure
- **View** (`app/templates/`): Jinja2 templates for HTML rendering
- **Controller** (`app/routes_*.py`): Flask routes handling business logic

## Project Structure

```
online-bookstore/
├── app/
│   ├── __init__.py              # Flask application factory
│   ├── models.py                # SQLAlchemy database models (6 tables)
│   ├── forms.py                 # WTForms for validation
│   ├── auth.py                  # Login manager configuration
│   ├── routes_auth.py           # Authentication routes (register, login, profile)
│   ├── routes_main.py           # Main application routes (books, cart, checkout, orders)
│   ├── routes_admin.py          # Admin routes (manage books, categories, users)
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css        # Custom Bootstrap styling
│   │   └── js/
│   │       └── main.js          # Client-side validation & utilities
│   └── templates/
│       ├── base.html            # Master template with navigation
│       ├── home.html            # Homepage
│       ├── books.html           # Books listing with search/filter
│       ├── book_detail.html     # Book detail with reviews
│       ├── cart.html            # Shopping cart
│       ├── checkout.html        # Checkout form
│       ├── dashboard.html       # User dashboard
│       ├── order_detail.html    # Order details
│       ├── contact.html         # Contact form
│       ├── login.html           # Login form
│       ├── register.html        # Registration form
│       ├── profile.html         # User profile
│       ├── edit_profile.html    # Profile editing
│       ├── admin/
│       │   ├── dashboard.html   # Admin dashboard
│       │   ├── manage_books.html # Book management
│       │   ├── add_book.html    # Add new book
│       │   ├── edit_book.html   # Edit book
│       │   ├── manage_categories.html
│       │   ├── manage_orders.html
│       │   └── manage_users.html
│       └── errors/
│           ├── 404.html         # Not found
│           ├── 500.html         # Server error
│           └── 403.html         # Access denied
├── config.py                    # Flask configuration (Dev/Test/Prod)
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
└── documentation/
    ├── PROJECT_PROPOSAL.md      # Project specification
    ├── DATABASE_DESIGN.md       # Database schema & relationships
    ├── TESTING_DOCUMENTATION.md # Test cases
    ├── USER_MANUAL.md          # User guide
    ├── INSTALLATION_GUIDE.md   # Setup instructions
    ├── API_DOCUMENTATION.md    # API reference
    ├── DEPLOYMENT.md           # Deployment guides
    └── ARCHITECTURE.md         # This file
```

## Code Standards

### Python Code Style (PEP 8)

```python
# Module imports - organize by type
from datetime import datetime, timedelta
from functools import wraps

from flask import Flask, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Class naming - CamelCase
class UserModel:
    pass

# Function naming - snake_case
def create_user(username):
    pass

# Constant naming - UPPER_SNAKE_CASE
MAX_USERNAME_LENGTH = 50
DEFAULT_PAGE_SIZE = 20

# Variable naming - snake_case
user_email = "user@example.com"
is_admin = False
```

### Flask Route Structure

```python
from flask import Blueprint

# Create blueprint
auth_bp = Blueprint('auth', __name__)

# Route definition
@auth_bp.route('/register', methods=['GET', 'POST'])
@auth_bp.route('/login', methods=['GET', 'POST'])
@login_required
@admin_required
def my_route():
    """Route docstring explaining purpose and behavior."""
    # Implementation
    pass

# Register blueprint in app factory
def create_app(config_name='development'):
    app = Flask(__name__)
    app.register_blueprint(auth_bp)
    return app
```

### Database Model Structure

```python
from app import db
from datetime import datetime

class MyModel(db.Model):
    """Model docstring with description and relationships."""
    __tablename__ = 'my_table'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Regular columns
    name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    user = db.relationship('User', backref='my_objects')
    
    def __repr__(self):
        return f'<MyModel {self.name}>'
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat()
        }
```

### Form Validation Structure

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError

class MyForm(FlaskForm):
    """Form docstring."""
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=3, max=20)
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )
    submit = SubmitField('Submit')
    
    def validate_username(self, username):
        """Custom validation method."""
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('Username already exists.')
```

### HTML Template Structure (Jinja2)

```html
{% extends "base.html" %}

{% block title %}Page Title{% endblock %}

{% block content %}
<div class="container">
    <!-- Flash messages -->
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="alert alert-{{ category }}">
                    {{ message }}
                </div>
            {% endfor %}
        {% endif %}
    {% endwith %}
    
    <!-- Page content -->
    {% if current_user.is_authenticated %}
        <p>Welcome {{ current_user.username }}!</p>
    {% else %}
        <p>Please log in.</p>
    {% endif %}
    
    <!-- Loops and conditionals -->
    {% for item in items %}
        <div class="item">
            {{ item.name }}
        </div>
    {% else %}
        <p>No items found.</p>
    {% endfor %}
</div>
{% endblock %}
```

### JavaScript Code Style

```javascript
// Use ES6+ features when possible
const MAX_ITEMS = 100;

// Function naming - camelCase
function initializeFormValidation() {
    // Implementation
}

// Class naming - PascalCase
class FormValidator {
    constructor(formElement) {
        this.form = formElement;
    }
    
    validate() {
        // Implementation
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    initializeFormValidation();
});

// Error handling
try {
    // Code that might throw error
} catch (error) {
    console.error('Error:', error);
}
```

## Design Patterns

### 1. Application Factory Pattern

```python
# config.py
class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Load configuration
    if config_name == 'development':
        app.config.from_object('config.DevelopmentConfig')
    elif config_name == 'testing':
        app.config.from_object('config.TestingConfig')
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    
    return app
```

### 2. Blueprint Pattern

```python
# Create blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Routes
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    pass

# Register in app factory
app.register_blueprint(auth_bp)

# Access URL: /auth/register, /auth/login
```

### 3. Decorator Pattern (Access Control)

```python
from functools import wraps
from flask import abort

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    pass
```

### 4. Repository Pattern (Data Access)

```python
class UserRepository:
    @staticmethod
    def create_user(username, email, password_hash):
        user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)
```

## Database Schema

### Entity Relationship Diagram

```
┌──────────────────────┐
│      User            │
├──────────────────────┤
│ id (PK)              │
│ username (UNIQUE)    │
│ email (UNIQUE)       │
│ password_hash        │
│ full_name            │
│ phone                │
│ address              │
│ city                 │
│ postal_code          │
│ is_admin             │
│ created_at           │
│ updated_at           │
└──────────────────────┘
         │ 1
         │
         │ N
         ├─────────────────────────────────────┐
         │                                     │
┌────────▼──────────────┐          ┌──────────▼──────────────┐
│      Order            │          │      Review             │
├───────────────────────┤          ├───────────────────────────┤
│ id (PK)               │          │ id (PK)                   │
│ user_id (FK)          │          │ user_id (FK)              │
│ total_price           │          │ book_id (FK)              │
│ status                │          │ rating                    │
│ shipping_address      │          │ title                     │
│ shipping_city         │          │ content                   │
│ shipping_postal       │          │ created_at                │
│ created_at            │          │ updated_at                │
│ updated_at            │          └───────────────────────────┘
└────────┬──────────────┘                    ▲
         │ 1                                 │ N
         │                                   │
         │ N                    ┌────────────┴────────────┐
         │                      │                         │
┌────────▼──────────────┐      ┌▼───────────────────────┐
│    OrderItem          │      │       Book             │
├───────────────────────┤      ├───────────────────────┤
│ id (PK)               │      │ id (PK)               │
│ order_id (FK)         │      │ title (UNIQUE)        │
│ book_id (FK)          │      │ author                │
│ quantity              │      │ isbn (UNIQUE)         │
│ price_at_purchase     │      │ description           │
└───────────────────────┘      │ price                 │
         ▲                      │ stock                 │
         │ N                    │ category_id (FK)      │
         │                      │ publisher             │
         │ 1                    │ publication_year      │
         └──────────────────────┤ pages                 │
                                │ language              │
         ┌──────────────────────┤ created_at            │
         │ N                    │ updated_at            │
         │                      └───────────────────────┘
         │                               ▲
         │                               │ N
         │ 1                             │
┌────────┴──────────────┐               │ 1
│    Category           │      ┌────────┴───────────┐
├───────────────────────┤      │                    │
│ id (PK)               │      │ (Inherent in Book) │
│ name (UNIQUE)         │      └────────────────────┘
│ description           │
│ created_at            │
└───────────────────────┘
```

### Relationship Summary

| Relationship | Type | Description |
|---|---|---|
| User ↔ Order | 1:N | One user has many orders |
| User ↔ Review | 1:N | One user writes many reviews |
| Book ↔ Review | 1:N | One book has many reviews |
| Category ↔ Book | 1:N | One category has many books |
| Order ↔ OrderItem | 1:N | One order has many items |
| Book ↔ Order | M:N | (Via OrderItem) Many books in many orders |

## API Design

### RESTful Conventions

```
GET    /books              - List all books (paginated)
GET    /books/<id>         - Get specific book
POST   /books              - Create new book (admin)
PUT    /books/<id>         - Update book (admin)
DELETE /books/<id>         - Delete book (admin)

GET    /user/orders        - List user's orders
GET    /orders/<id>        - Get order details
POST   /orders             - Create new order (checkout)
PUT    /orders/<id>        - Update order (admin)

GET    /books/<id>/reviews - List book reviews
POST   /books/<id>/reviews - Add review
```

### API Response Format

```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Example"
  },
  "message": "Operation successful"
}
```

### Error Response Format

```json
{
  "success": false,
  "error": "Validation Error",
  "details": {
    "field_name": ["Error message"]
  }
}
```

## Security Architecture

### 1. Authentication Flow

```
User → Login Form
     ↓
Validate Credentials
     ↓
Check Password Hash
     ↓
Create Session (Flask-Login)
     ↓
Set Secure Cookie
     ↓
Redirect to Dashboard
```

### 2. Authorization Check

```python
from flask_login import current_user, login_required

@app.route('/dashboard')
@login_required  # Checks if user is authenticated
def dashboard():
    # User must be logged in
    return render_template('dashboard.html')

@app.route('/admin')
@admin_required  # Custom decorator
def admin_panel():
    # User must be admin
    return render_template('admin/dashboard.html')
```

### 3. Password Security

```python
from werkzeug.security import generate_password_hash, check_password_hash

# Hashing
password_hash = generate_password_hash('user_password')

# Verification
is_correct = check_password_hash(password_hash, 'user_password')
```

### 4. CSRF Protection

```python
# Enabled by default with Flask-WTF
# Every form includes CSRF token
<form method="POST">
    {{ form.csrf_token }}
    <!-- Form fields -->
</form>
```

## Testing Strategy

### Unit Testing (Models)

```python
import unittest
from app import create_app, db
from app.models import User, Book

class UserModelTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_user_password_hashing(self):
        user = User(username='test', email='test@example.com')
        user.set_password('password123')
        self.assertFalse(user.check_password('wrong_password'))
        self.assertTrue(user.check_password('password123'))
```

### Integration Testing (Routes)

```python
def test_user_registration():
    client = app.test_client()
    response = client.post('/register', data={
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    assert response.status_code == 302  # Redirect after success
```

### Test Coverage Goals

- Models: 100% coverage
- Routes: 95%+ coverage
- Forms: 90%+ coverage
- Utilities: 100% coverage

---

**Last Updated**: December 2024
**Version**: 1.0
**Status**: Stable
