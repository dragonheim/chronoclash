import json

class Equipment:
    """Represents a single piece of equippable gear."""
    def __init__(self, item_id, name, item_type, slot, rarity, level_req, bonuses_json, damage_json, description):
        self.item_id = item_id
        self.name = name
        self.item_type = item_type
        self.slot = slot
        self.rarity = rarity
        self.level_req = level_req
        self.description = description

        # Bonuses are stored as a JSON string in the DB, parse them into a dict.
        try:
            self.bonuses = json.loads(bonuses_json) if bonuses_json else {}
        except json.JSONDecodeError:
            self.bonuses = {}
            print(f"Warning: Could not parse bonuses JSON for item '{self.name}': {bonuses_json}")

        # Damage is also a JSON string, parse it.
        try:
            self.damage = json.loads(damage_json) if damage_json else {}
        except json.JSONDecodeError:
            self.damage = {}
            print(f"Warning: Could not parse damage JSON for item '{self.name}': {damage_json}")

    def __str__(self):
        return f"{self.name} ({self.rarity} {self.item_type})"