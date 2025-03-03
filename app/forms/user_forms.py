# app/forms/user_forms.py
from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SelectField, BooleanField, 
    SubmitField, FloatField
)
from wtforms.validators import (
    DataRequired, Length, Email, EqualTo, ValidationError,
    Optional
)
from app.models.user import User
from flask_login import current_user

class ProfileForm(FlaskForm):
    """Form for user profile information"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    company = StringField('Company')
    submit = SubmitField('Update Profile')
    
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already taken. Please choose a different one.')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already registered. Please use a different one.')

class PasswordChangeForm(FlaskForm):
    """Form for changing password"""
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long.')
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match.')
    ])
    submit = SubmitField('Change Password')

class PreferencesForm(FlaskForm):
    """Form for user preferences"""
    # Dashboard preferences
    default_dashboard = SelectField('Default Dashboard', choices=[
        ('prices', 'Price Intelligence'),
        ('production', 'Production Tracking'),
        ('market', 'Market Analytics'),
        ('news', 'News & Research')
    ])
    
    # Chart preferences
    chart_color_theme = SelectField('Chart Color Theme', choices=[
        ('default', 'Default Blue'),
        ('green', 'Green'),
        ('red', 'Red'),
        ('gray', 'Grayscale'),
        ('rainbow', 'Rainbow')
    ])
    default_chart_type = SelectField('Default Chart Type', choices=[
        ('line', 'Line Chart'),
        ('bar', 'Bar Chart'),
        ('candlestick', 'Candlestick Chart')
    ])
    
    # Notification preferences
    email_notifications = BooleanField('Email Notifications')
    notification_frequency = SelectField('Notification Frequency', choices=[
        ('daily', 'Daily Digest'),
        ('weekly', 'Weekly Summary'),
        ('realtime', 'Real-time Alerts')
    ])
    
    # Display preferences
    items_per_page = SelectField('Items Per Page', choices=[
        ('10', '10'),
        ('25', '25'),
        ('50', '50'),
        ('100', '100')
    ])
    date_format = SelectField('Date Format', choices=[
        ('mm/dd/yyyy', 'MM/DD/YYYY'),
        ('dd/mm/yyyy', 'DD/MM/YYYY'),
        ('yyyy-mm-dd', 'YYYY-MM-DD')
    ])
    
    submit = SubmitField('Save Preferences')

class AlertForm(FlaskForm):
    """Form for user alerts"""
    alert_type = SelectField('Alert Type', choices=[
        ('price_change', 'Price Change'),
        ('price_threshold', 'Price Threshold'),
        ('production_announcement', 'Production Announcement'),
        ('news_keyword', 'News Keyword'),
        ('supply_deficit', 'Supply Deficit Warning')
    ])
    threshold = FloatField('Threshold Value', validators=[Optional()])
    frequency = SelectField('Alert Frequency', choices=[
        ('daily', 'Daily'),
        ('realtime', 'Real-time')
    ])
    submit = SubmitField('Save Alert')