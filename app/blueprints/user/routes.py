# app/blueprints/user/routes.py
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.blueprints.user import user_bp
from app.models.user import User, UserPreference, UserAlert
from app.forms.user_forms import (
    ProfileForm, PasswordChangeForm, PreferencesForm, AlertForm
)
from app import db
import datetime

@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile management view"""
    form = ProfileForm(obj=current_user)
    
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.company = form.company.data
        
        # Email change requires additional validation in a real app
        # For demo, we'll just update it
        current_user.email = form.email.data
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('user.profile'))
    
    return render_template(
        'user/profile.html',
        form=form
    )

@user_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change password view"""
    form = PasswordChangeForm()
    
    if form.validate_on_submit():
        # Verify current password
        if current_user.verify_password(form.current_password.data):
            current_user.password = form.new_password.data
            db.session.commit()
            flash('Password changed successfully!', 'success')
            return redirect(url_for('user.profile'))
        else:
            flash('Current password is incorrect.', 'danger')
    
    return render_template(
        'user/change_password.html',
        form=form
    )

@user_bp.route('/preferences', methods=['GET', 'POST'])
@login_required
def preferences():
    """User preferences management view"""
    # Get existing preferences
    existing_prefs = {}
    for pref in current_user.preferences:
        existing_prefs[pref.preference_key] = pref.preference_value
    
    form = PreferencesForm(data=existing_prefs)
    
    if form.validate_on_submit():
        # Update default dashboard
        update_preference('default_dashboard', form.default_dashboard.data)
        
        # Update chart preferences
        update_preference('chart_color_theme', form.chart_color_theme.data)
        update_preference('default_chart_type', form.default_chart_type.data)
        
        # Update notification preferences
        update_preference('email_notifications', str(form.email_notifications.data))
        update_preference('notification_frequency', form.notification_frequency.data)
        
        # Update display preferences
        update_preference('items_per_page', form.items_per_page.data)
        update_preference('date_format', form.date_format.data)
        
        flash('Preferences updated successfully!', 'success')
        return redirect(url_for('user.preferences'))
    
    return render_template(
        'user/preferences.html',
        form=form
    )

def update_preference(key, value):
    """Helper function to update user preference"""
    # Check if preference exists
    pref = UserPreference.query.filter_by(
        user_id=current_user.id,
        preference_key=key
    ).first()
    
    if pref:
        # Update existing preference
        pref.preference_value = value
    else:
        # Create new preference
        pref = UserPreference(
            user_id=current_user.id,
            preference_key=key,
            preference_value=value
        )
        db.session.add(pref)
    
    db.session.commit()

@user_bp.route('/alerts', methods=['GET'])
@login_required
def alerts():
    """User alerts management view"""
    user_alerts = UserAlert.query.filter_by(user_id=current_user.id).all()
    
    return render_template(
        'user/alerts.html',
        alerts=user_alerts
    )

@user_bp.route('/alerts/add', methods=['GET', 'POST'])
@login_required
def add_alert():
    """Add new alert view"""
    form = AlertForm()
    
    if form.validate_on_submit():
        alert = UserAlert(
            user_id=current_user.id,
            alert_type=form.alert_type.data,
            threshold=form.threshold.data,
            frequency=form.frequency.data,
            is_active=True
        )
        
        db.session.add(alert)
        db.session.commit()
        
        flash('Alert added successfully!', 'success')
        return redirect(url_for('user.alerts'))
    
    return render_template(
        'user/add_alert.html',
        form=form
    )

@user_bp.route('/alerts/<int:alert_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_alert(alert_id):
    """Edit existing alert view"""
    alert = UserAlert.query.get_or_404(alert_id)
    
    # Verify ownership
    if alert.user_id != current_user.id:
        flash('You do not have permission to edit this alert.', 'danger')
        return redirect(url_for('user.alerts'))
    
    form = AlertForm(obj=alert)
    
    if form.validate_on_submit():
        alert.alert_type = form.alert_type.data
        alert.threshold = form.threshold.data
        alert.frequency = form.frequency.data
        
        db.session.commit()
        
        flash('Alert updated successfully!', 'success')
        return redirect(url_for('user.alerts'))
    
    return render_template(
        'user/edit_alert.html',
        form=form,
        alert=alert
    )

@user_bp.route('/alerts/<int:alert_id>/toggle', methods=['POST'])
@login_required
def toggle_alert(alert_id):
    """Toggle alert active status"""
    alert = UserAlert.query.get_or_404(alert_id)
    
    # Verify ownership
    if alert.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Permission denied'}), 403
    
    alert.is_active = not alert.is_active
    db.session.commit()
    
    return jsonify({
        'success': True,
        'is_active': alert.is_active
    })

@user_bp.route('/alerts/<int:alert_id>/delete', methods=['POST'])
@login_required
def delete_alert(alert_id):
    """Delete an alert"""
    alert = UserAlert.query.get_or_404(alert_id)
    
    # Verify ownership
    if alert.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Permission denied'}), 403
    
    db.session.delete(alert)
    db.session.commit()
    
    return jsonify({'success': True})

@user_bp.route('/dashboard')
@login_required
def dashboard():
    """User personal dashboard view"""
    # Get user's default dashboard preference
    default_dashboard = get_user_preference('default_dashboard', 'prices')
    
    # Redirect to appropriate dashboard
    if default_dashboard == 'prices':
        return redirect(url_for('prices.dashboard'))
    elif default_dashboard == 'production':
        return redirect(url_for('production.mine_dashboard'))
    elif default_dashboard == 'market':
        return redirect(url_for('market.supply_demand'))
    elif default_dashboard == 'news':
        return redirect(url_for('news.latest'))
    else:
        return redirect(url_for('prices.dashboard'))

def get_user_preference(key, default=None):
    """Helper function to get user preference"""
    pref = UserPreference.query.filter_by(
        user_id=current_user.id,
        preference_key=key
    ).first()
    
    return pref.preference_value if pref else default