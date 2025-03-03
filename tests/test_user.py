# tests/test_user.py
import pytest

def test_profile_view(client, auth):
    """Test user profile view"""
    # Login
    auth.login()
    
    # Access profile page
    response = client.get('/user/profile')
    assert response.status_code == 200
    assert b'Profile Information' in response.data
    assert b'user@example.com' in response.data
    
def test_profile_update(client, auth, app):
    """Test user profile update"""
    # Login
    auth.login()
    
    # Update profile
    response = client.post(
        '/user/profile',
        data={
            'username': 'updated_user',
            'email': 'user@example.com',  # Keep same email
            'company': 'Updated Company'
        },
        follow_redirects=True
    )
    
    assert response.status_code == 200
    assert b'Profile updated successfully!' in response.data
    assert b'updated_user' in response.data
    assert b'Updated Company' in response.data
    
    # Verify changes in database
    with app.app_context():
        from app.models.user import User
        user = User.query.filter_by(email='user@example.com').first()
        assert user.username == 'updated_user'
        assert user.company == 'Updated Company'

def test_change_password(client, auth, app):
    """Test change password functionality"""
    # Login
    auth.login()
    
    # Change password
    response = client.post(
        '/user/change-password',
        data={
            'current_password': 'userpassword',
            'new_password': 'newpassword123',
            'confirm_password': 'newpassword123'
        },
        follow_redirects=True
    )
    
    assert response.status_code == 200
    assert b'Password changed successfully!' in response.data
    
    # Verify by logging in with new password
    auth.logout()
    response = auth.login(password='newpassword123')
    assert response.headers['Location'] == '/prices/dashboard'
    
    # Test with incorrect current password
    auth.logout()
    auth.login()
    response = client.post(
        '/user/change-password',
        data={
            'current_password': 'wrongpassword',
            'new_password': 'anotherpassword',
            'confirm_password': 'anotherpassword'
        },
        follow_redirects=True
    )
    
    assert b'Current password is incorrect' in response.data