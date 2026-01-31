PRIMARY_ATTRIBUTES_LIST = ["Agility", "Constitution", "Strength", "Intelligence", "Spirit", "Wisdom"]

SECONDARY_ATTRIBUTES_DEF = {
    "Might": {"a": "Strength", "b": "Wisdom", "c": "Agility"},
    "Endurance": {"a": "Constitution", "b": "Spirit", "c": "Strength"},
    "Speed": {"a": "Agility", "b": "Intelligence", "c": "Constitution"},
    "Energy": {"a": "Intelligence", "b": "Constitution", "c": "Spirit"},
    "Willpower": {"a": "Wisdom", "b": "Strength", "c": "Spirit"},
    "Dexterity": {"a": "Spirit", "b": "Agility", "c": "Intelligence"},
}

TIME_PERIOD_ADJUSTMENTS = {
    "Past": {"Strength": 2, "Spirit": 1, "Wisdom": -1, "Intelligence": -2},
    "Future": {"Intelligence": 2, "Agility": 1, "Spirit": -1, "Constitution": -2},
    "Present": {}
}

# Tertiary Attribute Formulas directly calculate the final value
# Format: { "TertiaryStatName": (Coefficient, "RelevantSecondaryStatName") }
# Formula: (Coefficient * class_level) + RelevantSecondaryStatValue
TERTIARY_ARCHETYPE_FORMULAS = {
    "Tank": {
        "HP": (10, "Endurance"),  # GDD: (10 * class level) + endurance
        "Mana": (4, "Energy"),  # GDD: (4 * class level) + energy
        "Dodge": (4, "Dexterity"), # GDD: (4 * class level) + dexterity
        "AP": (4, "Might"),  # GDD: (4 * class level) + might
        "Accuracy": (6, "Speed"),  # GDD: (6 * class level) + speed
    },
    "DPS": {
        "HP": (4, "Endurance"),  # GDD: (4 * class level) + endurance
        "Mana": (10, "Energy"),  # GDD: (10 * class level) + energy
        "Dodge": (3, "Dexterity"), # GDD: (3 * class level) + dexterity
        "AP": (7, "Willpower"),  # GDD: (7 * class level) + willpower
        "Accuracy": (6, "Speed"),  # GDD: (6 * class level) + speed
    },
    "Healer": {
        "HP": (7, "Endurance"),  # GDD: (7 * class level) + endurance
        "Mana": (7, "Energy"),  # GDD: (7 * class level) + energy
        "Dodge": (3, "Dexterity"), # GDD: (3 * class level) + dexterity
        "AP": (4, "Willpower"),  # GDD: (4 * class level) + willpower
        "Accuracy": (4, "Speed"),  # GDD: (4 * class level) + speed
    }
    # Note: Armor is from equipment only, so not calculated here.
}

INITIAL_ATTRIBUTE_POINTS = 10
MAX_INITIAL_ALLOCATION_PER_ATTRIBUTE = 3
LEVEL_UP_ATTRIBUTE_POINTS = 3
MAX_LEVEL_UP_ALLOCATION_PER_ATTRIBUTE = 1
MAX_LEVEL = 20

DAMAGE_TYPES = ["Physical", "Fire", "Ice", "Lightning", "Arcane", "Poison"]