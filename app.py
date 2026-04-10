"""
Simple Flask application for CloudBees Unify CI/CD demo
Version: 1.1.0-staging
"""
from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
app.config['ENV'] = 'staging'

# Swagger UI configuration
SWAGGER_URL = '/api/docs'
API_URL = '/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "UNIFY Python Sample API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# In-memory storage for items
items = {
    1: {'id': 1, 'name': 'Sample Item', 'description': 'This is a sample item'},
}


@app.route('/swagger.json')
def swagger_spec():
    """Serve Swagger specification"""
    import json
    with open('swagger.json', 'r') as f:
        return jsonify(json.load(f))


@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        'message': 'Welcome to the Python Sample App!',
        'status': 'success',
        'documentation': 'Visit /api/docs for API documentation'
    })


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'python-sample-app'
    })


@app.route('/api/greet/<name>')
def greet(name):
    """Greeting endpoint with parameter"""
    return jsonify({
        'message': f'Hello, {name}!',
        'status': 'success'
    })


@app.route('/api/items', methods=['GET'])
def get_items():
    """Get all items"""
    return jsonify({
        'items': list(items.values()),
        'count': len(items),
        'status': 'success'
    })


@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Get a specific item by ID"""
    item = items.get(item_id)
    if item:
        return jsonify({
            'item': item,
            'status': 'success'
        })
    return jsonify({
        'error': 'Item not found',
        'status': 'error'
    }), 404


@app.route('/api/items', methods=['POST'])
def create_item():
    """Create a new item"""
    data = request.get_json()

    if not data or 'name' not in data:
        return jsonify({
            'error': 'Name is required',
            'status': 'error'
        }), 400

    # Generate new ID
    new_id = max(items.keys()) + 1 if items else 1

    new_item = {
        'id': new_id,
        'name': data['name'],
        'description': data.get('description', '')
    }

    items[new_id] = new_item

    return jsonify({
        'item': new_item,
        'status': 'success'
    }), 201


@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """Update an existing item"""
    if item_id not in items:
        return jsonify({
            'error': 'Item not found',
            'status': 'error'
        }), 404

    data = request.get_json()

    if not data or len(data) == 0:
        return jsonify({
            'error': 'No data provided',
            'status': 'error'
        }), 400

    # Update item
    if 'name' in data:
        items[item_id]['name'] = data['name']
    if 'description' in data:
        items[item_id]['description'] = data['description']

    return jsonify({
        'item': items[item_id],
        'status': 'success'
    })


@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete an item"""
    if item_id not in items:
        return jsonify({
            'error': 'Item not found',
            'status': 'error'
        }), 404

    deleted_item = items.pop(item_id)

    return jsonify({
        'message': 'Item deleted successfully',
        'item': deleted_item,
        'status': 'success'
    })


def add_numbers(a, b):
    """Add two numbers"""
    return a + b


def multiply_numbers(a, b):
    """Multiply two numbers"""
    return a * b


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
