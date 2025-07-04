import sqlite3
import logging
import json

LOG_LEVEL = logging.INFO

logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')

def load_db_name_from_config():
    """Loads the database name from the config file."""
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            return config['DB_NAME']
    except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        logging.critical(f"FATAL: Could not load DB_NAME from config.json: {e}. Exiting.")
        exit(1)

DB_NAME = load_db_name_from_config()

def setup_database():
    """
    Initializes the database and creates the necessary tables if they don't exist.
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # --- Create Users Table ---
        # Stores account information. Usernames must be unique.
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role INTEGER NOT NULL DEFAULT 100,
            failed_login_attempts INTEGER NOT NULL DEFAULT 0,
            lockout_until DATETIME,
            is_locked BOOLEAN NOT NULL DEFAULT 0
        )''')
        logging.info("'users' table created or already exists.")

        # --- Create Characters Table ---
        # Stores character data, linked to a user account.
        # This schema is ready for when we add character creation logic.
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL UNIQUE,
            time_period TEXT NOT NULL,
            archetype TEXT NOT NULL,
            char_class_name TEXT NOT NULL,
            level INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )''')
        logging.info("'characters' table created or already exists.")

        # --- Create Monster Templates Table ---
        # Defines the base stats and properties of a monster type.
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS monster_templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            archetype TEXT NOT NULL,
            char_class_name TEXT NOT NULL,
            agility INTEGER NOT NULL DEFAULT 10,
            constitution INTEGER NOT NULL DEFAULT 10,
            strength INTEGER NOT NULL DEFAULT 10,
            intelligence INTEGER NOT NULL DEFAULT 10,
            spirit INTEGER NOT NULL DEFAULT 10,
            wisdom INTEGER NOT NULL DEFAULT 10
        )''')
        logging.info("'monster_templates' table created or already exists.")

        # --- Create Monster Spawns Table ---
        # Defines where monsters appear in the world.
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS monster_spawns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            monster_template_id INTEGER NOT NULL,
            zone_name TEXT NOT NULL,
            level INTEGER NOT NULL DEFAULT 1,
            category TEXT NOT NULL DEFAULT 'Common',
            quantity INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (monster_template_id) REFERENCES monster_templates(id) ON DELETE CASCADE
        )''')
        logging.info("'monster_spawns' table created or already exists.")

        # --- Populate with initial monster data ---
        # Using INSERT OR IGNORE to prevent errors on subsequent runs
        cursor.execute('''
        INSERT OR IGNORE INTO monster_templates (name, archetype, char_class_name, agility, constitution, strength, intelligence, spirit, wisdom)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', ("Ancient Gear-Serpent", "Tank", "Flameblade", 15, 9, 6, 10, 8, 12))

        conn.commit()
        conn.close()
        logging.info(f"Database '{DB_NAME}' setup complete.")

    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")

if __name__ == "__main__":
    setup_database()