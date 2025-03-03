# app/utils/access_control.py
from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def premium_required(f):
    """Decorator to restrict access to premium users"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_premium():
            flash('This feature requires a premium subscription.', 'warning')
            return redirect(url_for('user.profile'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to restrict access to admin users"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            flash('This feature requires administrator privileges.', 'danger')
            return redirect(url_for('user.profile'))
        return f(*args, **kwargs)
    return decorated_function