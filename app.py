from flask import Flask, request, jsonify, g, render_template, session, redirect, url_for
import sqlite3
from werkzeug.security import check_password_hash
import os

# By default, Flask looks for templates in a 'templates' folder.
# The static folder is also 'static' by default, so we don't need to specify them.
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24) # Needed for session management

# --- Configuration ---
# CMI.db is the application database shipped with this project.  app.db is an
# empty placeholder, so using it causes `/login` to fail with "no such table:
# users".
DATABASE = 'CMI.db'

# Get the absolute path of the directory where this script is located
script_dir = os.path.abspath(os.path.dirname(__file__))
# Create the full path to the database, making the connection more robust.
db_path = os.path.join(script_dir, DATABASE)

# --- Database Health Check ---
# Check if the database exists on startup to provide a clear error message.
if not os.path.exists(db_path):
    print("="*80)
    print(f"ERROR: Database file not found at '{db_path}'")
    print("Please initialize the database by running the following command from your terminal:")
    print("\n  python init_db.py\n")
    print("="*80)
    # We exit here because the application is not in a runnable state.
    exit(1)

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
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
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
    try:
        user = db.execute('SELECT * FROM users WHERE username = ?', (user_id.lower(),)).fetchone()
    except sqlite3.Error:
        # Keep this endpoint's API contract consistent: the frontend expects
        # JSON on an unsuccessful login, not Flask's HTML 500 error page.
        app.logger.exception('Database error while processing login')
        return jsonify(success=False, error='The login service is temporarily unavailable. Please try again later.'), 503

    # check_password_hash handles the secure comparison.
    if user and check_password_hash(user['password'], password):
        # Store user info in the session to keep them logged in.
        session.clear()
        session['user_id'] = user['username']
        # The user_id from the form has the original casing, which is nicer for display.
        session['user_display_name'] = user_id
        # On success, redirect to the dashboard. The client-side JS will handle this.
        return redirect(url_for('dashboard'))
    else:
        # Generic error message for security
        return jsonify(success=False, error='Invalid credentials. Please try again.'), 401

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html', username=session.get('user_display_name'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    # Set debug=True for local development to enable auto-reloading on code changes.
    app.run(host='0.0.0.0', port=port, debug=True)
