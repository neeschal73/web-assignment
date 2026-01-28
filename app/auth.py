from flask_login import LoginManager
from app.models import User

"""
Authentication utilities for Flask-Login integration
"""

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'


@login_manager.user_loader
def load_user(user_id):
    """
    Load user by ID for Flask-Login
    Args:
        user_id: User ID from session
    Returns:
        User object or None
    """
    return User.query.get(int(user_id))
