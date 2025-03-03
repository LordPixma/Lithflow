# tests/test_auth.py
import pytest
from flask import g, session
from app.models.user import User

def test_login(client, auth):
    """Test user login functionality"""
    # Test login page loads
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Log In' in response.data
    
    # Test login with correct credentials
    response = auth.login()
    assert response.headers['Location'] == '/prices/dashboard'
    
    # Test login with incorrect password
    response = auth.login(password='wrongpassword')
    assert b'Invalid email or password' in response.data
    
    # Test login with non-existent user
    response = auth.login(email='nonexistent@example.com')
    assert b'Invalid email or password' in response.data

def test_logout(client, auth):
    """Test user logout functionality"""
    auth.login()
    
    response = auth.logout()
    assert response.headers['Location'] == '/auth/login'
    
    # Check that user is logged out by trying to access a protected page
    response = client.get('/prices/dashboard', follow_redirects=True)
    assert b'Log In' in response.data

def test_register(client, app):
    """Test user registration functionality"""
    # Test register page loads
    response = client.get('/auth/register')
    assert response.status_code == 200
    assert b'Register' in response.data
    
    # Test successful registration
    response = client.post(
        '/auth/register',
        data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'company': 'New Company',
            'password': 'newpassword',
            'confirm_password': 'newpassword'
        }
    )
    assert response.headers['Location'] == '/auth/login'
    
    # Verify user was created in the database
    with app.app_context():
        user = User.query.filter_by(email='newuser@example.com').first()
        assert user is not None
        assert user.username == 'newuser'
        assert user.company == 'New Company'
        assert user.role == 'basic'
    
    # Test registration with existing username
    response = client.post(
        '/auth/register',
        data={
            'username': 'user',  # Existing username
            'email': 'another@example.com',
            'password': 'newpassword',
            'confirm_password': 'newpassword'
        }
    )
    assert b'Username already taken' in response.data
    
    # Test registration with existing email
    response = client.post(
        '/auth/register',
        data={
            'username': 'anotheruser',
            'email': 'user@example.com',  # Existing email
            'password': 'newpassword',
            'confirm_password': 'newpassword'
        }
    )
    assert b'Email already registered' in response.data
