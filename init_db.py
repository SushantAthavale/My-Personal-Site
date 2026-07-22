import sqlite3
from werkzeug.security import generate_password_hash
import os

DB_FILE = 'CMI.db'
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, DB_FILE)

# --- Safety Check ---
# To prevent accidentally overwriting the database, check if it exists.
# If you need to reset the database, manually delete 'CMI.db' and rerun this script.
if os.path.exists(DB_PATH):
    print(f"Database file '{DB_PATH}' already exists. Aborting initialization.")
    print("If you want to re-create the database, please delete the file and run this script again.")
    exit()

print(f"Creating new database '{DB_FILE}'...")

# Use a 'with' statement for robust connection handling.
# It automatically handles commits on success and closes the connection.
with sqlite3.connect(DB_PATH) as connection:
    cursor = connection.cursor()

    # Create the users table
    cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );
    ''')

    # --- User Data ---
    users_to_add = {
        'admin': 'CMI-Admin@0962',
        'user@caspro.in': 'demo1234',
    }

    for username, password in users_to_add.items():
        hashed_password = generate_password_hash(password)
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username.lower(), hashed_password))

print(f"Database '{DB_PATH}' initialized successfully with {len(users_to_add)} users.")