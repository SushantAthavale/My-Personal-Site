from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='static')

VALID_USERS = {
    'admin': 'password123',
    'user@caspro.in': 'demo1234',
}

@app.route('/')
def index():
    return send_from_directory('.', 'Login.html')

@app.route('/login', methods=['POST'])
def login():
    user_id = request.form.get('userId', '').strip()
    password = request.form.get('password', '')

    if not user_id or not password:
        return jsonify(success=False, error='Enter both your user ID and password.'), 400

    if len(password) < 4:
        return jsonify(success=False, error='That password looks too short.'), 400

    expected_password = VALID_USERS.get(user_id.lower())
    if expected_password and expected_password == password:
        return jsonify(success=True, message='Welcome back, ' + user_id + '!')

    return jsonify(success=False, error='Invalid credentials. Please try again.'), 401

@app.route('/dashboard')
def dashboard():
    return '<h1>Dashboard</h1><p>Signed in successfully. Replace this with your real portal.</p>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
