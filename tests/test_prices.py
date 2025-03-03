# tests/test_prices.py
import pytest
import json
from datetime import datetime, timedelta

def test_price_dashboard_requires_login(client):
    """Test that price dashboard requires login"""
    response = client.get('/prices/dashboard')
    assert response.headers['Location'].startswith('/auth/login')

def test_price_dashboard_access(client, auth):
    """Test access to price dashboard"""
    auth.login()
    response = client.get('/prices/dashboard')
    assert response.status_code == 200
    assert b'Lithium Price Trends' in response.data

def test_price_api_endpoint(client, auth):
    """Test price data API endpoint"""
    auth.login()
    response = client.get('/prices/api/price-data?compound=lithium%20carbonate&region=China&period=1y')
    assert response.status_code == 200
    
    # Parse JSON response
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0
    
    # Check required fields exist
    assert 'date' in data[0]
    assert 'price' in data[0]
    
    # Check data type
    assert isinstance(data[0]['price'], (int, float))

def test_premium_features_access(client, auth):
    """Test access control for premium features"""
    # Login as basic user
    auth.login()
    
    # Try to access premium feature
    response = client.get('/prices/forecast')
    assert response.status_code == 302  # Redirect to profile page
    
    # Login as premium user
    auth.login(email='premium@example.com', password='premiumpassword')
    
    # Access premium feature
    response = client.get('/prices/forecast')
    assert response.status_code == 200
