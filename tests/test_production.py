# tests/test_production.py
import pytest
import json

def test_mine_dashboard_requires_login(client):
    """Test that mine dashboard requires login"""
    response = client.get('/production/mine-dashboard')
    assert response.headers['Location'].startswith('/auth/login')

def test_mine_dashboard_access(client, auth):
    """Test access to mine dashboard"""
    auth.login()
    response = client.get('/production/mine-dashboard')
    assert response.status_code == 200
    
def test_mine_data_api(client, auth):
    """Test mine data API endpoint"""
    auth.login()
    response = client.get('/production/api/mine-data')
    assert response.status_code == 200
    
    # Parse JSON response
    data = json.loads(response.data)
    assert isinstance(data, list)
    
    # Check response structure if data exists
    if len(data) > 0:
        assert 'id' in data[0]
        assert 'name' in data[0]
        assert 'country' in data[0]
        
def test_country_production_api(client, auth):
    """Test country production API endpoint"""
    auth.login()
    response = client.get('/production/api/country-production')
    assert response.status_code == 200
    
    # Parse JSON response
    data = json.loads(response.data)
    assert isinstance(data, list)
    
    # Check response structure if data exists
    if len(data) > 0:
        assert 'country' in data[0]
        assert 'mine_production' in data[0]
        assert isinstance(data[0]['mine_production'], (int, float))