# Performance Optimization Guide - Online Bookstore

## Overview

This guide provides strategies and techniques to optimize the Online Bookstore application for maximum performance.

## Database Optimization

### 1. Query Optimization

#### N+1 Query Problem

**Problem Example**:
```python
# ✗ BAD: This causes N+1 queries
users = User.query.all()  # 1 query
for user in users:
    orders = user.orders  # N queries (one per user)
```

**Solution - Use Eager Loading**:
```python
# ✓ GOOD: Single query with eager loading
from sqlalchemy.orm import joinedload

users = User.query.options(joinedload(User.orders)).all()
# Only 2 queries total

# Or use selectinload for better performance with many relations
from sqlalchemy.orm import selectinload
users = User.query.options(selectinload(User.orders)).all()
```

#### Query Limiting and Pagination

```python
# ✗ BAD: Loading all 10,000 books into memory
all_books = Book.query.all()

# ✓ GOOD: Use pagination
page = request.args.get('page', 1, type=int)
books = Book.query.paginate(page=page, per_page=12)
print(f"Showing {books.total} books total")
```

#### Selective Field Queries

```python
# ✗ BAD: Loading entire book objects when you only need titles
books = Book.query.all()
titles = [book.title for book in books]

# ✓ GOOD: Load only what you need
titles = db.session.query(Book.title).all()
```

### 2. Database Indexing

#### Add Strategic Indexes

```python
# In models.py
from app import db

class Book(db.Model):
    __tablename__ = 'book'
    
    # Frequently searched fields
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    author = db.Column(db.String(100), nullable=False, index=True)
    isbn = db.Column(db.String(20), unique=True, index=True)
    
    # Foreign keys should be indexed
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), index=True)
    
    # Timestamp fields used in sorting
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

class Order(db.Model):
    __tablename__ = 'order'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    status = db.Column(db.String(20), index=True)
```

#### Composite Indexes

```python
# For queries filtering on multiple columns
from sqlalchemy import Index

class Review(db.Model):
    __tablename__ = 'review'
    __table_args__ = (
        Index('idx_book_user_review', 'book_id', 'user_id'),
        Index('idx_created_rating', 'created_at', 'rating'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rating = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### 3. Connection Pooling

```python
# In config.py
class ProductionConfig:
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,              # Number of connections to keep
        'pool_recycle': 3600,         # Recycle connections after 1 hour
        'pool_pre_ping': True,        # Ping connection before using
        'max_overflow': 20,           # Allow overflow connections
        'echo_pool': False,           # Set True for debugging
    }
```

### 4. Query Caching

```python
from flask_caching import Cache
from app import app

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/books')
@cache.cached(timeout=60)  # Cache for 60 seconds
def get_books():
    books = Book.query.paginate(page=1, per_page=12)
    return render_template('books.html', books=books)

# Cache popular categories
@cache.cached(timeout=300)  # Cache for 5 minutes
def get_categories():
    return Category.query.all()

# Invalidate cache when data changes
@app.route('/admin/book/add', methods=['POST'])
def add_book():
    # ... create book ...
    cache.delete('get_books')  # Clear books cache
    return redirect('/admin/books')
```

## Frontend Optimization

### 1. CSS and JavaScript

#### Minification

```bash
# Install minifiers
pip install cssmin jsmin

# Or use build tools like webpack/gulp
# Example with webpack:
npm install --save-dev webpack webpack-cli

# Configure webpack.config.js
# Build optimized assets
npx webpack --mode production
```

#### Bundling

```javascript
// Combine multiple JS files into one
// webpack.config.js
module.exports = {
    entry: './app/static/js/main.js',
    output: {
        filename: 'bundle.min.js',
        path: './app/static/js/dist'
    },
    mode: 'production'
};
```

### 2. Image Optimization

```bash
# Compress images
# Using ImageMagick
convert image.jpg -quality 85 -resize 1200x image-optimized.jpg

# Using Pillow in Python
from PIL import Image
img = Image.open('image.jpg')
img.save('image-optimized.jpg', 'JPEG', quality=85, optimize=True)
```

#### Responsive Images

```html
<!-- Serve different sizes for different devices -->
<picture>
    <source media="(max-width: 480px)" srcset="image-small.jpg">
    <source media="(max-width: 768px)" srcset="image-medium.jpg">
    <img src="image-large.jpg" alt="Description">
</picture>
```

### 3. Lazy Loading

```html
<!-- Lazy load images that are below the fold -->
<img src="placeholder.jpg" 
     data-src="actual-image.jpg" 
     loading="lazy" 
     alt="Description">
```

```javascript
// Lazy load images on scroll
const images = document.querySelectorAll('img[loading="lazy"]');
const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src;
            img.removeAttribute('loading');
            observer.unobserve(img);
        }
    });
});

images.forEach(img => imageObserver.observe(img));
```

### 4. CDN Usage

```python
# Serve static files through CDN
# In templates, use CDN URLs for popular libraries
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

# For your custom files, use CloudFront/Cloudflare
STATIC_URL = 'https://cdn.example.com/static/'
```

## Application Performance

### 1. Request/Response Caching

```python
from flask import request, jsonify
from functools import wraps

def cache_response(timeout=60):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = f'response_{request.path}_{request.args}'
            
            # Try to get from cache
            cached = cache.get(cache_key)
            if cached:
                return cached
            
            # Generate response
            response = f(*args, **kwargs)
            
            # Store in cache
            cache.set(cache_key, response, timeout=timeout)
            return response
        return decorated_function
    return decorator

@app.route('/api/books')
@cache_response(timeout=300)
def api_books():
    books = Book.query.paginate(page=1, per_page=100)
    return jsonify([book.to_dict() for book in books.items])
```

### 2. Database Connection Pooling

```python
# Already configured in config.py
# Reuse connections instead of creating new ones
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 10,
    'pool_recycle': 3600,
}
```

### 3. Async Tasks

```python
# For long-running tasks, use task queue
from celery import Celery

celery = Celery(app.name, broker='redis://localhost:6379')

@celery.task
def send_order_confirmation_email(order_id):
    order = Order.query.get(order_id)
    # Send email asynchronously
    pass

# Usage in route
@app.route('/checkout', methods=['POST'])
def checkout():
    # Create order
    order = Order(...)
    db.session.add(order)
    db.session.commit()
    
    # Send email asynchronously
    send_order_confirmation_email.delay(order.id)
    
    return redirect('/dashboard')
```

### 4. Compression

```python
# Enable gzip compression
from flask_compress import Compress

app = Flask(__name__)
Compress(app)

# Or configure in web server (nginx)
# gzip on;
# gzip_types text/plain text/css text/js application/json;
# gzip_min_length 1000;
```

## Monitoring and Profiling

### 1. Application Profiling

```python
from werkzeug.middleware.profiler import ProfilerMiddleware
import cProfile

# Profile requests
if app.debug:
    app.wsgi_app = ProfilerMiddleware(
        app.wsgi_app,
        restrictions=[30],  # Show top 30 functions
        sort_by=('cumulative', 'calls')
    )

# Access profiling results at http://localhost:5000/profile/results
```

### 2. Database Query Logging

```python
# Enable SQLAlchemy query logging
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Or in code
app.config['SQLALCHEMY_ECHO'] = True

# Track slow queries
from flask import before_request, after_request
import time

@app.before_request
def before_request_time():
    request.start_time = time.time()

@app.after_request
def after_request_logging(response):
    duration = time.time() - request.start_time
    if duration > 0.5:  # Log if took more than 500ms
        app.logger.warning(f'Slow request: {request.path} took {duration:.2f}s')
    return response
```

### 3. Performance Metrics

```python
# Track key metrics
import time
from collections import defaultdict

metrics = defaultdict(list)

def track_metric(name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            start = time.time()
            result = f(*args, **kwargs)
            duration = time.time() - start
            metrics[name].append(duration)
            return result
        return decorated_function
    return decorator

@track_metric('db.user.query')
def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

# View metrics
def get_performance_stats():
    stats = {}
    for name, times in metrics.items():
        stats[name] = {
            'count': len(times),
            'avg': sum(times) / len(times),
            'min': min(times),
            'max': max(times)
        }
    return stats
```

## Load Testing

### Using Apache Bench

```bash
# Test 1000 requests with 10 concurrent
ab -n 1000 -c 10 http://localhost:5000/

# Test with POST data
ab -n 1000 -c 10 -p data.json -T application/json http://localhost:5000/api/books
```

### Using Locust

```python
# locustfile.py
from locust import HttpUser, task, between

class BookstoreUser(HttpUser):
    wait_time = between(1, 5)
    
    @task
    def view_books(self):
        self.client.get('/books')
    
    @task
    def view_book_detail(self):
        self.client.get('/book/1')
    
    @task
    def search(self):
        self.client.get('/books?search=python')
    
    def on_start(self):
        # Login
        self.client.post('/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
```

```bash
# Run load test
locust -f locustfile.py --host=http://localhost:5000
# Open http://localhost:8089
```

## Best Practices Summary

### Quick Wins

1. **Enable database indexes** - Fastest improvement for queries
2. **Use pagination** - Don't load thousands of records
3. **Cache frequently accessed data** - Reduce database hits
4. **Optimize images** - Reduce payload size
5. **Enable compression** - Reduce network bandwidth
6. **Use lazy loading** - Improve page load time
7. **Minify CSS/JS** - Reduce file sizes
8. **Use CDN for static files** - Faster delivery globally

### Medium Effort

9. **Implement eager loading** - Reduce query count
10. **Add strategic indexes** - Optimize slow queries
11. **Use async tasks** - Don't block requests
12. **Monitor performance** - Find bottlenecks
13. **Implement request caching** - Reduce computation
14. **Use connection pooling** - Reduce overhead

### Long Term

15. **Scale horizontally** - Add more application servers
16. **Use database replication** - Read from replicas
17. **Implement API rate limiting** - Prevent abuse
18. **Use message queues** - Decouple services
19. **Implement CDN** - Global content delivery
20. **Use database sharding** - Scale database

---

**Last Updated**: December 2024
**Version**: 1.0
