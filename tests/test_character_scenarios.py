import pytest
from chronoclash_core.mechanics.entities import Character
from chronoclash_core.mechanics.equipment import Equipment
from chronoclash_core.game_data import XP_FOR_LEVEL, SPELLS

@pytest.fixture
def new_character():
    """Provides a fresh character for each test."""
    return Character(
        name="Tester",
        time_period="Present",
        archetype="DPS",
        char_class_name="Grenadier"
    )

def test_character_creation_and_initial_stats(new_character):
    """Tests that a character is created with the correct initial values."""
    assert new_character.name == "Tester"
    assert new_character.character_level == 1
    assert new_character.experience == 0
    assert new_character.experience_to_next_level == XP_FOR_LEVEL[1]
    assert new_character.attribute_points == 10 # From PRD for new characters

    # Check if time period modifier was applied (Present: +2 Int, +1 Agi)
    assert new_character.primary_attributes["Intelligence"] == 7 # Base 5 + 2
    assert new_character.primary_attributes["Agility"] == 6 # Base 5 + 1
    assert new_character.primary_attributes["Strength"] == 5 # Base 5

    # Check a secondary attribute calculation (e.g., AP = Strength + Agility)
    assert new_character.secondary_attributes["AP"] == 11 # 5 Str + 6 Agi

    # Check a tertiary attribute (HP is based on Constitution and class mods)
    # Grenadier (DPS) has a 1.0 HP mod. HP = (Constitution * 10) * 1.0
    assert new_character.tertiary_attributes["HP"] == 50 # 5 Con * 10

def test_level_up(new_character):
    """Tests the experience gain and leveling up process."""
    xp_to_level_2 = XP_FOR_LEVEL[1]
    
    # Gain enough XP to level up
    level_up_messages = new_character.gain_experience(xp_to_level_2)
    
    assert new_character.character_level == 2
    assert new_character.experience == 0 # XP should reset after level up
    assert new_character.experience_to_next_level == XP_FOR_LEVEL[2]
    assert new_character.attribute_points == 10 + 5 # 10 initial + 5 for level 2
    assert "You have reached Level 2!" in level_up_messages[0]

def test_spend_attribute_points(new_character):
    """Tests spending attribute points and the resulting stat recalculation."""
    initial_strength = new_character.primary_attributes["Strength"]
    initial_ap = new_character.secondary_attributes["AP"]
    
    # Spend 3 points on Strength
    success, message = new_character.spend_attribute_points({"Strength": 3})
    
    assert success is True
    assert new_character.attribute_points == 7 # 10 - 3
    assert new_character.primary_attributes["Strength"] == initial_strength + 3
    # AP should be recalculated (AP = Strength + Agility)
    assert new_character.secondary_attributes["AP"] == initial_ap + 3

def test_spend_too_many_points(new_character):
    """Tests that a character cannot spend more points than they have."""
    success, message = new_character.spend_attribute_points({"Strength": 11})
    assert success is False
    assert "not enough attribute points" in message.lower()
    assert new_character.attribute_points == 10 # Unchanged

def test_equip_item_updates_stats(new_character):
    """Tests that equipping an item correctly modifies character stats."""
    initial_hp = new_character.tertiary_attributes["HP"]
    
    # Create a sample piece of equipment
    power_vest = Equipment(
        id=99, name="Power Vest", item_type="Armor", slot="chest",
        bonuses_json='{"Constitution": 5}'
    )
    
    new_character.equip_item(power_vest)
    
    # HP = (Constitution * 10) * class_mod.
    # Initial Con = 5. New Con = 10.
    # HP should increase by (5 * 10) = 50
    assert new_character.tertiary_attributes["HP"] == initial_hp + 50
    assert new_character.equipment["chest"] == power_vest