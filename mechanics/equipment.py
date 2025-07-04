class Equipment:
    def __init__(self, name, slot, bonuses=None):
        self.name = name
        self.slot = slot # e.g., "weapon", "armor_body", "accessory1"
        # Bonuses can apply to secondary or tertiary attributes.
        # Example: {"Armor": 10, "HP": 50, "Might": 5, "AP": 3}
        self.bonuses = bonuses if bonuses else {}

    def __str__(self):
        return f"{self.name} ({self.slot}) - Bonuses: {self.bonuses}"