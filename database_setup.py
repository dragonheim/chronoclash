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
        
        # Use executescript to run all schema creation commands at once.
        # This is cleaner and ensures all tables are created together.
        schema_script = """
            -- Users table to store account information
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role INTEGER NOT NULL DEFAULT 20, -- 0=Admin, 10=GM, 20=Player
                failed_login_attempts INTEGER NOT NULL DEFAULT 0,
                lockout_until TEXT, -- ISO 8601 format
                is_locked BOOLEAN NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            -- Zones table to store world locations
            CREATE TABLE IF NOT EXISTS zones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                -- Future: Add level range, PvP status, etc.
                required_level INTEGER NOT NULL DEFAULT 1
            );

            -- Characters table to store player character data
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL UNIQUE,
                time_period TEXT NOT NULL,
                archetype TEXT NOT NULL,
                char_class_name TEXT NOT NULL,
                level INTEGER NOT NULL DEFAULT 1,
                experience INTEGER NOT NULL DEFAULT 0,
                attribute_points INTEGER NOT NULL DEFAULT 0,
                current_hp REAL NOT NULL DEFAULT -1,
                current_mana REAL NOT NULL DEFAULT -1,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            );

            -- NPCs table to store non-player character data
            CREATE TABLE IF NOT EXISTS npcs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                zone_id INTEGER NOT NULL,
                dialogue TEXT,
                role TEXT NOT NULL DEFAULT 'Civilian',
                FOREIGN KEY (zone_id) REFERENCES zones (id)
            );

            -- Monster Templates Table: Defines the base stats of a monster type.
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
            );

            -- Monster Spawns Table: Defines where monsters appear in the world.
            CREATE TABLE IF NOT EXISTS monster_spawns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                monster_template_id INTEGER NOT NULL,
                zone_id INTEGER NOT NULL,
                level INTEGER NOT NULL DEFAULT 1,
                category TEXT NOT NULL DEFAULT 'Common',
                quantity INTEGER NOT NULL DEFAULT 1,
                FOREIGN KEY (monster_template_id) REFERENCES monster_templates(id) ON DELETE CASCADE,
                FOREIGN KEY (zone_id) REFERENCES zones (id),
                UNIQUE(monster_template_id, zone_id)
            );

            -- Items table to store templates for all equippable items.
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                item_type TEXT NOT NULL, -- 'Weapon', 'Armor', 'Accessory'
                slot TEXT NOT NULL, -- 'weapon', 'armor_body', 'accessory1', 'accessory2'
                rarity TEXT NOT NULL DEFAULT 'Common',
                level_req INTEGER NOT NULL DEFAULT 1,
                -- JSON string for bonuses, e.g., '{"AP": 5, "HP": 10}'
                bonuses TEXT,
                -- JSON string for weapon damage, e.g., '{"min": 8, "max": 12, "type": "Bludgeoning"}'
                damage TEXT,
                description TEXT
            );

            -- Character Inventory table to link items to characters.
            CREATE TABLE IF NOT EXISTS character_inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                character_id INTEGER NOT NULL,
                item_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 1,
                is_equipped BOOLEAN NOT NULL DEFAULT 0,
                FOREIGN KEY (character_id) REFERENCES characters(id) ON DELETE CASCADE,
                FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE
            );
        """
        cursor.executescript(schema_script)
        logging.info("Core tables created or already exist.")

        # --- Populate with initial monster data ---
        # Using INSERT OR IGNORE to prevent errors on subsequent runs
        cursor.execute('''
        INSERT OR IGNORE INTO monster_templates (name, archetype, char_class_name, agility, constitution, strength, intelligence, spirit, wisdom)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', ("Temporal Ghoul", "DPS", "Hex Weaver", 12, 8, 10, 5, 5, 5))
        cursor.execute('''
        INSERT OR IGNORE INTO monster_templates (name, archetype, char_class_name, agility, constitution, strength, intelligence, spirit, wisdom)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', ("Ancient Gear-Serpent", "Tank", "Flameblade", 15, 9, 6, 10, 8, 12))
        logging.info("Initial monster templates populated.")

        # --- Populate with initial zone data ---
        zone_script = """
            INSERT OR IGNORE INTO zones (id, name, description, required_level) VALUES (1, 'Seattle', 'The rain-slicked streets of a fractured metropolis, where augmented reality overlays clash with crumbling brickwork.', 1);
            INSERT OR IGNORE INTO zones (id, name, description, required_level) VALUES (2, 'Echo Vale', 'A valley where time-distortions cause whispers of the past and visions of the future to manifest physically.', 1);
        """
        cursor.executescript(zone_script)
        logging.info("Initial zones populated.")

        # --- Populate with initial monster spawn data ---
        spawn_script = """
            -- Monsters spawn in Echo Vale (Zone ID=2)
            INSERT OR IGNORE INTO monster_spawns (monster_template_id, zone_id, level, category, quantity) VALUES (2, 2, 1, 'Common', 3);
            INSERT OR IGNORE INTO monster_spawns (monster_template_id, zone_id, level, category, quantity) VALUES (1, 2, 1, 'Common', 2);
        """
        cursor.executescript(spawn_script)
        logging.info("Initial monster spawns populated.")

        # --- Populate with initial NPC data ---
        npc_script = """
            -- All NPCs are in Seattle (Zone ID=1) for now.
            INSERT OR IGNORE INTO npcs (name, zone_id, role, dialogue) VALUES
            ('Lythia Culverson', 1, 'Master Crafter', 'Time doesn’t care about your labels. It flows forward, backward, sideways—it dances. If you want to survive in this world, learn to dance with it. What can I help you craft?'),
            ('Dr. Elias Kwan', 1, 'Lore Keeper', 'Time is not broken—it is remembered poorly. You are the witness. Now bear it. What piece of history do you seek?'),
            ('Captain Darius Vale', 1, 'Military Leader', 'You want to fight in the Nexus? First you prove you can survive me. The Steel Sentinels are always looking for new recruits.'),
            ('Selene Marrow', 1, 'Paradox Broker', 'I don’t sell things. I trade possibilities. What’s your gamble worth?'),
            ('Sister Evora', 1, 'Side Quest Giver', 'The future may be broken, but hope still fits in small hands. Can you help one of my orphans?'),
            ('Kael "Wires" Nakamura', 1, 'Technomancer', 'Code is just magic that forgot its name. Looking to mod some gear?'),
            ('Dr. Thorne Vale', 1, 'Quest Giver', 'You think you’re restoring balance? You’re only reinforcing the illusion of control. Let go. Become part of the weave.');
        """
        cursor.executescript(npc_script)
        logging.info("Initial NPCs populated.")

        # --- Populate with initial item data ---
        # As per weapons.md, the Rusted Pipe Wrench is a default starting weapon.
        item_script = """
            INSERT OR IGNORE INTO items (name, item_type, slot, rarity, level_req, bonuses, damage, description)
            VALUES ('Rusted Pipe Wrench', 'Weapon', 'weapon', 'Common', 1, '{}', '{"min": 8, "max": 12, "type": "Bludgeoning"}', 'A heavy, dented pipe wrench, surprisingly effective as a bludgeoning tool in a pinch.');
        """
        cursor.executescript(item_script)
        logging.info("Initial items populated.")

        conn.commit()
        conn.close()
        logging.info(f"Database '{DB_NAME}' setup complete.")

    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")

if __name__ == "__main__":
    setup_database()