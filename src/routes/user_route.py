from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from src.utils.auth_utils import *
from src.models.user_schema import *
from src.utils.db_utils import *

# Create a Blueprint for user-related routes
user_bp = Blueprint('user_bp', __name__)


# Define a route for user registration
@user_bp.route('/register', methods=['POST'])
def register():
    """
    Handle user registration.
    """
    try:
        data = user_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    if get_user_by_username(data['username']) is not None:
        return jsonify({'message': 'Username already exists.'}), 400

    user_data = {
        'username': data['username'],
        'password': hash_password(data['password']),
        'created_at': datetime.now(),
        'updated_at': datetime.now()
    }
    try:
        add_new_users(user_data)
    except Exception as e:
        return jsonify({'message': 'An error occurred while registering the user.', 'error': str(e)}), 500

    return jsonify({'message': 'User registered successfully!'}), 201


@user_bp.route('/login', methods=['POST'])
def login():
    """
    Handle user login.
    """
    try:
        data = user_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    user = get_user_by_username(data['username'])
    if user is None:
        return jsonify({'message': 'Invalid username or password.'}), 401

    if not is_valid_password(user['password'], data['password']):
        return jsonify({'message': 'Invalid username or password.'}), 401

    access_token = create_access_token(identity=user['username'])
    return jsonify({'access_token': access_token}), 200
