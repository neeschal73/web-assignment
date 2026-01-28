from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, NumberRange
from app.models import User

"""
Forms for user registration, login, and profile management
Handles validation for user input
"""


class RegistrationForm(FlaskForm):
    """User registration form"""
    username = StringField('Username', validators=[
        DataRequired(message='Username is required'),
        Length(min=3, max=20, message='Username must be between 3 and 20 characters')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Invalid email address')
    ])
    full_name = StringField('Full Name', validators=[
        DataRequired(message='Full name is required'),
        Length(min=3, max=120, message='Full name must be between 3 and 120 characters')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=6, message='Password must be at least 6 characters')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password'),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        """Check if username already exists"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')
    
    def validate_email(self, email):
        """Check if email already exists"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different one.')


class LoginForm(FlaskForm):
    """User login form"""
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Invalid email address')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required')
    ])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateProfileForm(FlaskForm):
    """User profile update form"""
    full_name = StringField('Full Name', validators=[
        DataRequired(message='Full name is required'),
        Length(min=3, max=120, message='Full name must be between 3 and 120 characters')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Invalid email address')
    ])
    phone = StringField('Phone Number', validators=[
        Length(max=20, message='Phone number must be less than 20 characters')
    ])
    address = StringField('Address', validators=[
        Length(max=255, message='Address must be less than 255 characters')
    ])
    city = StringField('City', validators=[
        Length(max=100, message='City name must be less than 100 characters')
    ])
    postal_code = StringField('Postal Code', validators=[
        Length(max=20, message='Postal code must be less than 20 characters')
    ])
    submit = SubmitField('Update Profile')
    
    def validate_email(self, email):
        """Check if email is already registered to another user"""
        user = User.query.filter_by(email=email.data).first()
        if user and user.email != email.data:
            raise ValidationError('Email already in use. Please use a different one.')


class ReviewForm(FlaskForm):
    """Book review form"""
    rating = IntegerField('Rating (1-5 stars)', validators=[
        DataRequired(message='Rating is required'),
        NumberRange(min=1, max=5, message='Rating must be between 1 and 5')
    ])
    title = StringField('Review Title', validators=[
        DataRequired(message='Review title is required'),
        Length(min=5, max=200, message='Title must be between 5 and 200 characters')
    ])
    content = TextAreaField('Review Content', validators=[
        DataRequired(message='Review content is required'),
        Length(min=10, max=1000, message='Review must be between 10 and 1000 characters')
    ])
    submit = SubmitField('Submit Review')


class ContactForm(FlaskForm):
    """Contact form"""
    name = StringField('Your Name', validators=[
        DataRequired(message='Name is required'),
        Length(min=3, max=120, message='Name must be between 3 and 120 characters')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Invalid email address')
    ])
    subject = StringField('Subject', validators=[
        DataRequired(message='Subject is required'),
        Length(min=5, max=200, message='Subject must be between 5 and 200 characters')
    ])
    message = TextAreaField('Message', validators=[
        DataRequired(message='Message is required'),
        Length(min=10, max=2000, message='Message must be between 10 and 2000 characters')
    ])
    submit = SubmitField('Send Message')
