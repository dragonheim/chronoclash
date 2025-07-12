import sqlite3
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import json
from functools import wraps

# --- Configuration ---
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
        DB_NAME = config['DB_NAME']
        STATUS_SERVER_URL = config['STATUS_SERVER_URL']
except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
    # Use print for Flask's startup sequence before logging might be configured
    print(f"FATAL: Could not load configuration from config.json: {e}. Exiting.")
    exit(1)

# --- Flask App Initialization ---
app = Flask(__name__)
# This secret key is essential for session management.
# In a production environment, this should be a long, random, and secret string.
app.secret_key = 'dev-secret-key'

# --- Game Data ---
# This data, derived from the GDD, helps the web app understand class options.
CLASS_DEFINITIONS = {
    "Flameblade": {"time_period": "Past", "archetype": "Tank"},
    "Hex Weaver": {"time_period": "Past", "archetype": "DPS"},
    "Cleric": {"time_period": "Past", "archetype": "Healer"},
    "Shocktrooper": {"time_period": "Present", "archetype": "Tank"},
    "Grenadier": {"time_period": "Present", "archetype": "DPS"},
    "Field Medic": {"time_period": "Present", "archetype": "Healer"},
    "Cyberblade": {"time_period": "Future", "archetype": "Tank"},
    "Pulse Mage": {"time_period": "Future", "archetype": "DPS"},
    "Nano-Surgeon": {"time_period": "Future", "archetype": "Healer"},
}

# --- Decorators for Authorization ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You must be logged in to view this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Role 0 is Admin
        if session.get('role') != 0:
            flash('You must be an administrator to access this page.', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def gm_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Role 0 is Admin, Role 10 is GM. Admins can access GM panels.
        if session.get('role') not in [0, 10]:
            flash('You must be a Game Master or Admin to access this page.', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def get_db_connection():
    """Creates a connection to the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.context_processor
def inject_server_status():
    """
    Injects server status variables into the context of all templates.
    This runs for every request, so the status is always fresh.
    """
    status = "Down"
    player_count = 0
    try:
        # Use a short timeout to avoid hanging the web request if the server is unresponsive.
        response = requests.get(STATUS_SERVER_URL, timeout=1)
        if response.status_code == 200:
            status = "Up"
            player_count = len(response.json())
    except requests.exceptions.RequestException:
        # This catches ConnectionError, Timeout, etc. and treats them as "Down".
        pass
    return dict(server_status=status, online_player_count=player_count)

@app.route('/')
def index():
    """
    Main landing page. Redirects to the dashboard if logged in,
    otherwise shows the login page.
    """
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handles user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Username and password are required.', 'error')
            return redirect(url_for('register'))

        # Hash the password for secure storage
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        try:
            conn.execute(
                'INSERT INTO users (username, password_hash) VALUES (?, ?)',
                (username, hashed_password)
            )
            conn.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            # This error occurs if the username is already taken (due to UNIQUE constraint)
            flash('Username already exists. Please choose another.', 'error')
        finally:
            conn.close()

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login and session creation."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        if not user:
            flash('Invalid username or password.', 'error')
            conn.close()
            return render_template('login.html')

        # Check for permanent lock
        if user['is_locked']:
            flash('Your account has been permanently locked. Please contact an administrator.', 'error')
            conn.close()
            return render_template('login.html')

        # Check for temporary lockout
        if user['lockout_until'] and datetime.fromisoformat(user['lockout_until']) > datetime.now():
            remaining_time = datetime.fromisoformat(user['lockout_until']) - datetime.now()
            minutes, seconds = divmod(int(remaining_time.total_seconds()), 60)
            flash(f'Your account is temporarily locked. Please try again in {minutes}m {seconds}s.', 'error')
            conn.close()
            return render_template('login.html')

        if check_password_hash(user['password_hash'], password):
            # Successful login: reset locks and set session
            conn.execute('UPDATE users SET failed_login_attempts = 0, lockout_until = NULL WHERE id = ?', (user['id'],))
            conn.commit()
            conn.close()
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            flash(f'Welcome back, {user["username"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            # Failed login: increment attempts and apply locks if necessary
            new_attempts = user['failed_login_attempts'] + 1
            
            if new_attempts >= 6:
                conn.execute('UPDATE users SET failed_login_attempts = ?, is_locked = 1 WHERE id = ?', (new_attempts, user['id']))
                flash('Too many failed login attempts. Your account has been permanently locked.', 'error')
            elif new_attempts >= 3:
                lockout_time = datetime.now() + timedelta(minutes=30)
                conn.execute('UPDATE users SET failed_login_attempts = ?, lockout_until = ? WHERE id = ?', (new_attempts, lockout_time.isoformat(), user['id']))
                flash('Your account has been temporarily locked for 30 minutes due to multiple failed login attempts.', 'error')
            else:
                conn.execute('UPDATE users SET failed_login_attempts = ? WHERE id = ?', (new_attempts, user['id']))
                flash('Invalid username or password.', 'error')
            
            conn.commit()
            conn.close()
            return render_template('login.html')

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """The main user dashboard, shown after a successful login."""

    # Load the user's characters from the database
    conn = get_db_connection()
    characters = conn.execute(
        'SELECT * FROM characters WHERE user_id = ? ORDER BY name', (session['user_id'],)
    ).fetchall()
    conn.close()

    return render_template('dashboard.html', characters=characters)

@app.route('/logout')
@login_required
def logout():
    """Clears the session to log the user out."""
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/character/delete/<int:char_id>', methods=['POST'])
@login_required
def delete_character(char_id):
    """Handles the deletion of a single character."""
    conn = get_db_connection()
    # Security check: Ensure the character belongs to the logged-in user before deleting.
    character = conn.execute(
        'SELECT * FROM characters WHERE id = ? AND user_id = ?',
        (char_id, session['user_id'])
    ).fetchone()

    if character:
        conn.execute('DELETE FROM characters WHERE id = ?', (char_id,))
        conn.commit()
        flash(f'Character "{character["name"]}" has been deleted.', 'success')
    else:
        # This case handles if someone tries to delete a character that's not theirs or doesn't exist.
        flash('Character not found or you do not have permission to delete it.', 'error')
    
    conn.close()
    return redirect(url_for('dashboard'))

@app.route('/account/delete', methods=['GET', 'POST'])
@login_required
def delete_account():
    """Handles showing the account deletion confirmation page and processing the deletion."""
    if request.method == 'POST':
        conn = get_db_connection()
        conn.execute('DELETE FROM users WHERE id = ?', (session['user_id'],))
        conn.commit()
        conn.close()
        session.clear()
        flash('Your account and all associated characters have been permanently deleted.', 'success')
        return redirect(url_for('register'))

    return render_template('delete_account.html')

@app.route('/character/create', methods=['GET', 'POST'])
@login_required
def create_character():
    """Handles the character creation form and logic."""
    if request.method == 'POST':
        char_name = request.form['char_name']
        char_class = request.form['char_class']

        if not char_name or not char_class:
            flash('Character name and class are required.', 'error')
            return redirect(url_for('create_character'))

        if char_class not in CLASS_DEFINITIONS:
            flash('Invalid class selected.', 'error')
            return redirect(url_for('create_character'))

        class_info = CLASS_DEFINITIONS[char_class]
        time_period = class_info['time_period']
        archetype = class_info['archetype']

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO characters (user_id, name, time_period, archetype, char_class_name) VALUES (?, ?, ?, ?, ?)',
                (session['user_id'], char_name, time_period, archetype, char_class)
            )
            
            # Get the ID of the character we just created
            character_id = cursor.lastrowid

            # As per weapons.md, every character starts with a Rusted Pipe Wrench.
            # We assume its ID is 1 from database_setup.py.
            starting_weapon_id = 1

            # Add the starting weapon to the character's inventory and equip it
            cursor.execute(
                'INSERT INTO character_inventory (character_id, item_id, is_equipped) VALUES (?, ?, ?)',
                (character_id, starting_weapon_id, 1) # 1 for True (equipped)
            )

            conn.commit()
            flash(f'Character "{char_name}" created successfully!', 'success')
            return redirect(url_for('dashboard'))
        except sqlite3.IntegrityError:
            conn.rollback()
            flash(f'A character with the name "{char_name}" already exists.', 'error')
        finally:
            conn.close()
    
    return render_template('create_character.html', classes=CLASS_DEFINITIONS)

# --- Admin Panel Routes ---

@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    """The main landing page for administrators."""
    return render_template('admin_dashboard.html')

@app.route('/admin/users')
@login_required
@admin_required
def list_users():
    """Displays a list of all users for management."""
    conn = get_db_connection()
    users = conn.execute('SELECT id, username, role, failed_login_attempts, lockout_until, is_locked FROM users ORDER BY username').fetchall()
    conn.close()
    return render_template('user_list.html', users=users, now=datetime.now().isoformat())

@app.route('/admin/unlock/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def unlock_user(user_id):
    """Unlocks a user account."""
    conn = get_db_connection()
    conn.execute('UPDATE users SET failed_login_attempts = 0, lockout_until = NULL, is_locked = 0 WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    flash('User account has been unlocked.', 'success')
    return redirect(url_for('list_users'))

# --- GM Panel Routes ---

@app.route('/gm')
@login_required
@gm_required
def gm_dashboard():
    """The main landing page for Game Masters."""
    return render_template('gm_dashboard.html')

@app.route('/gm/online-players')
@login_required
@gm_required
def online_players():
    """Fetches and displays the list of currently online players from the game server."""
    players = []
    try:
        response = requests.get(STATUS_SERVER_URL, timeout=3)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        players = response.json()
    except requests.exceptions.ConnectionError:
        flash('Could not connect to the game server to retrieve the player list. Is it running?', 'error')
    except requests.exceptions.RequestException as e:
        flash(f'An error occurred while fetching the player list: {e}', 'error')
    
    return render_template('online_players.html', players=players)

if __name__ == '__main__':
    # Note: debug=True is for development only.
    # In a production environment, use a proper WSGI server like Gunicorn or Waitress.
    app.run(host='0.0.0.0', port=5000, debug=True)