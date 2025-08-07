import pytest
from chronoclash_core.mechanics.entities import Character
from chronoclash_core.mechanics.equipment import Equipment
from chronoclash_core.game_data import XP_FOR_LEVEL

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
    assert new_character.experience_to_next_level == XP_FOR_LEVEL.get(1)
    assert new_character.attribute_points == 0 # Starts at 0, gained on level up

    # "Present" time period has no modifiers, so all primary attributes should be the base of 10.
    assert new_character.primary_attributes["Intelligence"] == 10
    assert new_character.primary_attributes["Agility"] == 10
    assert new_character.primary_attributes["Strength"] == 10

    # Check a secondary attribute calculation (e.g., Willpower)
    # Willpower = (Wisdom/2) + (Strength/4) + (Spirit/4)
    # Willpower = (10/2) + (10/4) + (10/4) = 5 + 2.5 + 2.5 = 10
    assert new_character.secondary_attributes["Willpower"] == 10.0

    # Check a tertiary attribute (AP for DPS)
    # AP = (7 * class_level) + willpower
    # AP = (7 * 1) + 10 = 17
    assert new_character.tertiary_attributes["AP"] == 17.0

    # Check that resistances were initialized
    assert "resistances" in new_character.tertiary_attributes
    assert "Slashing" in new_character.tertiary_attributes["resistances"]
    assert new_character.tertiary_attributes["resistances"]["Slashing"] == 0

def test_level_up(new_character):
    """Tests the experience gain and leveling up process."""
    xp_to_level_2 = XP_FOR_LEVEL.get(1)
    
    # Gain enough XP to level up
    level_up_messages = new_character.gain_experience(xp_to_level_2)
    
    assert new_character.character_level == 2
    assert new_character.experience == 0 # XP should reset after level up
    assert new_character.experience_to_next_level == XP_FOR_LEVEL.get(2)
    assert new_character.attribute_points == 5 # From LEVEL_UP_ATTRIBUTE_POINTS
    assert "** DING! You have reached Level 2!" in level_up_messages[0]

def test_spend_attribute_points(new_character):
    """Tests spending attribute points and the resulting stat recalculation."""
    new_character.attribute_points = 5 # Manually give points for testing
    initial_strength = new_character.primary_attributes["Strength"]
    initial_ap = new_character.tertiary_attributes["AP"]
    
    # Spend 3 points on Strength
    success, message = new_character.spend_attribute_points({"Strength": 3})
    
    assert success is True
    assert new_character.attribute_points == 2 # 5 - 3
    assert new_character.primary_attributes["Strength"] == initial_strength + 3
    # AP depends on Willpower, which depends on Strength.
    # Willpower increases by (3 / 4.0) = 0.75. AP should increase by the same.
    assert new_character.tertiary_attributes["AP"] == pytest.approx(initial_ap + 0.75)

def test_spend_too_many_points(new_character):
    """Tests that a character cannot spend more points than they have."""
    new_character.attribute_points = 5
    success, message = new_character.spend_attribute_points({"Strength": 6})
    assert success is False
    assert "only have 5 available" in message.lower()
    assert new_character.attribute_points == 5 # Unchanged

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