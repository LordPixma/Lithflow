# app/models/user.py
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from app import db, login_manager
import datetime

class User(UserMixin, db.Model):
    """User model for authentication and profile information"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    company = db.Column(db.String(120))
    role = db.Column(db.String(20), default='basic')  # basic, premium, admin
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    preferences = db.relationship('UserPreference', backref='user', lazy=True)
    alerts = db.relationship('UserAlert', backref='user', lazy=True)
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_premium(self):
        return self.role in ('premium', 'admin')
    
    def is_admin(self):
        return self.role == 'admin'
    
    def __repr__(self):
        return f'<User {self.username}>'

class UserPreference(db.Model):
    """User preferences for dashboard customization"""
    __tablename__ = 'user_preferences'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    preference_key = db.Column(db.String(50), nullable=False)
    preference_value = db.Column(db.String(255))
    
    def __repr__(self):
        return f'<UserPreference {self.preference_key}>'

class UserAlert(db.Model):
    """User alert settings"""
    __tablename__ = 'user_alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    alert_type = db.Column(db.String(50), nullable=False)
    threshold = db.Column(db.Float)
    frequency = db.Column(db.String(20), default='daily')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    def __repr__(self):
        return f'<UserAlert {self.alert_type}>'

class AnonymousUser(AnonymousUserMixin):
    """Anonymous user class for Flask-Login"""
    
    def is_premium(self):
        return False
    
    def is_admin(self):
        return False

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

