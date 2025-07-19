import math

# --- Experience and Leveling ---

# The maximum level for the current game version.
# As per PRD, this is 20 for the initial release, but we design the
# chart for the eventual cap of 50.
MAX_LEVEL = 50

# The formula for the XP curve.
# A higher exponent makes leveling progressively harder. 1.5 is a good start.
XP_BASE = 100
XP_EXPONENT = 1.5

# A pre-calculated dictionary mapping each level to the XP required to reach the *next* level.
# XP_FOR_LEVEL[1] is the XP needed to go from level 1 to 2.
# We add a buffer at the end for the max level.
XP_FOR_LEVEL = {
    level: math.floor(XP_BASE * (level ** XP_EXPONENT))
    for level in range(1, MAX_LEVEL + 2)
}

# --- Combat Configuration ---

# Base XP awarded for defeating a monster. This will be multiplied by the monster's level.
MONSTER_BASE_XP = 25

# --- Spell Definitions ---
# A central dictionary defining all spells in the game.
# This allows for easy balancing and expansion.
# Cooldowns are in seconds.
SPELLS = {
    "rejuvenate": {
        "type": "heal",
        "mana_cost": 10,
        "cooldown": 15, # seconds
        "archetype_mods": {
            "Healer": 0.50,
            "Tank": 1/3,
            "DPS": 0.25,
        }
    },
    "chrono-blast": {
        "type": "damage",
        "mana_cost": 15,
        "cooldown": 5, # seconds
        "requires_combat": True,
        "archetype_mods": {
            "DPS": 0.50,
            "Tank": 1/3,
            "Healer": 0.25,
        }
    }
}