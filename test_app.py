"""
Unit tests for the Flask application
"""
import pytest
from app import app, add_numbers, multiply_numbers, items


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Reset items to default state before each test
        items.clear()
        items[1] = {'id': 1, 'name': 'Sample Item', 'description': 'This is a sample item'}
        yield client


def test_home(client):
    """Test home endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Welcome to the Python Sample App!'
    assert data['status'] == 'success'
    assert 'documentation' in data


def test_swagger_spec(client):
    """Test Swagger specification endpoint"""
    response = client.get('/swagger.json')
    assert response.status_code == 200
    data = response.get_json()
    assert 'openapi' in data
    assert data['info']['title'] == 'UNIFY Python Sample API'


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


def test_get_items(client):
    """Test get all items endpoint"""
    response = client.get('/api/items')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['count'] == 1
    assert len(data['items']) == 1
    assert data['items'][0]['name'] == 'Sample Item'


def test_get_item_success(client):
    """Test get single item endpoint - success"""
    response = client.get('/api/items/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['item']['id'] == 1
    assert data['item']['name'] == 'Sample Item'


def test_get_item_not_found(client):
    """Test get single item endpoint - not found"""
    response = client.get('/api/items/999')
    assert response.status_code == 404
    data = response.get_json()
    assert data['status'] == 'error'
    assert data['error'] == 'Item not found'


def test_create_item_success(client):
    """Test create item endpoint - success"""
    new_item = {
        'name': 'New Item',
        'description': 'A newly created item'
    }
    response = client.post('/api/items', json=new_item)
    assert response.status_code == 201
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['item']['name'] == 'New Item'
    assert data['item']['description'] == 'A newly created item'
    assert 'id' in data['item']


def test_create_item_missing_name(client):
    """Test create item endpoint - missing name"""
    response = client.post('/api/items', json={'description': 'No name'})
    assert response.status_code == 400
    data = response.get_json()
    assert data['status'] == 'error'
    assert data['error'] == 'Name is required'


def test_create_item_no_data(client):
    """Test create item endpoint - no data"""
    response = client.post('/api/items',
                          json={},
                          content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert data['status'] == 'error'


def test_update_item_success(client):
    """Test update item endpoint - success"""
    update_data = {
        'name': 'Updated Item',
        'description': 'Updated description'
    }
    response = client.put('/api/items/1', json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['item']['name'] == 'Updated Item'
    assert data['item']['description'] == 'Updated description'


def test_update_item_partial(client):
    """Test update item endpoint - partial update"""
    update_data = {'name': 'Partially Updated'}
    response = client.put('/api/items/1', json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['item']['name'] == 'Partially Updated'
    assert data['item']['description'] == 'This is a sample item'


def test_update_item_not_found(client):
    """Test update item endpoint - not found"""
    response = client.put('/api/items/999', json={'name': 'Updated'})
    assert response.status_code == 404
    data = response.get_json()
    assert data['status'] == 'error'
    assert data['error'] == 'Item not found'


def test_update_item_no_data(client):
    """Test update item endpoint - no data"""
    response = client.put('/api/items/1',
                         json={},
                         content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert data['status'] == 'error'


def test_delete_item_success(client):
    """Test delete item endpoint - success"""
    response = client.delete('/api/items/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['message'] == 'Item deleted successfully'
    assert data['item']['id'] == 1

    # Verify item is deleted
    response = client.get('/api/items/1')
    assert response.status_code == 404


def test_delete_item_not_found(client):
    """Test delete item endpoint - not found"""
    response = client.delete('/api/items/999')
    assert response.status_code == 404
    data = response.get_json()
    assert data['status'] == 'error'
    assert data['error'] == 'Item not found'
