from flask import Flask, request, jsonify, g, render_template
import sqlite3
from werkzeug.security import check_password_hash
import os

# By default, Flask looks for templates in a 'templates' folder.
# The static folder is also 'static' by default, so we don't need to specify them.
app = Flask(__name__)

# --- Configuration ---
DATABASE = 'CMI.db'

# Get the absolute path of the directory where this script is located
script_dir = os.path.abspath(os.path.dirname(__file__))
# Create the full path to the database, making the connection more robust.
db_path = os.path.join(script_dir, DATABASE)

def get_db():
    """
    Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called again.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    """Close the database connection at the end of the request."""
    db = g.pop('db', None)

    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('Login.html')

@app.route('/login', methods=['POST'])
def login():
    user_id = request.form.get('userId', '').strip()
    password = request.form.get('password', '').strip()

    if not user_id or not password:
        return jsonify(success=False, error='Enter both your user ID and password.'), 400

    if len(password) < 4:
        return jsonify(success=False, error='That password looks too short.'), 400

    db = get_db()
    user = db.execute('SELECT * FROM users WHERE username = ?', (user_id.lower(),)).fetchone()

    # check_password_hash handles the secure comparison.
    if user and check_password_hash(user['password'], password):
        # The user_id from the form has the original casing, which is nicer to display.
        return jsonify(success=True, message='Welcome back, ' + user_id + '!')
    else:
        # Generic error message for security
        return jsonify(success=False, error='Invalid credentials. Please try again.'), 401

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    # Set debug=True for local development to enable auto-reloading on code changes.
    app.run(host='0.0.0.0', port=port, debug=True)
