# Installation Guide - Online Bookstore

Complete step-by-step guide to install and run the Online Bookstore application.

---

## Prerequisites

Before installing, ensure you have:
- **Python 3.8 or higher** installed on your system
- **pip** (Python package manager)
- **Git** installed and configured
- **Administrator/sudo access** (if needed for system packages)
- **At least 500MB** of free disk space

### System Requirements

**Minimum:**
- OS: Windows 7+, macOS 10.14+, Linux (any modern distro)
- RAM: 2GB
- CPU: 1GHz or higher
- Storage: 500MB free space

**Recommended:**
- OS: Windows 10+, macOS 11+, Ubuntu 20.04 LTS+
- RAM: 4GB or more
- CPU: 2GHz or higher
- Storage: SSD with 1GB+ free space

---

## Installation Steps

### Step 1: Verify Python Installation

Open command prompt/terminal and check if Python is installed:

```bash
python --version
```

Expected output: `Python 3.8.x` or higher

If Python is not installed, download from [python.org](https://www.python.org/)

### Step 2: Clone the Repository

Clone the project from GitHub:

```bash
git clone https://github.com/yourusername/online-bookstore.git
cd online-bookstore
```

**Alternative:** If not using Git, download the ZIP file and extract it.

### Step 3: Create Virtual Environment

A virtual environment isolates project dependencies from system Python.

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your command prompt after activation.

### Step 4: Upgrade pip

Ensure pip is up to date:

```bash
pip install --upgrade pip
```

### Step 5: Install Dependencies

Install all required packages from requirements.txt:

```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- Flask-SQLAlchemy (database ORM)
- Flask-Login (authentication)
- Flask-WTF (forms)
- WTForms (form validation)
- Werkzeug (security utilities)
- Email-validator (email validation)

### Step 6: Verify Installation

Verify all packages are installed:

```bash
pip list
```

Check that all required packages are listed.

### Step 7: Initialize the Database

The database will be created automatically when you run the app for the first time. To manually initialize it:

```bash
python -c "from app import create_app; app = create_app(); app.app_context().push(); from app.models import db; db.create_all()"
```

### Step 8: Run the Application

Start the Flask development server:

```bash
python run.py
```

You should see output similar to:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Step 9: Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

---

## Troubleshooting Installation

### Python Not Found

**Problem:** `python: command not found` or `'python' is not recognized`

**Solution:**
1. Python is not installed or not in PATH
2. Try `python3` instead of `python`
3. Reinstall Python and check "Add Python to PATH"

### Virtual Environment Not Activating

**Problem:** `(venv)` doesn't appear in terminal

**Solution:**
- Windows: Check your terminal is PowerShell/CMD, not another shell
- Mac/Linux: Ensure you used `source` command
- Try: `python -m venv venv --system-site-packages`

### Module Not Found Error

**Problem:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
1. Verify virtual environment is activated (see `(venv)`)
2. Run: `pip install -r requirements.txt`
3. Check pip is pointing to venv: `which pip`

### Port Already in Use

**Problem:** `Address already in use` on port 5000

**Solution:**
```bash
# Find process using port 5000
netstat -ano | findstr :5000  # Windows
lsof -i :5000  # Mac/Linux

# Kill the process or use different port
python run.py  # Default port 5000
# OR modify run.py to use different port (e.g., 5001)
```

### Database Errors

**Problem:** `sqlite3.DatabaseError` or `database is locked`

**Solution:**
1. Delete `bookstore.db` file
2. Restart the application
3. Database will be recreated with fresh data

### Static Files Not Loading

**Problem:** CSS/JavaScript not loading (404 errors)

**Solution:**
1. Verify project structure is correct
2. Check `static/` directory exists
3. Restart the application
4. Hard refresh browser (Ctrl+Shift+R)

---

## Configuration

### Environment Variables (Optional)

Create a `.env` file for configuration:

```bash
FLASK_ENV=development
FLASK_APP=run.py
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///bookstore.db
```

Load environment variables (optional):
```bash
# Windows
set FLASK_ENV=development

# Mac/Linux
export FLASK_ENV=development
```

### Modify Configuration

Edit `config.py` to customize:
- Database location
- Secret key
- Session timeout
- Max file upload size
- Debug settings

---

## First-Time Setup

When you run the application for the first time:

1. **Database Created:** `bookstore.db` is generated automatically
2. **Tables Created:** All database tables are set up
3. **Sample Data:** Sample books and categories are added
4. **Admin User Created:** 
   - Email: `admin@bookstore.com`
   - Password: `admin123`

---

## Using the Application

### Create User Account

1. Go to `http://localhost:5000`
2. Click "Register"
3. Fill in the registration form
4. Click "Register"

### Login

1. Click "Login"
2. Enter your credentials
3. Click "Login"

### Browse Books

1. Click "Books" in navigation
2. Search or filter by category
3. Click on a book to see details

### Admin Access

1. Login with admin credentials
2. Click your name → "Admin Panel"
3. Manage books, categories, orders, users

---

## Development Workflow

### Editing Code

1. Edit Python files in the `app/` directory
2. Flask will auto-reload on changes (debug mode)
3. Refresh browser to see changes

### Adding Dependencies

If you need a new package:
```bash
pip install package-name
pip freeze > requirements.txt
```

### Database Changes

If you modify models:
1. Delete `bookstore.db`
2. Restart application
3. Database recreates with new schema

### Deactivating Virtual Environment

When done working:
```bash
deactivate
```

---

## Production Deployment

### Before Deploying

1. Set `DEBUG=False` in `config.py`
2. Generate a strong `SECRET_KEY`
3. Use PostgreSQL instead of SQLite
4. Set up environment variables
5. Use production WSGI server (Gunicorn)

### Deploy to PythonAnywhere

1. Create account at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload files
3. Create web app with Flask
4. Configure WSGI file
5. Reload web app

### Deploy to Heroku

```bash
# Install Heroku CLI
heroku create your-app-name

# Create Procfile with:
# web: gunicorn run:app

git push heroku main
```

### Deploy to DigitalOcean

1. Create Droplet
2. SSH into server
3. Clone repository
4. Set up virtual environment
5. Install Gunicorn
6. Set up Nginx reverse proxy
7. Configure SSL

---

## Updating the Application

To update to the latest version:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

---

## Uninstallation

To completely remove the application:

1. Deactivate virtual environment: `deactivate`
2. Delete project directory
3. Delete virtual environment folder

```bash
# Full cleanup
rm -rf online-bookstore  # Project folder
rm -rf venv  # Virtual environment
```

---

## Getting Help

### Documentation
- See [README.md](../README.md) for overview
- See [USER_MANUAL.md](USER_MANUAL.md) for usage guide
- See [DATABASE_DESIGN.md](DATABASE_DESIGN.md) for database info

### Common Issues
- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Review error messages carefully
- Check browser console (F12)

### Support
- Email: support@bookstore.com
- Issues: GitHub Issues
- Bugs: bugs@bookstore.com

---

## Verification Checklist

After installation, verify:

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip list` shows Flask, SQLAlchemy, etc.)
- [ ] Application runs without errors (`python run.py`)
- [ ] Browser shows home page at `http://localhost:5000`
- [ ] Can register new user
- [ ] Can login with credentials
- [ ] Admin panel accessible
- [ ] Database file exists (`bookstore.db`)
- [ ] Static files load (CSS/JavaScript)

---

**Installation Guide Version:** 1.0  
**Last Updated:** January 28, 2024  
**Status:** Ready for Development
