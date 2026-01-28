# Troubleshooting Guide - Online Bookstore

## Common Issues and Solutions

### Application Won't Start

#### Issue: `ModuleNotFoundError: No module named 'flask'`

**Cause**: Required packages not installed or virtual environment not activated

**Solution**:
```bash
# Activate virtual environment first
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep Flask
```

---

#### Issue: `SQLAlchemy: Could not locate a column in row for column 'user.id'`

**Cause**: Database tables not created or schema mismatch

**Solution**:
```bash
# Delete old database
rm instance/bookstore.db

# Recreate database and tables
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('Database created successfully')"

# Verify tables created
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); print(db.metadata.tables.keys())"
```

---

### Authentication Issues

#### Issue: `RuntimeError: The session has been invalidated`

**Cause**: Session management error or cookie corruption

**Solution**:
```bash
# Clear browser cookies:
# 1. Open browser settings
# 2. Find "Cookies and cached images"
# 3. Delete cookies for localhost:5000

# Or clear from code:
python -c "
from app import create_app
app = create_app()
with app.app_context():
    from flask import session
    session.clear()
"
```

---

#### Issue: `Login page loops - can't log in`

**Cause**: Password hash mismatch or database not initialized

**Solution**:
```bash
# Check if admin user exists
python -c "
from app import create_app, db
from app.models import User
app = create_app()
with app.app_context():
    admin = User.query.filter_by(email='admin@bookstore.com').first()
    if admin:
        print('Admin exists:', admin.username)
    else:
        print('Admin user not found - run initialization')
"

# Reinitialize database with sample data
python -c "
from app import create_app, db
from app.models import User, Category, Book
app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()
    # Add admin user
    admin = User(
        username='admin',
        email='admin@bookstore.com',
        full_name='Administrator',
        is_admin=True
    )
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    print('Admin user created: admin@bookstore.com / admin123')
"
```

---

### Database Issues

#### Issue: `OperationalError: unable to open database file`

**Cause**: Database file permissions or path issues

**Solution**:
```bash
# Check database location
python -c "
from app import create_app
app = create_app()
print('Database URL:', app.config['SQLALCHEMY_DATABASE_URI'])
"

# Check file permissions (Linux/Mac)
ls -la instance/bookstore.db

# Create instance directory if missing
mkdir -p instance
touch instance/bookstore.db
chmod 644 instance/bookstore.db
```

---

#### Issue: `IntegrityError: UNIQUE constraint failed: user.email`

**Cause**: Attempting to create user with duplicate email

**Solution**:
```bash
# Check existing users
python -c "
from app import create_app, db
from app.models import User
app = create_app()
with app.app_context():
    users = User.query.all()
    for user in users:
        print(f'{user.username}: {user.email}')
"

# Delete duplicate if needed
python -c "
from app import create_app, db
from app.models import User
app = create_app()
with app.app_context():
    # Find and delete duplicate
    duplicate = User.query.filter_by(email='duplicate@example.com').first()
    if duplicate:
        db.session.delete(duplicate)
        db.session.commit()
        print('Deleted duplicate user')
"
```

---

### Static Files Issues

#### Issue: CSS/JavaScript files not loading (404 errors)

**Cause**: Static files not served correctly or paths incorrect

**Solution**:
```bash
# Check static file paths
python -c "
from app import create_app
app = create_app()
print('Static folder:', app.static_folder)
print('Static URL path:', app.static_url_path)
"

# List static files
ls -la app/static/css/
ls -la app/static/js/

# Verify template is referencing correctly
# Should be: {{ url_for('static', filename='css/style.css') }}
# NOT: /static/css/style.css
```

---

#### Issue: Static files in production not served

**Cause**: Need to collect static files for production

**Solution**:
```bash
# For development with Flask
export FLASK_ENV=development
python run.py

# For production, use separate web server (nginx)
# Or use Flask with static file hosting

# Collect static files to public directory
flask collect-static  # or manually copy

# Or use nginx configuration
# location /static {
#     alias /path/to/app/static;
# }
```

---

### Performance Issues

#### Issue: Application running slowly

**Cause**: N+1 queries, missing indexes, or large dataset

**Solution**:
```bash
# Enable query logging
python -c "
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

from app import create_app, db
app = create_app()
with app.app_context():
    from flask import url_for
    # This will print all SQL queries
    books = db.session.query(Book).all()
"

# Add database indexes
python -c "
from app import create_app, db
from app.models import Book, User, Order
app = create_app()
with app.app_context():
    # Create indexes
    db.Index('idx_book_title', Book.title).create(db.engine)
    db.Index('idx_user_email', User.email).create(db.engine)
    db.Index('idx_order_created', Order.created_at).create(db.engine)
    print('Indexes created')
"
```

---

#### Issue: Memory usage constantly increasing

**Cause**: Database connection leaks or session not closing

**Solution**:
```python
# Ensure proper session cleanup
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

# Use context managers
with app.app_context():
    # Do database work
    users = User.query.all()
    # Session closes automatically

# Avoid keeping references to queries
# ✗ Bad
all_books = Book.query.all()
for book in all_books:
    print(book.title)
all_books = None  # Too late

# ✓ Good
for book in Book.query.all():
    print(book.title)
# Session closes automatically
```

---

### Form Validation Issues

#### Issue: Form validation always fails

**Cause**: CSRF token missing or invalid

**Solution**:
```html
<!-- Ensure CSRF token in form -->
<form method="POST">
    {{ form.csrf_token }}
    <!-- Other fields -->
    <button type="submit">Submit</button>
</form>
```

```python
# Check CSRF configuration
python -c "
from app import create_app
app = create_app()
print('Secret key:', app.config['SECRET_KEY'])
print('WTF CSRF enabled:', app.config.get('WTF_CSRF_ENABLED', True))
"
```

---

#### Issue: File uploads not working

**Cause**: Missing upload directory or permission issues

**Solution**:
```bash
# Create uploads directory
mkdir -p app/static/uploads
chmod 755 app/static/uploads

# Check upload configuration
python -c "
from app import create_app
app = create_app()
print('Upload folder:', app.config.get('UPLOAD_FOLDER'))
print('Max file size:', app.config.get('MAX_CONTENT_LENGTH'))
"

# Increase max file size if needed (in config.py)
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
```

---

### Email Issues

#### Issue: Password reset emails not sending

**Cause**: Mail server configuration incorrect

**Solution**:
```bash
# Check mail configuration
python -c "
from app import create_app
app = create_app()
print('Mail server:', app.config.get('MAIL_SERVER'))
print('Mail port:', app.config.get('MAIL_PORT'))
print('Mail username:', app.config.get('MAIL_USERNAME'))
"

# Test email sending
python -c "
from flask_mail import Message, Mail
from app import create_app

app = create_app()
mail = Mail(app)

with app.app_context():
    try:
        msg = Message(
            subject='Test Email',
            recipients=['test@example.com'],
            body='This is a test email'
        )
        mail.send(msg)
        print('Email sent successfully')
    except Exception as e:
        print(f'Error sending email: {e}')
"
```

---

### Git Issues

#### Issue: Git merge conflicts

**Solution**:
```bash
# View conflict markers
git diff

# Resolve conflicts manually in editor
# Then stage resolved files
git add resolved_file.py

# Complete merge
git commit -m "Resolve merge conflicts"

# Or abort merge
git merge --abort
```

---

#### Issue: Accidentally committed sensitive data

**Solution**:
```bash
# Remove from git history (before pushing)
git reset HEAD~1
git rm --cached sensitive_file
echo "sensitive_file" >> .gitignore
git add .gitignore
git commit -m "Remove sensitive file from history"

# If already pushed, rotate credentials immediately!
# Change API keys, passwords, etc.
```

---

## Debug Mode

### Enable Debug Output

```python
# In config.py or run.py
import logging

logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.DEBUG)

# Add to create_app()
app.config['DEBUG'] = True
app.config['TESTING'] = True
```

### Use Python Debugger

```python
# In route handler
from pdb import set_trace

@app.route('/debug-route')
def debug_route():
    set_trace()  # Debugger will pause here
    return render_template('template.html')

# In interactive shell
python -i run.py
# Then use pdb commands: n (next), s (step), c (continue), p (print)
```

### Use Flask Shell

```bash
# Interactive Python shell with app context
flask shell

# Then run code
>>> from app.models import User
>>> users = User.query.all()
>>> print(users)
```

---

## Performance Profiling

### Profile Flask Application

```python
from werkzeug.contrib.profiler import ProfilerMiddleware

if __name__ == '__main__':
    app.wsgi_app = ProfilerMiddleware(
        app.wsgi_app,
        restrictions=[30],
        sort_by=('cumulative', 'calls')
    )
    app.run(debug=True)
```

### Database Query Analysis

```bash
# Enable SQLAlchemy logging
export SQLALCHEMY_ECHO=True
python run.py

# Or in code
app.config['SQLALCHEMY_ECHO'] = True
```

---

## Verification Checklist

After resolving issues:

- [ ] Test in browser
- [ ] Check browser console for JavaScript errors
- [ ] Verify database tables exist
- [ ] Check application logs
- [ ] Run test suite
- [ ] Verify git status clean
- [ ] Document the issue and solution

---

## Getting More Help

1. **Check Application Logs**
   ```bash
   tail -f logs/bookstore.log
   ```

2. **Check Flask Debug Mode**
   - Look at detailed error pages in browser
   - Check stack traces for exact error location

3. **Search Documentation**
   - [Flask Documentation](https://flask.palletsprojects.com/)
   - [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
   - [Flask-WTF Documentation](https://flask-wtf.readthedocs.io/)

4. **Ask for Help**
   - Open GitHub issue with detailed error description
   - Include error logs and steps to reproduce
   - Mention Python version and OS

---

**Last Updated**: December 2024
**Version**: 1.0
