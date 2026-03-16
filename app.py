"""
Simple Flask application for CloudBees Unify CI/CD demo
Version: 1.1.0-staging
"""
from flask import Flask, jsonify

app = Flask(__name__)
app.config['ENV'] = 'staging'


@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        'message': 'Welcome to the Python Sample App!',
        'status': 'success'
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


def add_numbers(a, b):
    """Add two numbers"""
    return a + b


def multiply_numbers(a, b):
    """Multiply two numbers"""
    return a * b


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
