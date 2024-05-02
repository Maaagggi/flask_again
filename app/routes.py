from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from app import app
import logging
import uuid

app.logger.setLevel(logging.DEBUG)

data_store = {
    'users': [],
    'tasks': []
}


def generate_next_id(data):
    return len(data) + 1


def find_user(uid):
    for user in data_store['users']:
        if user['uid'] == uid:
            return user
    return None


@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    if find_user(username):
        return jsonify({"error": "Username taken"}), 400

    user_id = uuid.uuid4()
    new_user = {'username': username, 'password': password, 'uid': user_id}
    data_store['users'].append(new_user)  # Add user to the list

    # Print user data and data store after registration
    app.logger.debug(f"Registered user: {username}, {password}")
    app.logger.debug(data_store['users'])

    return jsonify({"message": "User registered"}), 201


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    # Find the uid using the username
    uid = None  # Initialize uid
    for user in data_store['users']:
        if user['username'] == username:
            uid = user['uid']
            break  # Exit the loop once you find the user

    # Handle invalid username
    if not uid:
        return jsonify({"error": "Invalid username or password"}), 401

    # Find user details using uid
    user = find_user(uid)

    app.logger.debug(user['password'])  # to check if the passwords or a match
    app.logger.debug(password)

    if not user or user['password'] != password:
        return jsonify({"error": "Invalid username or password"}), 401

    access_token = create_access_token(identity=user['username'])

    # Print user data and data store after login
    app.logger.debug(f"""
    Logged-in user: {username}, {password}
    Updated data store: {data_store['users']}
    User with ID {user.get('id')} logged in successfully
    """)

    return jsonify({"access_token": access_token, "message": "Login successful"})


@app.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    task_data = request.get_json()
    current_user_id = get_jwt_identity()

    task_id = uuid.uuid4()
    new_task = {
        'id': task_id,
        'title': task_data['title'],
        'user_id': current_user_id
    }
    data_store['tasks'].append(new_task)

    return jsonify({"message": "Task created"}), 201


@app.route('/view')
@jwt_required()
def view_tasks():
    current_user_id = get_jwt_identity()
    user_tasks = [task for task in data_store['tasks'] if task['user_id'] == current_user_id]

    return jsonify(user_tasks)
