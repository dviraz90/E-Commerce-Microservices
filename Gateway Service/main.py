from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)
auth_service_url = 'http://localhost:5000'
product_service_url = 'http://localhost:5001'
order_service_url = 'http://localhost:5002'
user_service_url = 'http://localhost:5003'
support_service_url = 'http://localhost:5004'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def authenticate_token(token):
    response = requests.post(f'{auth_service_url}/verify_token', json={'token': token})
    if response.status_code != 200:
        logger.error('Failed to verify token: %s', response.json().get('message', ''))
        return False
    return response.json()['valid']


@app.route('/products')
def get_products():
    token = request.headers.get('Authorization')
    if not token or not authenticate_token(token):
        return jsonify({'message': 'Unauthorized'}), 401

    response = requests.get(f'{product_service_url}/products')
    return jsonify(response.json())


@app.route('/orders', methods=['POST'])
def create_order():
    token = request.headers.get('Authorization')
    if not token or not authenticate_token(token):
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.json
    response = requests.post(f'{order_service_url}/orders', json=data)
    return jsonify(response.json())


@app.route('/users')
def get_users():
    token = request.headers.get('Authorization')
    if not token or not authenticate_token(token):
        return jsonify({'message': 'Unauthorized'}), 401

    response = requests.get(f'{user_service_url}/users')
    return jsonify(response.json())


@app.route('/support')
def get_support_tickets():
    token = request.headers.get('Authorization')
    if not token or not authenticate_token(token):
        return jsonify({'message': 'Unauthorized'}), 401

    response = requests.get(f'{support_service_url}/support')
    return jsonify(response.json())


if __name__ == '__main__':
    app.run(debug=True)