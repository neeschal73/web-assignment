# Deployment Guide - Online Bookstore

## Table of Contents
1. [Production Environment Setup](#production-environment-setup)
2. [Deployment Platforms](#deployment-platforms)
3. [Database Migration](#database-migration)
4. [Security Considerations](#security-considerations)
5. [Monitoring & Maintenance](#monitoring--maintenance)
6. [Troubleshooting](#troubleshooting)

## Production Environment Setup

### Environment Configuration

Before deploying, ensure the following environment variables are set:

```bash
# .env file (do not commit to version control)
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secure-random-key-here
DATABASE_URL=postgresql://user:password@localhost/bookstore_prod
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Database Setup for Production

#### PostgreSQL Setup (Recommended)

1. **Install PostgreSQL**
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install postgresql postgresql-contrib
   
   # macOS
   brew install postgresql
   ```

2. **Create Database and User**
   ```bash
   sudo -u postgres psql
   
   CREATE USER bookstore_user WITH PASSWORD 'secure-password';
   CREATE DATABASE bookstore_prod OWNER bookstore_user;
   GRANT ALL PRIVILEGES ON DATABASE bookstore_prod TO bookstore_user;
   ```

3. **Update Connection String**
   ```
   DATABASE_URL=postgresql://bookstore_user:secure-password@localhost/bookstore_prod
   ```

### Application Configuration

1. **Update config.py**
   ```python
   import os
   from datetime import timedelta
   
   class ProductionConfig:
       DEBUG = False
       TESTING = False
       SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
       SECRET_KEY = os.environ.get('SECRET_KEY')
       SQLALCHEMY_TRACK_MODIFICATIONS = False
       SQLALCHEMY_ENGINE_OPTIONS = {
           'pool_size': 10,
           'pool_recycle': 3600,
           'pool_pre_ping': True,
       }
       SESSION_COOKIE_SECURE = True
       SESSION_COOKIE_HTTPONLY = True
       SESSION_COOKIE_SAMESITE = 'Lax'
       PERMANENT_SESSION_LIFETIME = timedelta(days=7)
   ```

2. **Update run.py for Production**
   ```python
   from app import create_app, db
   import os
   
   app = create_app(os.environ.get('FLASK_ENV', 'development'))
   
   if __name__ == '__main__':
       # Use production WSGI server - gunicorn instead
       app.run()
   ```

## Deployment Platforms

### Option 1: Heroku Deployment

#### Prerequisites
- Heroku CLI installed
- Git repository initialized
- Heroku account

#### Steps

1. **Install Gunicorn (Production WSGI Server)**
   ```bash
   pip install gunicorn
   pip freeze > requirements.txt
   ```

2. **Create Procfile**
   ```
   # Procfile
   web: gunicorn run:app
   ```

3. **Create runtime.txt**
   ```
   python-3.11.4
   ```

4. **Heroku Setup**
   ```bash
   heroku login
   heroku create your-bookstore-app
   heroku addons:create heroku-postgresql:hobby-dev
   ```

5. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set FLASK_ENV=production
   ```

6. **Deploy**
   ```bash
   git push heroku master
   heroku run python -c "from app import db, create_app; app = create_app('production'); db.create_all()"
   heroku logs --tail
   ```

### Option 2: PythonAnywhere Deployment

#### Prerequisites
- PythonAnywhere account (free or paid)
- Git repository

#### Steps

1. **Clone Repository on PythonAnywhere**
   - Open bash console on PythonAnywhere
   ```bash
   git clone https://github.com/yourusername/online-bookstore.git
   cd online-bookstore
   ```

2. **Create Virtual Environment**
   ```bash
   mkvirtualenv --python=/usr/bin/python3.11 bookstore
   pip install -r requirements.txt
   ```

3. **Configure Web App**
   - Go to Web tab in PythonAnywhere
   - Add new web app
   - Choose Python 3.11
   - Point WSGI file to: `/home/yourusername/online-bookstore/wsgi.py`

4. **Create WSGI File**
   ```python
   # wsgi.py
   import sys
   import os
   
   path = '/home/yourusername/online-bookstore'
   if path not in sys.path:
       sys.path.append(path)
   
   os.environ['FLASK_ENV'] = 'production'
   os.environ['SECRET_KEY'] = 'your-secret-key'
   
   from run import app as application
   ```

5. **Configure Database**
   - Use MySQL (provided by PythonAnywhere)
   - Create database in PythonAnywhere MySQL tab
   - Update `DATABASE_URL` in environment

### Option 3: DigitalOcean App Platform

#### Prerequisites
- DigitalOcean account
- GitHub repository connected
- Docker installed locally

#### Steps

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   ENV FLASK_APP=run.py
   ENV FLASK_ENV=production
   
   EXPOSE 8000
   
   CMD ["gunicorn", "--bind", "0.0.0.0:8000", "run:app"]
   ```

2. **Create .dockerignore**
   ```
   .git
   .gitignore
   __pycache__
   *.pyc
   .env
   venv/
   .DS_Store
   *.sqlite
   *.sqlite3
   ```

3. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add Docker configuration for DigitalOcean deployment"
   git push origin main
   ```

4. **Deploy on DigitalOcean**
   - Create new App Platform app
   - Connect GitHub repository
   - Set environment variables
   - Deploy

### Option 4: AWS Elastic Beanstalk

#### Prerequisites
- AWS account
- AWS CLI installed
- Elastic Beanstalk CLI installed

#### Steps

1. **Initialize Elastic Beanstalk**
   ```bash
   eb init -p python-3.11 online-bookstore --region us-east-1
   ```

2. **Create Environment**
   ```bash
   eb create production-env
   ```

3. **Set Environment Variables**
   ```bash
   eb setenv SECRET_KEY=your-secret-key FLASK_ENV=production
   ```

4. **Deploy**
   ```bash
   eb deploy
   ```

## Database Migration

### Initial Production Database Setup

1. **Backup Development Database** (if needed)
   ```bash
   sqlite3 bookstore.db ".dump" > backup.sql
   ```

2. **Initialize Production Database**
   ```bash
   from app import create_app, db
   app = create_app('production')
   with app.app_context():
       db.create_all()
   ```

3. **Load Sample Data** (optional)
   ```bash
   from app import create_app, db
   from app.models import Category, Book, User
   app = create_app('production')
   with app.app_context():
       # Add initial categories and books
       pass
   ```

### Alembic for Database Migrations (Optional)

For future updates, use Alembic for version control of database schema:

```bash
pip install alembic
alembic init migrations
```

## Security Considerations

### 1. Environment Variables
- **Never commit secrets** to version control
- Use `.env` files (ignored by .gitignore)
- Rotate `SECRET_KEY` regularly

### 2. HTTPS/SSL
- **Always use HTTPS** in production
- Enable automatic redirects from HTTP to HTTPS
- Use Let's Encrypt for free SSL certificates

```python
# In Flask app
@app.before_request
def redirect_to_https():
    if not request.is_secure and app.env == 'production':
        return redirect(request.url.replace('http://', 'https://'), code=301)
```

### 3. Database Security
- Use strong, unique passwords
- Enable database backups
- Restrict database access to application server only
- Use connection pooling

### 4. Application Security
- Set `FLASK_DEBUG = False` in production
- Configure CORS if needed
- Implement rate limiting for login attempts
- Enable CSRF protection (already included in Flask-WTF)

### 5. Logging and Monitoring
```python
import logging
from logging.handlers import RotatingFileHandler
import os

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/bookstore.log', 
                                       maxBytes=10240000, 
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Online Bookstore startup')
```

## Monitoring & Maintenance

### 1. Application Health Checks
- Create health check endpoint
- Monitor response times
- Track error rates

```python
@app.route('/health')
def health_check():
    try:
        db.session.execute('SELECT 1')
        return {'status': 'healthy'}, 200
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}, 503
```

### 2. Database Backups
- Schedule automated daily backups
- Store backups in secure, separate location
- Test backup restoration regularly

```bash
# PostgreSQL backup script
#!/bin/bash
pg_dump -U bookstore_user bookstore_prod > /backup/bookstore_$(date +%Y%m%d).sql
```

### 3. Log Monitoring
- Monitor error logs regularly
- Set up alerts for critical errors
- Archive logs for long-term storage

### 4. Performance Monitoring
- Monitor database query performance
- Track API response times
- Monitor server resource usage

## Troubleshooting

### Common Deployment Issues

#### Issue 1: Database Connection Failures
**Symptom**: `OperationalError: (psycopg2.OperationalError) could not connect`

**Solution**:
1. Verify `DATABASE_URL` is correct
2. Check database server is running
3. Verify firewall rules allow connection
4. Test connection manually: `psql -U user -d database -h host`

#### Issue 2: Static Files Not Loading
**Symptom**: CSS/JavaScript files return 404 errors

**Solution**:
```bash
# Collect static files
python -c "from app import create_app; app = create_app('production'); app.config['FLASK_ENV'] = 'production'"
flask collect-static

# Or serve with nginx
location /static {
    alias /path/to/app/static;
}
```

#### Issue 3: Memory Issues
**Symptom**: Application crashes with OutOfMemory errors

**Solution**:
- Increase gunicorn worker timeout
- Implement database connection pooling
- Add caching layer (Redis)
- Monitor and optimize queries

#### Issue 4: Login Issues
**Symptom**: Users cannot log in after deployment

**Solution**:
- Check `SECRET_KEY` consistency across servers
- Verify `SESSION_COOKIE_SECURE` settings
- Clear browser cookies and try again
- Check database connectivity

#### Issue 5: Email Notifications Not Sending
**Symptom**: Password reset/contact emails not received

**Solution**:
- Verify SMTP credentials
- Check `MAIL_SERVER`, `MAIL_PORT` settings
- Ensure firewall allows outgoing connections
- Check email spam folder
- Enable "Less secure apps" if using Gmail

### Debug Commands

```bash
# Check Flask app configuration
flask shell
>>> app.config

# Test database connection
python -c "from app import db, create_app; app = create_app('production'); 
           with app.app_context(): db.session.execute('SELECT 1')"

# Check environment variables
env | grep FLASK

# View application logs
tail -f logs/bookstore.log
```

## Performance Optimization

### 1. Database Optimization
```python
# Add database indexes
db.Index('idx_book_title', Book.title)
db.Index('idx_user_email', User.email)
db.Index('idx_order_created', Order.created_at)
```

### 2. Caching Strategy
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/books')
@cache.cached(timeout=60)
def get_books():
    # This will be cached for 60 seconds
    pass
```

### 3. CDN Integration
- Serve static files through CDN (CloudFront, Cloudflare)
- Reduce server load
- Improve global performance

### 4. Database Connection Pooling
```python
# Already configured in ProductionConfig
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True,
}
```

## Rollback Procedures

### If Deployment Fails

1. **Heroku Rollback**
   ```bash
   heroku releases
   heroku rollback v123
   ```

2. **Manual Rollback**
   ```bash
   git revert HEAD
   git push origin main
   # Redeploy
   ```

3. **Database Rollback**
   ```bash
   psql -U user -d database < /backup/bookstore_backup.sql
   ```

## Success Checklist

- [ ] Environment variables configured
- [ ] Database created and migrated
- [ ] SSL/HTTPS certificate installed
- [ ] Static files serving correctly
- [ ] Email notifications working
- [ ] Admin panel accessible
- [ ] User authentication working
- [ ] Shopping cart functional
- [ ] Checkout process tested
- [ ] Error handling working
- [ ] Logging configured
- [ ] Backups automated
- [ ] Monitoring set up
- [ ] Performance acceptable
- [ ] Security headers configured

---

**Last Updated**: December 2024
**Version**: 1.0
**Status**: Production Ready
