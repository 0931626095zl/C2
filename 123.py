from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime, timedelta
import random
import string

app = Flask(__name__)

DATABASE = 'data.db'

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def create_user(username, password, lever, date_end):
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (username, password, lever, date_end) VALUES (?,?,?,?)", (username, password, lever, date_end))
    db.commit()
    db.close()

def check_user(username):
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    db.close()
    return user

def send(client, message, success):
    # Placeholder for your send function
    pass

@app.route('/api', methods=['GET'])
def api():
    user = request.args.get('user')
    password = request.args.get('pass')
    lever = request.args.get('lever')
    date_param = request.args.get('date')

    # Check if user, password, and lever are provided
    if not user or not password or not lever:
        return jsonify({'message': 'User, password, and lever are required', 'success': False})

    # Check if the user already exists
    existing_user = check_user(user)
    if existing_user:
        return jsonify({'message': 'User already exists', 'success': False})

    # Generate a random password if not provided
    if not password:
        password = generate_random_string(8)

    # Calculate the expiration date
    current_date = datetime.now()
    expiration_date = current_date + timedelta(days=1)  # 24 hours from now

    # Convert expiration_date to the desired format (yyyy-mm-dd)
    expiration_date_str = expiration_date.strftime('%Y-%m-%d')

    # Create the user with the specified lever
    create_user(user, password, lever, expiration_date_str)

    # Send response
    send('dummy_client', f'User created with user: {user}, password: {password}, lever: {lever}', True)
    return jsonify({'message': f'User created with user: {user}, password: {password}, lever: {lever}', 'success': True})

if __name__ == '__main__':
    app.run(debug=True, port=8080)
