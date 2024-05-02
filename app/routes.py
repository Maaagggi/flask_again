from flask import jsonify, request
from flask_jwt_extended import create_access_token

from app import app

# Updated users dictionary with username, password, and id attributes
users = {
    'user1': {'username': 'user1', 'password': 'password1', 'id': 1},
    'user2': {'username': 'user2', 'password': 'password2', 'id': 2}
}


# Task list dictionary
tasks = {}


@app.route('/login', methods='POST')
def login():
    data = request.get_json()
    username = data.get('username', None)
    password = data.get('password', None)

    if not username or not password:
        return jsonify({'message': 'Username or password is missing'}), 400

    if username not in users or users[username]['password'] != password:
        return jsonify({'message': 'Invalid username or password'}), 401

    access_token = create_access_token(identity=username)
    return jsonify({'access_token': access_token}), 200


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username', None)
    password = data.get('password', None)

    if not username or not password:
        return jsonify({'message': 'Username or password is missing'}), 400

    if username in users:
        return jsonify({'message': 'Username already exists'}), 400

    # Generate a new user ID
    user_id = max(users.values(), key=lambda x: x['id'])['id'] + 1 if users else 1

    # Add the new user to the users dictionary
    users[username] = {'username': username, 'password': password, 'id': user_id}

    return jsonify({'message': 'User registered successfully', 'user': users[username]}), 200
