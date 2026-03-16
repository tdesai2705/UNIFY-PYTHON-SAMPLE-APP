"""
Unit tests for the Flask application
"""
import pytest
from app import app, add_numbers, multiply_numbers


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home(client):
    """Test home endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Welcome to the Python Sample App!'
    assert data['status'] == 'success'


def test_health(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'python-sample-app'


def test_greet(client):
    """Test greeting endpoint"""
    response = client.get('/api/greet/John')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Hello, John!'
    assert data['status'] == 'success'


def test_add_numbers():
    """Test add_numbers function"""
    assert add_numbers(2, 3) == 5
    assert add_numbers(-1, 1) == 0
    assert add_numbers(0, 0) == 0


def test_multiply_numbers():
    """Test multiply_numbers function"""
    assert multiply_numbers(2, 3) == 6
    assert multiply_numbers(5, 5) == 25
    assert multiply_numbers(0, 10) == 0
