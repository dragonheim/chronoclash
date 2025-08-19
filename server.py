import asyncio
import logging
import sys
import io
import sqlite3
import random
import math
import json
from contextlib import redirect_stdout
from chronoclash_core.mechanics.entities import Character, Monster
from chronoclash_core.mechanics.equipment import Equipment
from chronoclash_core.game_data import XP_FOR_LEVEL, MONSTER_BASE_XP, SPELLS
# --- Configuration ---
HOST = '0.0.0.0' # Listen on all available network interfaces
PORT = 8888
LOG_LEVEL = logging.INFO
STATUS_HOST = '0.0.0.0' # Listen on all available network interfaces
STATUS_PORT = 8889

# --- Game Balance Constants ---
AP_DAMAGE_CONVERSION = 0.25 # 4 AP = +1 damage
ARMOR_EFFECTIVENESS = 200 # A higher value makes armor less effective.

# --- Setup Logging ---
logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Load Config ---
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
        DB_NAME = config['DB_NAME']
except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
    logging.critical(f"FATAL: Could not load DB_NAME from config.json: {e}. Exiting.")
    exit(1)

class CleanDisconnect(Exception):
    """Custom exception to signal a clean client disconnect."""
    pass


def get_db_connection():
    """Creates a connection to the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


class GameServer:
    """
    The main GameServer class responsible for handling client connections
    and orchestrating game logic.
    """
    def __init__(self, host, port, status_host, status_port):
        self.host = host
        self.port = port
        self.status_host = status_host
        self.status_port = status_port
        # {addr: {'writer': writer, 'character': character_obj, ...}}
        self.clients = {}
        self.shutdown_event = asyncio.Event()
        self.combat_loop_task = None
        self.zones = {}
        self._load_zones()
        self._load_npcs()
        self._spawn_initial_monsters()
        # A mapping of command strings to their handler methods
        self.command_handlers = {}
        self._register_commands()

    def _load_zones(self):
        """Loads all zones from the database into the server's state."""
        logging.info("Loading zones from database...")
        conn = get_db_connection()
        try:
            zones_data = conn.execute("SELECT id, name, description, required_level FROM zones").fetchall()
            for zone_row in zones_data:
                zone_name = zone_row['name']
                self.zones[zone_name] = {
                    "id": zone_row['id'],
                    "description": zone_row['description'],
                    "required_level": zone_row['required_level'],
                    "npcs": [],
                    "monsters": [],
                    "broadcast_queue": asyncio.Queue()
                }
            logging.info(f"Loaded {len(self.zones)} zones: {list(self.zones.keys())}")
        except sqlite3.Error as e:
            logging.error(f"Database error while loading zones: {e}", exc_info=True)
        finally:
            conn.close()

    def _spawn_initial_monsters(self):
        """Loads monster spawn data from the database and populates the world."""
        logging.info("Spawning initial monsters from database...")
        conn = get_db_connection()
        try:
            # Query for all spawn points, joining with the monster templates
            query = """
                SELECT
                    mt.name, mt.archetype, mt.char_class_name,
                    mt.agility, mt.constitution, mt.strength,
                    mt.intelligence, mt.spirit, mt.wisdom,
                    z.name AS zone_name, ms.level, ms.category, ms.quantity
                FROM monster_spawns ms
                JOIN monster_templates mt ON ms.monster_template_id = mt.id
                JOIN zones z ON ms.zone_id = z.id
            """
            spawns = conn.execute(query).fetchall()

            total_spawned = 0
            for spawn_data in spawns:
                zone_name = spawn_data['zone_name']
                if zone_name not in self.zones:
                    logging.warning(f"Zone '{zone_name}' defined in monster_spawns not found in server config. Skipping.")
                    continue

                primary_attributes = {
                    "Agility": spawn_data['agility'], "Constitution": spawn_data['constitution'],
                    "Strength": spawn_data['strength'], "Intelligence": spawn_data['intelligence'],
                    "Spirit": spawn_data['spirit'], "Wisdom": spawn_data['wisdom'],
                }

                for i in range(spawn_data['quantity']):
                    monster = Monster(
                        name=f"{spawn_data['name']} #{i+1}", level=spawn_data['level'],
                        archetype=spawn_data['archetype'], char_class_name=spawn_data['char_class_name'],
                        primary_attributes_override=primary_attributes, category=spawn_data['category']
                    )
                    self.zones[zone_name]["monsters"].append(monster)
                    total_spawned += 1
                logging.info(f"Spawned {spawn_data['quantity']}x {spawn_data['name']} in {zone_name}.")
            if total_spawned == 0:
                logging.warning("No monsters were spawned. Check monster_spawns table in the database.")
        except sqlite3.Error as e:
            logging.error(f"Database error while spawning monsters: {e}", exc_info=True)
        finally:
            conn.close()

    def _load_npcs(self):
        """Loads NPC data from the database and places them in their zones."""
        logging.info("Loading NPCs from database...")
        conn = get_db_connection()
        try:
            query = """
                SELECT n.id, n.name, z.name AS zone_name, n.role, n.dialogue
                FROM npcs n
                JOIN zones z ON n.zone_id = z.id
            """
            npcs = conn.execute(query).fetchall()
            for npc_data in npcs:
                zone_name = npc_data['zone_name']
                if zone_name not in self.zones:
                    # This case should ideally not happen with foreign key constraints
                    logging.warning(f"NPC '{npc_data['name']}' references zone '{zone_name}' which was not loaded. Skipping.")
                    continue
                self.zones[zone_name]["npcs"].append(dict(npc_data))
                logging.info(f"Loaded NPC '{npc_data['name']}' into {zone_name}.")

        except sqlite3.Error as e:
            logging.error(f"Database error while loading NPCs: {e}", exc_info=True)
        finally:
            conn.close()

    def _register_commands(self):
        """Registers all available server commands."""
        self.command_handlers = {
            "/stats": self.handle_stats,
            "/quit": self.handle_quit,
            "/shutdown": self.handle_shutdown,
            "/who": self.handle_who,
            "/users": self.handle_who, # Alias for /who
            "/look": self.handle_look,
            "/attack": self.handle_attack,
            "/talk": self.handle_talk,
            "/zone": self.handle_zone,
            "/spend": self.handle_spend,
            "/cast": self.handle_cast,
            "/move": self.handle_zone, # Alias
        }
        logging.info(f"Registered commands: {list(self.command_handlers.keys())}")

    async def handle_stats(self, session, args):
        """Handles the /stats command. Sends character stats to the client."""
        writer = session['writer']
        player_character = session['character']
        string_buffer = io.StringIO()
        with redirect_stdout(string_buffer):
            player_character.display_stats()
        response = string_buffer.getvalue() + "\n"
        writer.write(response.encode())
        await writer.drain()
        return

    async def handle_look(self, session, args):
        """Handles the /look command. Shows players and monsters in the current zone."""
        writer = session['writer']
        player_character = session['character']
        current_zone_name = session.get('zone', 'Unknown')

        if current_zone_name not in self.zones:
            writer.write(b"You are in an unknown void.\n")
            await writer.drain()
            return

        zone_data = self.zones[current_zone_name]
        response_lines = [f"--- You are in {current_zone_name} ---"]

        # List players
        response_lines.append("Players here:")
        players_in_zone = [
            s['character'] for s in self.clients.values()
            if s.get('zone') == current_zone_name and s['character'] != player_character
        ]
        if players_in_zone:
            for char in players_in_zone:
                response_lines.append(f"  [Lvl {char.character_level}] {char.name}")
        else:
            response_lines.append("  You are alone.")

        response_lines.append("") # Add a blank line for spacing

        # List NPCs
        response_lines.append("People here:")
        npcs_in_zone = zone_data.get("npcs", [])
        if npcs_in_zone:
            for npc in npcs_in_zone:
                response_lines.append(f"  {npc['name']} <{npc['role']}>")

        response_lines.append("") # Add a blank line for spacing

        # List monsters
        response_lines.append("You see:")
        monsters_in_zone = zone_data.get("monsters", [])
        if monsters_in_zone:
            for monster in monsters_in_zone:
                response_lines.append(f"  [Lvl {monster.character_level} {monster.category}] {monster.name} ({monster.current_hp:.0f}/{monster.tertiary_attributes.get('HP', 0):.0f} HP)")
        
        response = "\n".join(response_lines) + "\n"
        writer.write(response.encode())
        await writer.drain()

    async def handle_attack(self, session, args):
        """Initiates combat with a target monster."""
        writer = session['writer']
        player_character = session['character']

        if player_character.is_in_combat:
            writer.write(b"You are already in combat.\n")
            await writer.drain()
            return

        if not args:
            writer.write(b"Usage: /attack <target name>\n")
            await writer.drain()
            return

        target_name = " ".join(args)
        current_zone_name = session.get('zone', 'Unknown')
        zone_data = self.zones.get(current_zone_name)

        if not zone_data:
            writer.write(b"You are in an unknown void and cannot attack.\n")
            await writer.drain()
            return

        target_monster = None
        for monster in zone_data['monsters']:
            if monster.name.lower() == target_name.lower():
                target_monster = monster
                break

        if not target_monster:
            writer.write(f"You don't see a '{target_name}' here.\n".encode())
            await writer.drain()
            return
        
        if target_monster.is_in_combat:
            writer.write(f"The {target_monster.name} is already in combat with someone else.\n".encode())
            await writer.drain()
            return

        # Initiate combat
        player_character.is_in_combat = True
        player_character.combat_target = target_monster
        target_monster.is_in_combat = True
        target_monster.combat_target = player_character

        logging.info(f"{player_character.name} has initiated combat with {target_monster.name}.")
        response = f"You attack the {target_monster.name}!\n"
        writer.write(response.encode())
        await writer.drain()

    async def handle_talk(self, session, args):
        """Handles talking to an NPC."""
        writer = session['writer']
        current_zone_name = session.get('zone', 'Unknown')

        if not args:
            writer.write(b"Usage: /talk <npc name>\n")
            await writer.drain()
            return

        target_name = " ".join(args)
        zone_data = self.zones.get(current_zone_name)

        if not zone_data:
            writer.write(b"You are in an unknown void and cannot talk to anyone.\n")
            await writer.drain()
            return

        target_npc = None
        for npc in zone_data.get('npcs', []):
            if npc['name'].lower() == target_name.lower():
                target_npc = npc
                break

        if not target_npc:
            writer.write(f"You don't see anyone named '{target_name}' here.\n".encode())
            await writer.drain()
            return

        dialogue = target_npc.get('dialogue', "...")
        response = f"[{target_npc['name']}]: {dialogue}\n"
        writer.write(response.encode())
        await writer.drain()

    async def handle_zone(self, session, args):
        """Handles moving a character to a different zone."""
        writer = session['writer']
        player_character = session['character']
        current_zone_name = session.get('zone')

        if player_character.has_flag("Rooted"):
            writer.write(b"You are Rooted and cannot move!\n")
            await writer.drain()
            return

        if not args:
            available_zones = [
                name for name, data in self.zones.items()
                if player_character.character_level >= data['required_level'] and name != current_zone_name
            ]
            response = "Usage: /zone <destination>\n"
            if available_zones:
                response += f"Available zones for you: {', '.join(available_zones)}\n"
            else:
                response += "There are no other zones available to you at this time.\n"
            writer.write(response.encode())
            await writer.drain()
            return

        target_zone_input = " ".join(args)

        # Find the actual zone name (case-insensitive)
        actual_zone_name = None
        for z_name in self.zones.keys():
            if z_name.lower() == target_zone_input.lower():
                actual_zone_name = z_name
                break

        if not actual_zone_name:
            writer.write(f"Zone '{target_zone_input}' does not exist.\n".encode())
            await writer.drain()
            return

        if actual_zone_name == current_zone_name:
            writer.write(f"You are already in {current_zone_name}.\n".encode())
            await writer.drain()
            return

        if player_character.is_in_combat:
            writer.write(b"You cannot change zones while in combat!\n")
            await writer.drain()
            return

        zone_data = self.zones[actual_zone_name]
        if player_character.character_level < zone_data['required_level']:
            writer.write(f"You must be level {zone_data['required_level']} to enter {actual_zone_name}.\n".encode())
            await writer.drain()
            return

        logging.info(f"Player {player_character.name} is moving from {current_zone_name} to {actual_zone_name}.")
        await self.broadcast_to_zone(current_zone_name, f"INFO: {player_character.name} has left the area.", exclude_session=session)
        session['zone'] = actual_zone_name
        await self.broadcast_to_zone(actual_zone_name, f"INFO: {player_character.name} has arrived.", exclude_session=session)
        writer.write(f"You travel to {actual_zone_name}.\n".encode())
        await writer.drain()
        await self.handle_look(session, []) # Automatically look around the new zone

    async def handle_spend(self, session, args):
        """Handles spending attribute points. Usage: /spend <attr> <points> ..."""
        writer = session['writer']
        player_character = session['character']

        if not args or len(args) % 2 != 0:
            response = "Usage: /spend <attribute> <points> [attribute2] [points2] ...\n"
            response += "Example: /spend Strength 2 Agility 1\n"
            response += f"You have {player_character.attribute_points} points available to spend.\n"
            writer.write(response.encode())
            await writer.drain()
            return

        allocations = {}
        try:
            for i in range(0, len(args), 2):
                # Capitalize to match the expected format in mechanics
                attr_name = args[i].capitalize()
                points = int(args[i+1])
                allocations[attr_name] = allocations.get(attr_name, 0) + points
        except (ValueError, IndexError):
            writer.write(b"Invalid format. Please provide attribute names and integer point values.\n")
            await writer.drain()
            return

        success, message = player_character.spend_attribute_points(allocations)

        writer.write(f"{message}\n".encode())
        await writer.drain()

        if success:
            await self.update_character_progress(player_character)
            await self.handle_stats(session, []) # Show updated stats

    async def handle_cast(self, session, args):
        """Handles casting a spell. Usage: /cast <spell name>"""
        writer = session['writer']
        player_character = session['character']

        if not args:
            writer.write(b"Usage: /cast <spell name>\n")
            await writer.drain()
            return

        spell_name = " ".join(args).lower()
        spell_data = SPELLS.get(spell_name)

        if not spell_data:
            writer.write(f"You don't know a spell named '{' '.join(args)}'.\n".encode())
            await writer.drain()
            return

        # --- Pre-cast checks ---
        if spell_data.get("requires_combat", False) and (not player_character.is_in_combat or not player_character.combat_target):
            writer.write(b"You must be in combat to cast that spell.\n")
            await writer.drain()
            return

        can_cast, reason = player_character.can_cast(spell_name, spell_data)
        if not can_cast:
            writer.write(f"{reason}\n".encode())
            await writer.drain()
            return

        # --- Deduct cost and put on cooldown ---
        player_character.current_mana -= spell_data.get("mana_cost", 0)
        player_character.put_on_cooldown(spell_name, spell_data)

        # --- Execute Spell Effect ---
        spell_type = spell_data.get("type")
        archetype = player_character.archetype
        max_hp = player_character.tertiary_attributes.get("HP", 0)

        if spell_type == "heal":
            heal_modifier = spell_data["archetype_mods"].get(archetype, 0.0)
            heal_amount = max_hp * heal_modifier
            amount_healed = player_character.heal(heal_amount)

            if amount_healed > 0:
                response = f"You cast {spell_name.title()}, healing yourself for {amount_healed:.0f} HP.\n"
                response += f"You are now at {player_character.current_hp:.0f}/{max_hp:.0f} HP.\n"
            else:
                response = "You are already at full health.\n"
            writer.write(response.encode())
            await writer.drain()

        elif spell_type == "damage":
            target = player_character.combat_target
            # This check is slightly redundant due to the pre-cast check, but it's safe.
            if not target:
                writer.write(b"You don't have a target.\n")
                await writer.drain()
                return

            damage_modifier = spell_data["archetype_mods"].get(archetype, 0.0)
            damage = round(max_hp * damage_modifier)
            target.current_hp -= damage

            response = f"You unleash a {spell_name.title()} at {target.name}, dealing {damage} damage!\n"
            writer.write(response.encode())
            await writer.drain()

            if target.current_hp <= 0:
                await self.handle_defeat(player_character, target)
            else:
                target_max_hp = target.tertiary_attributes.get('HP', 0)
                response = f"The {target.name} has {target.current_hp:.0f}/{target_max_hp:.0f} HP remaining.\n"
                writer.write(response.encode())
                await writer.drain()
        else:
            writer.write(f"Spell '{spell_name}' has an unknown effect type.\n".encode())
            await writer.drain()

    async def handle_quit(self, session, args):
        """Handles the /quit command. Signals for a clean disconnect."""
        writer = session['writer']
        player_character = session['character']

        # If in combat, the monster gets a final, fatal blow.
        if player_character.is_in_combat and player_character.combat_target:
            monster = player_character.combat_target
            logging.warning(f"Player {player_character.name} quit during combat with {monster.name}. Monster wins.")
            monster.is_in_combat = False
            monster.combat_target = None
            player_character.current_hp = 0
            writer.write(f"As you turn to flee, the {monster.name} strikes a fatal blow!\n".encode())
            await writer.drain()

        goodbye_message = "Disconnecting. Goodbye!\n"
        writer.write(goodbye_message.encode())
        await writer.drain()
        raise CleanDisconnect()

    async def handle_shutdown(self, session, args):
        """Handles the /shutdown command. Stops the server gracefully."""
        writer = session['writer']
        # --- Placeholder for Admin Check ---
        # In the future, you would add a check here like:
        # if not session['character'].is_admin:
        #     writer.write(b"You do not have permission to use this command.\n")
        #     return
        logging.warning(f"Shutdown command issued by {session['character'].name}.")
        writer.write(b"Acknowledged. Initiating server shutdown...\n")
        await writer.drain()
        await self.broadcast(f"SERVER: The server is being shut down by an administrator. Goodbye!")
        self.shutdown_event.set()
        return

    async def handle_who(self, session, args):
        """Handles the /who command. Lists players online."""
        writer = session['writer']
        current_zone = session.get('zone', 'Unknown')

        # Determine the scope of the search
        search_scope = ""
        if not args:
            search_scope = current_zone.lower()
        else:
            search_scope = args[0].lower()

        response_lines = []
        # Handle 'all' case
        if search_scope == 'all':
            players_by_zone = {}
            for s in self.clients.values():
                if s.get('character'):
                    char = s['character']
                    zone = s.get('zone', 'Unknown')
                    if zone not in players_by_zone:
                        players_by_zone[zone] = []
                    players_by_zone[zone].append(f"  [Lvl {char.character_level} {char.char_class_name}] {char.name}")

            if not players_by_zone:
                response_lines.append("No players are currently online.")
            else:
                response_lines.append("Players Online:")
                total_players = 0
                for zone, players in sorted(players_by_zone.items()):
                    total_players += len(players)
                    response_lines.append(f"--- {zone.capitalize()} ({len(players)}) ---")
                    response_lines.extend(players)
                response_lines.append(f"Total players online: {total_players}")
        else:
            # Handle specific zone case (including current zone)
            matching_players = []
            for s in self.clients.values():
                if s.get('character') and s.get('zone', 'Unknown').lower() == search_scope:
                    char = s['character']
                    matching_players.append(f"  [Lvl {char.character_level} {char.char_class_name}] {char.name}")

            if not matching_players:
                response_lines.append(f"No players found in zone '{search_scope.capitalize()}'.")
            else:
                response_lines.append(f"Players in {search_scope.capitalize()} ({len(matching_players)}):")
                response_lines.extend(matching_players)
        
        response = "\n".join(response_lines) + "\n"
        writer.write(response.encode())
        await writer.drain()
        return

    async def handle_status_request(self, reader, writer):
        """
        Handles a request to the status server, returning a JSON of online players.
        This provides a minimal HTTP response for easy consumption.
        """
        addr = writer.get_extra_info('peername')
        logging.info(f"Status request from {addr}")

        player_list = []
        for session in self.clients.values():
            if session.get('character'):
                player_list.append({
                    'name': session['character'].name,
                    'zone': session.get('zone', 'Unknown'),
                    'level': session['character'].character_level,
                    'class': session['character'].char_class_name
                })

        try:
            json_payload = json.dumps(player_list, indent=2)
            response_body = json_payload.encode('utf-8')

            # Create a simple HTTP 200 OK response
            headers = "\r\n".join([
                "HTTP/1.1 200 OK",
                f"Content-Length: {len(response_body)}",
                "Content-Type: application/json; charset=utf-8",
                "Connection: close",
                "\r\n"
            ])
            writer.write(headers.encode('utf-8'))
            writer.write(response_body)
            await writer.drain()
        finally:
            writer.close()
            await writer.wait_closed()

    async def handle_client(self, reader, writer):
        """Coroutine to handle a single client connection."""
        addr = writer.get_extra_info('peername')
        logging.info(f"New connection from {addr}")
        player_character = None
        session = None

        try:
            # --- Character Login ---
            writer.write(b"Welcome to Chrono Clash!\nPlease enter your character name to log in: ")
            await writer.drain()

            data = await reader.read(1024)
            if not data:
                raise CleanDisconnect("Client disconnected before login.")

            char_name_to_load = data.decode().strip()
            if not char_name_to_load:
                writer.write(b"Invalid name entered. Disconnecting.\n")
                await writer.drain()
                raise CleanDisconnect("Invalid name entered.")

            # --- Database Lookup ---
            conn = get_db_connection()
            char_data = conn.execute('SELECT * FROM characters WHERE name = ?', (char_name_to_load,)).fetchone()
            conn.close()

            # Check if character is already logged in
            for client_session in self.clients.values():
                if client_session['character'].name.lower() == char_name_to_load.lower():
                    writer.write(b"This character is already logged in.\n")
                    await writer.drain()
                    raise CleanDisconnect("Character already logged in.")

            if not char_data:
                logging.warning(f"Login failed for {addr}: Character '{char_name_to_load}' not found.")
                writer.write(f"Character '{char_name_to_load}' not found. Disconnecting.\n".encode())
                await writer.drain()
                raise CleanDisconnect("Character not found.")

            # --- Character Object Creation ---
            logging.info(f"Loading character '{char_data['name']}' for {addr}.")
            player_character = Character(
                name=char_data['name'],
                time_period=char_data['time_period'],
                archetype=char_data['archetype'],
                char_class_name=char_data['char_class_name']
            )
            # Manually set the level from DB and recalculate stats
            player_character.character_level = char_data['level']
            player_character.class_level = char_data['level']
            player_character.experience = char_data['experience']
            player_character.attribute_points = char_data['attribute_points']
            # Set the XP needed for the next level based on the loaded level
            player_character.experience_to_next_level = XP_FOR_LEVEL.get(player_character.character_level, 999999)
            player_character.recalculate_all_stats()

            # --- Load saved HP/Mana ---
            # If current_hp is -1 (default), it's a new character, so they start at full health (which recalculate_all_stats already did).
            # Otherwise, load the saved values, ensuring they don't exceed the max.
            if char_data['current_hp'] != -1:
                player_character.current_hp = min(char_data['current_hp'], player_character.tertiary_attributes.get('HP', 0))
            if char_data['current_mana'] != -1:
                player_character.current_mana = min(char_data['current_mana'], player_character.tertiary_attributes.get('Mana', 0))

            # Load and equip items
            await self._load_character_equipment(player_character)

            # Create and store the client's session
            session = {
                "writer": writer,
                "character": player_character,
                "zone": "Seattle" # Default zone for now
            }
            self.clients[addr] = session
            logging.info(f"Successfully loaded Level {player_character.character_level} character '{player_character.name}' for {addr}")

            # --- Send a more detailed welcome message ---
            welcome_message = (
                f"Welcome back, {player_character.name}!\n"
                f"You are a Level {player_character.character_level} {player_character.time_period} {player_character.archetype}.\n"
                f"Your HP: {player_character.tertiary_attributes.get('HP', 0):.2f}\n"
                f"Type '/stats' to see your full character sheet.\n"
            )
            writer.write(welcome_message.encode())
            await writer.drain()

            # --- Main Game Loop ---
            while True:
                # Wait for data from the client
                data = await reader.read(1024)
                if not data:
                    # An empty read indicates the client has disconnected
                    break

                message = data.decode().strip()                
                if not message:
                    continue

                logging.info(f"Received from {addr} ({player_character.name}): {message}")

                if message.startswith('/'):
                    await self.process_command(session, message)
                elif message.startswith('@'):
                    await self.process_whisper(session, message)
                else:
                    # For now, treat non-commands as unknown. Later this could be zone chat.
                    response = f"Unknown input. Commands start with '/' (e.g., /stats). Whispers with '@'.\n"
                    writer.write(response.encode())
                    await writer.drain()

        except CleanDisconnect:
            logging.info(f"Client {addr} ({player_character.name if player_character else 'N/A'}) disconnected gracefully.")
        except asyncio.CancelledError:
            logging.info(f"Client handler for {addr} was cancelled.")
        except ConnectionResetError:
            logging.warning(f"Connection reset by {addr}.")
        except Exception as e:
            logging.error(f"An error occurred with client {addr}: {e}")
        finally:
            # --- Cleanup on Disconnect ---
            char_name = "Unknown"
            if addr in self.clients:
                session = self.clients.get(addr)
                if session and session.get("character"):
                    player_character = session["character"]
                    char_name = player_character.name
                    
                    # Handle disconnect during combat
                    if player_character.is_in_combat and player_character.combat_target:
                        monster = player_character.combat_target
                        logging.warning(f"Player {char_name} disconnected during combat with {monster.name}. Monster wins.")
                        # Monster is no longer in combat
                        monster.is_in_combat = False
                        monster.combat_target = None
                        # Player is considered defeated
                        player_character.current_hp = 0
                    char_name = session["character"].name
                del self.clients[addr]

            logging.info(f"Closing connection for {addr} ({char_name})")

            # --- Save character progress on disconnect ---
            if player_character:
                try:
                    await self.update_character_progress(player_character)
                    logging.info(f"Saved progress for {player_character.name} on disconnect.")
                except Exception as e:
                    logging.error(f"Failed to save progress for {player_character.name} on disconnect: {e}")

            writer.close()
            await writer.wait_closed()

    async def process_command(self, session, message):
        """Parses and executes a slash-command."""
        writer = session['writer']
        parts = message.split()
        command = parts[0].lower()
        args = parts[1:]

        handler = self.command_handlers.get(command)
        if handler:
            await handler(session, args)
        else:
            response = f"Unknown command: '{command}'.\n"
            writer.write(response.encode())
            await writer.drain()

    async def process_whisper(self, sender_session, message):
        """Processes a whisper message and sends it to the target player."""
        sender_writer = sender_session['writer']
        sender_char = sender_session['character']

        parts = message.split(maxsplit=1)
        if len(parts) < 2 or not parts[1]:
            response = "Usage: @<player_name> <message>\n"
            sender_writer.write(response.encode())
            await sender_writer.drain()
            return

        target_name = parts[0][1:].lower()  # Remove '@' and lowercase for search
        whisper_message = parts[1]

        # Find the target client session by character name
        target_session = None
        for client_session in self.clients.values():
            if client_session['character'].name.lower() == target_name:
                target_session = client_session
                break

        if target_session:
            target_writer = target_session['writer']
            formatted_message = f"[{sender_char.name} whispers]: {whisper_message}\n"
            target_writer.write(formatted_message.encode())
            await target_writer.drain()

            # Confirmation to sender
            confirmation_message = f"[To {target_session['character'].name}]: {whisper_message}\n"
            sender_writer.write(confirmation_message.encode())
            await sender_writer.drain()
        else:
            response = f"Player '{parts[0][1:]}' not found.\n"
            sender_writer.write(response.encode())
            await sender_writer.drain()

    async def broadcast(self, message):
        """Sends a message to all connected clients."""
        logging.info(f"Broadcasting: {message}")
        full_message = message + "\n"
        # Create a list of writers to iterate over, avoiding issues if self.clients changes
        all_writers = [session['writer'] for session in self.clients.values()]
        for writer in all_writers:
            try:
                writer.write(full_message.encode())
                await writer.drain()
            except ConnectionError:
                # This client disconnected during the broadcast, which is fine.
                pass

    async def broadcast_to_zone(self, zone_name, message, exclude_session=None):
        """Sends a message to all clients in a specific zone."""
        logging.info(f"Broadcasting to zone '{zone_name}': {message}")
        full_message = f"{message}\n"
        for session in self.clients.values():
            if session.get('zone') == zone_name:
                # Don't send the message to the excluded session (e.g., the player who triggered it)
                if exclude_session and session is exclude_session:
                    continue
                try:
                    session['writer'].write(full_message.encode())
                    await session['writer'].drain()
                except ConnectionError:
                    pass

    def get_session_by_character(self, character):
        """Finds a client session associated with a given character object."""
        for session in self.clients.values():
            if session['character'] is character:
                return session
        return None

    async def handle_defeat(self, victor, defeated):
        """Handles the logic when one entity defeats another."""
        logging.info(f"{victor.name} has defeated {defeated.name}.")

        # End combat for both
        victor.is_in_combat = False
        victor.combat_target = None
        defeated.is_in_combat = False
        defeated.combat_target = None

        # Handle player victory
        victor_session = self.get_session_by_character(victor)
        if victor_session:
            msg = f"You have defeated the {defeated.name}!\n"
            victor_session['writer'].write(msg.encode())
            await victor_session['writer'].drain()

            # If a player defeated a monster, award experience
            if isinstance(victor, Character) and isinstance(defeated, Monster):
                # Use the formula from game_data.py
                xp_reward = math.ceil(MONSTER_BASE_XP * defeated.character_level)
                
                victor_session['writer'].write(f"You gain {xp_reward} experience.\n".encode())
                await victor_session['writer'].drain()

                level_up_messages = victor.gain_experience(xp_reward)
                for message in level_up_messages:
                    victor_session['writer'].write(f"\n{message}\n".encode())
                    await victor_session['writer'].drain()
                
                await self.update_character_progress(victor)

        # Handle player defeat
        defeated_session = self.get_session_by_character(defeated)
        if defeated_session:
            msg = f"You have been defeated by the {victor.name}!\n"
            defeated_session['writer'].write(msg.encode())
            await defeated_session['writer'].drain()
            # Future: Handle respawn logic. For now, they are just out of combat.

        # If a monster was defeated, remove it from the world
        if isinstance(defeated, Monster):
            for zone in self.zones.values():
                if defeated in zone['monsters']:
                    zone['monsters'].remove(defeated)
                    logging.info(f"Removed defeated monster {defeated.name} from the world.")
                    break

    async def combat_tick_loop(self):
        """The main game loop for processing combat ticks."""
        while not self.shutdown_event.is_set():
            try:
                await asyncio.sleep(3) # 3-second tick as per PRD

                # Gather all combatants to avoid issues with dicts/lists changing size during iteration
                all_combatants = []
                for session in self.clients.values():
                    if session['character'].is_in_combat:
                        all_combatants.append(session['character'])
                
                for zone in self.zones.values():
                    for monster in zone['monsters']:
                        if monster.is_in_combat:
                            all_combatants.append(monster)

                # Process combat for each combatant
                for attacker in all_combatants:
                    # --- Tick down effects and statuses at the start of the turn ---
                    # This happens for everyone in combat, even if they are stunned.
                    expiration_messages = attacker.tick_down_effects()
                    if expiration_messages:
                        attacker_session = self.get_session_by_character(attacker)
                        if attacker_session:
                            for msg in expiration_messages:
                                attacker_session['writer'].write(f"INFO: {msg}\n".encode())
                            await attacker_session['writer'].drain()

                    # Ensure the attacker is still in combat and has a valid target
                    if not attacker.is_in_combat or not attacker.combat_target:
                        continue

                    # --- Check for action-preventing statuses ---
                    if attacker.has_flag("Stunned"):
                        attacker_session = self.get_session_by_character(attacker)
                        if attacker_session:
                            msg = "You are Stunned and cannot act!\n"
                            attacker_session['writer'].write(msg.encode())
                            await attacker_session['writer'].drain()
                        # The lack of an attack message is enough to inform the target.
                        continue # Skip the rest of the turn

                    defender = attacker.combat_target
                    
                    # Check if defender is still a valid target
                    if defender.current_hp <= 0:
                        # Target is already defeated, end combat for attacker
                        attacker.is_in_combat = False
                        attacker.combat_target = None
                        continue

                    # --- Damage Calculation ---
                    # Start with a base unarmed damage range
                    base_damage = random.randint(1, 3)
                    
                    # If the attacker has a weapon, use its damage range instead
                    weapon = attacker.equipment.get('weapon')
                    if weapon and weapon.damage:
                        min_dmg = weapon.damage.get('min', 1)
                        max_dmg = weapon.damage.get('max', 2)
                        base_damage = random.randint(min_dmg, max_dmg)

                    # --- New Damage Formula from GDD ---
                    # 1. Add bonus damage from Attack Power (AP)
                    ap_bonus_damage = attacker.tertiary_attributes.get('AP', 0) * AP_DAMAGE_CONVERSION
                    
                    # 2. Calculate pre-mitigation damage
                    gross_damage = base_damage + ap_bonus_damage

                    # 3. Apply Armor mitigation
                    armor = defender.tertiary_attributes.get('Armor', 0)
                    armor_mitigation = 1 - (armor / (armor + ARMOR_EFFECTIVENESS))
                    
                    mitigated_damage = gross_damage * armor_mitigation

                    # 4. TODO: Apply Damage Type Resistance mitigation
                    # This is where you would get the weapon's damage type and check
                    # the defender's resistance to it, further modifying the damage.

                    damage = max(1, round(mitigated_damage)) # Always do at least 1 damage

                    defender.current_hp -= damage

                    # --- Send messages ---
                    attacker_session = self.get_session_by_character(attacker)
                    if attacker_session:
                        msg = f"You hit the {defender.name} for {damage} damage. ({defender.current_hp:.0f}/{defender.tertiary_attributes.get('HP', 0):.0f} HP)\n"
                        attacker_session['writer'].write(msg.encode())
                        await attacker_session['writer'].drain()

                    defender_session = self.get_session_by_character(defender)
                    if defender_session:
                        msg = f"The {attacker.name} hits you for {damage} damage! ({defender.current_hp:.0f}/{defender.tertiary_attributes.get('HP', 0):.0f} HP)\n"
                        defender_session['writer'].write(msg.encode())
                        await defender_session['writer'].drain()

                    # --- Check for defeat ---
                    if defender.current_hp <= 0:
                        await self.handle_defeat(attacker, defender)

            except asyncio.CancelledError:
                logging.info("Combat loop is shutting down.")
                break
            except Exception as e:
                logging.error(f"Error in combat loop: {e}", exc_info=True)

    async def _load_character_equipment(self, character: Character):
        """Queries the DB for a character's equipped items and applies them."""
        logging.info(f"Loading equipment for {character.name}...")
        conn = None
        try:
            conn = get_db_connection()
            query = """
                SELECT i.id, i.name, i.item_type, i.slot, i.rarity, i.level_req, i.bonuses, i.damage, i.description
                FROM character_inventory ci
                JOIN items i ON ci.item_id = i.id
                WHERE ci.character_id = (SELECT id FROM characters WHERE name = ?) AND ci.is_equipped = 1
            """
            equipped_items_data = conn.execute(query, (character.name,)).fetchall()

            for item_data in equipped_items_data:
                equipment_piece = Equipment(
                    item_data['id'],
                    name=item_data['name'],
                    item_type=item_data['item_type'],
                    slot=item_data['slot'],
                    rarity=item_data['rarity'],
                    level_req=item_data['level_req'],
                    bonuses_json=item_data['bonuses'],
                    damage_json=item_data['damage'],
                    description=item_data['description']
                )
                character.equip_item(equipment_piece)
        finally:
            if conn:
                conn.close()

    async def update_character_progress(self, character):
        """Saves a character's current level and experience to the database."""
        conn = None
        try:
            conn = get_db_connection()
            conn.execute(
                "UPDATE characters SET level = ?, experience = ?, attribute_points = ?, current_hp = ?, current_mana = ? WHERE name = ?",
                (character.character_level, character.experience, character.attribute_points, character.current_hp, character.current_mana, character.name)
            )
            conn.commit()
            logging.info(f"Updated progress for {character.name} in DB: Level {character.character_level}, XP {character.experience}, "
                         f"Points {character.attribute_points}, HP {character.current_hp:.0f}, Mana {character.current_mana:.0f}")
        finally:
            if conn:
                conn.close()

    async def start(self):
        """Starts the game server and the status server, and waits for shutdown."""
        game_server = None
        status_server = None
        try:
            game_server = await asyncio.start_server(
                self.handle_client, self.host, self.port)
            status_server = await asyncio.start_server(
                self.handle_status_request, self.status_host, self.status_port)

            game_addr = game_server.sockets[0].getsockname()
            status_addr = status_server.sockets[0].getsockname()
            logging.info(f"Game server started. Listening on {game_addr}")
            logging.info(f"Status server started. Listening on {status_addr}")

            self.combat_loop_task = asyncio.create_task(self.combat_tick_loop())

            await self.shutdown_event.wait()
        except Exception as e:
            logging.error(f"Error starting servers: {e}")
        finally:
            logging.info("Shutting down servers...")
            if game_server:
                game_server.close()
                await game_server.wait_closed()
            if status_server:
                status_server.close()
                await status_server.wait_closed()
            if self.combat_loop_task:
                self.combat_loop_task.cancel()
            logging.info("Servers have shut down.")

async def main():
    server = GameServer(HOST, PORT, STATUS_HOST, STATUS_PORT)
    await server.start()

if __name__ == "__main__":
    logging.info("Starting server.")
    asyncio.run(main())
