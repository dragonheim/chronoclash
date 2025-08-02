import pytest
from chronoclash_core.mechanics import (
    Character,
    Effect,
    Equipment,
    INITIAL_ATTRIBUTE_POINTS,
    MAX_INITIAL_ALLOCATION_PER_ATTRIBUTE,
    LEVEL_UP_ATTRIBUTE_POINTS,
    MAX_LEVEL_UP_ALLOCATION_PER_ATTRIBUTE,
    MAX_LEVEL,
    PRIMARY_ATTRIBUTES_LIST
)

# --- Fixtures ---

@pytest.fixture
def past_tank_char():
    """Returns a default Tank character from the Past era for testing."""
    return Character(name="Valerius", time_period="Past", archetype="Tank", char_class_name="Flameblade")

@pytest.fixture
def future_dps_char():
    """Returns a default DPS character from the Future era for testing."""
    return Character(name="Lyra", time_period="Future", archetype="DPS", char_class_name="Pulse Mage")

@pytest.fixture
def present_healer_char():
    """Returns a default Healer character from the Present era for testing."""
    return Character(name="Carlan", time_period="Present", archetype="Healer", char_class_name="Field Medic")


# --- Test Classes ---

class TestCharacterCreation:
    """Tests related to character initialization and setup."""

    def test_initialization(self, past_tank_char):
        """Test basic character attributes upon creation."""
        assert past_tank_char.name == "Valerius"
        assert past_tank_char.character_level == 1
        assert past_tank_char.class_level == 1
        assert past_tank_char.time_period == "Past"
        assert past_tank_char.archetype == "Tank"
        assert past_tank_char.char_class_name == "Flameblade"
        assert len(past_tank_char.active_effects) == 0

    def test_time_period_mods(self):
        """Test that time period modifiers are applied correctly to base attributes."""
        # Past: +2 Str, +1 Spi, -1 Wis, -2 Int
        past_char = Character("Past Test", "Past", "Tank")
        assert past_char.primary_attributes["Strength"] == 12
        assert past_char.primary_attributes["Spirit"] == 11
        assert past_char.primary_attributes["Wisdom"] == 9
        assert past_char.primary_attributes["Intelligence"] == 8
        assert past_char.primary_attributes["Agility"] == 10 # Unchanged
        assert past_char.primary_attributes["Constitution"] == 10 # Unchanged

        # Future: +2 Int, +1 Agi, -1 Spi, -2 Con
        future_char = Character("Future Test", "Future", "DPS")
        assert future_char.primary_attributes["Intelligence"] == 12
        assert future_char.primary_attributes["Agility"] == 11
        assert future_char.primary_attributes["Spirit"] == 9
        assert future_char.primary_attributes["Constitution"] == 8
        assert future_char.primary_attributes["Strength"] == 10 # Unchanged
        assert future_char.primary_attributes["Wisdom"] == 10 # Unchanged

        # Present: No changes
        present_char = Character("Present Test", "Present", "Healer")
        for attr in PRIMARY_ATTRIBUTES_LIST:
            assert present_char.primary_attributes[attr] == 10

    def test_initial_point_allocation_valid(self, past_tank_char):
        """Test a valid allocation of initial attribute points."""
        initial_str = past_tank_char.primary_attributes["Strength"]
        initial_con = past_tank_char.primary_attributes["Constitution"]
        
        allocations = {"Strength": 3, "Constitution": 3, "Spirit": 2, "Wisdom": 2} # 10 points
        result = past_tank_char.allocate_primary_points(INITIAL_ATTRIBUTE_POINTS, MAX_INITIAL_ALLOCATION_PER_ATTRIBUTE, allocations)
        
        assert result is True
        assert past_tank_char.primary_attributes["Strength"] == initial_str + 3
        assert past_tank_char.primary_attributes["Constitution"] == initial_con + 3

    def test_initial_point_allocation_too_many_total_points(self, past_tank_char):
        """Test allocating more than the total allowed initial points."""
        original_attrs = past_tank_char.primary_attributes.copy()
        allocations = {"Strength": 3, "Constitution": 3, "Spirit": 3, "Wisdom": 2} # 11 points
        result = past_tank_char.allocate_primary_points(INITIAL_ATTRIBUTE_POINTS, MAX_INITIAL_ALLOCATION_PER_ATTRIBUTE, allocations)
        
        assert result is False
        assert past_tank_char.primary_attributes == original_attrs

    def test_initial_point_allocation_too_many_per_attribute(self, past_tank_char):
        """Test allocating more than the max allowed points to a single attribute."""
        original_attrs = past_tank_char.primary_attributes.copy()
        allocations = {"Strength": 4, "Constitution": 3, "Spirit": 3} # 10 points, but Str > 3
        result = past_tank_char.allocate_primary_points(INITIAL_ATTRIBUTE_POINTS, MAX_INITIAL_ALLOCATION_PER_ATTRIBUTE, allocations)
        
        assert result is False
        assert past_tank_char.primary_attributes == original_attrs

    def test_initial_point_allocation_invalid_attribute(self, past_tank_char):
        """Test allocating points to a non-existent attribute."""
        original_attrs = past_tank_char.primary_attributes.copy()
        allocations = {"Strength": 3, "Magic": 3}
        result = past_tank_char.allocate_primary_points(INITIAL_ATTRIBUTE_POINTS, MAX_INITIAL_ALLOCATION_PER_ATTRIBUTE, allocations)
        
        assert result is False
        assert past_tank_char.primary_attributes == original_attrs

class TestCharacterLeveling:
    """Tests related to character leveling and advancement."""

    def test_level_up_valid(self, future_dps_char):
        """Test a valid level up with point allocation."""
        future_dps_char.level_up({"Intelligence": 1, "Wisdom": 1, "Agility": 1})
        assert future_dps_char.character_level == 2
        assert future_dps_char.class_level == 2
        # Base 12 Int + 1 = 13
        assert future_dps_char.primary_attributes["Intelligence"] == 13

    def test_level_up_invalid_allocation(self, future_dps_char):
        """Test a level up with an invalid point allocation, which should fail and revert."""
        original_attrs = future_dps_char.primary_attributes.copy()
        original_level = future_dps_char.character_level
        
        # Too many points for one attribute
        result = future_dps_char.level_up({"Intelligence": 2, "Wisdom": 1})
        
        assert result is False
        assert future_dps_char.character_level == original_level
        assert future_dps_char.primary_attributes == original_attrs

    def test_level_up_to_max(self, present_healer_char):
        """Test leveling a character all the way to the max level."""
        for i in range(1, MAX_LEVEL):
            present_healer_char.level_up({"Spirit": 1, "Wisdom": 1, "Constitution": 1})
        
        assert present_healer_char.character_level == MAX_LEVEL
        
        # Try to level up again
        result = present_healer_char.level_up({"Spirit": 1, "Wisdom": 1, "Constitution": 1})
        assert result is False
        assert present_healer_char.character_level == MAX_LEVEL

class TestAttributeCalculations:
    """Tests to verify secondary and tertiary attribute calculations."""

    def test_secondary_attributes(self, past_tank_char):
        """Test the formula for secondary attributes."""
        # Past Tank: Str 12, Con 10, Agi 10, Int 8, Spi 11, Wis 9
        # Might = (Str/2) + (Wis/4) + (Agi/4) = (12/2) + (9/4) + (10/4) = 6 + 2.25 + 2.5 = 10.75
        assert past_tank_char.secondary_attributes["Might"] == pytest.approx(10.75)
        
        # Endurance = (Con/2) + (Spi/4) + (Str/4) = (10/2) + (11/4) + (12/4) = 5 + 2.75 + 3 = 10.75
        assert past_tank_char.secondary_attributes["Endurance"] == pytest.approx(10.75)

    def test_tertiary_attributes_tank(self, past_tank_char):
        """Test tertiary attributes for a Tank archetype."""
        # At level 1, for a Tank:
        # Endurance = 10.75
        # HP = (10 * class_level) + Endurance = (10 * 1) + 10.75 = 20.75
        assert past_tank_char.tertiary_attributes["HP"] == pytest.approx(20.75)
        
        # Might = 10.75
        # AP = (4 * class_level) + Might = (4 * 1) + 10.75 = 14.75
        assert past_tank_char.tertiary_attributes["AP"] == pytest.approx(14.75)

    def test_tertiary_attributes_dps(self, future_dps_char):
        """Test tertiary attributes for a DPS archetype."""
        # Future DPS: Str 10, Con 8, Agi 11, Int 12, Spi 9, Wis 10
        # Energy = (Int/2) + (Con/4) + (Spi/4) = (12/2) + (8/4) + (9/4) = 6 + 2 + 2.25 = 10.25
        # Willpower = (Wis/2) + (Str/4) + (Spi/4) = (10/2) + (10/4) + (9/4) = 5 + 2.5 + 2.25 = 9.75
        
        # At level 1, for a DPS:
        # Mana = (10 * class_level) + Energy = (10 * 1) + 10.25 = 20.25
        assert future_dps_char.tertiary_attributes["Mana"] == pytest.approx(20.25)
        # AP = (7 * class_level) + Willpower = (7 * 1) + 9.75 = 16.75
        assert future_dps_char.tertiary_attributes["AP"] == pytest.approx(16.75)

    def test_recalculate_on_primary_change(self, present_healer_char):
        """Test that stats are recalculated when primary attributes change."""
        initial_hp = present_healer_char.tertiary_attributes["HP"]
        present_healer_char.allocate_primary_points(1, 1, {"Constitution": 1})
        new_hp = present_healer_char.tertiary_attributes["HP"]
        assert new_hp > initial_hp

class TestEffects:
    """Tests for applying and ticking status effects (buffs/debuffs)."""

    def test_apply_flat_buff(self, present_healer_char):
        """Test applying a flat bonus buff."""
        initial_might = present_healer_char.secondary_attributes["Might"]
        buff = Effect("Might Surge", "Might", "flat", 5, 3)
        present_healer_char.apply_effect(buff)
        
        assert len(present_healer_char.active_effects) == 1
        assert present_healer_char.secondary_attributes["Might"] == initial_might + 5

    def test_apply_percentage_debuff(self, present_healer_char):
        """Test applying a percentage penalty debuff."""
        initial_speed = present_healer_char.secondary_attributes["Speed"]
        debuff = Effect("Slow", "Speed", "percentage", -20, 2) # -20%
        present_healer_char.apply_effect(debuff)
        
        assert present_healer_char.secondary_attributes["Speed"] == pytest.approx(initial_speed * 0.8)

    def test_effect_tick_down_and_expire(self, present_healer_char):
        """Test that effects tick down and are removed when duration is 0."""
        initial_might = present_healer_char.secondary_attributes["Might"]
        buff = Effect("Might Surge", "Might", "flat", 5, 2)
        present_healer_char.apply_effect(buff)
        
        assert len(present_healer_char.active_effects) == 1
        assert present_healer_char.secondary_attributes["Might"] == initial_might + 5
        
        present_healer_char.tick_effects() # 1 tick remaining
        assert len(present_healer_char.active_effects) == 1
        assert present_healer_char.active_effects[0].remaining_ticks == 1
        assert present_healer_char.secondary_attributes["Might"] == initial_might + 5 # Still active
        
        present_healer_char.tick_effects() # 0 ticks remaining, should expire
        assert len(present_healer_char.active_effects) == 0
        assert present_healer_char.secondary_attributes["Might"] == initial_might # Back to normal

    def test_multiple_effects(self, past_tank_char):
        """Test applying multiple effects and see if they are calculated correctly."""
        initial_might = past_tank_char.secondary_attributes["Might"]
        initial_speed = past_tank_char.secondary_attributes["Speed"]
        
        might_buff = Effect("Might Surge", "Might", "flat", 10, 3)
        speed_debuff = Effect("Slow", "Speed", "percentage", -50, 2)
        
        past_tank_char.apply_effect(might_buff)
        past_tank_char.apply_effect(speed_debuff)
        
        assert len(past_tank_char.active_effects) == 2
        assert past_tank_char.secondary_attributes["Might"] == initial_might + 10
        assert past_tank_char.secondary_attributes["Speed"] == pytest.approx(initial_speed * 0.5)

        past_tank_char.tick_effects() # Tick 1
        past_tank_char.tick_effects() # Tick 2, speed debuff expires
        
        assert len(past_tank_char.active_effects) == 1
        assert past_tank_char.active_effects[0].name == "Might Surge"
        assert past_tank_char.secondary_attributes["Might"] == initial_might + 10
        assert past_tank_char.secondary_attributes["Speed"] == pytest.approx(initial_speed) # Speed is back to normal

        past_tank_char.tick_effects() # Tick 3, might buff expires
        assert len(past_tank_char.active_effects) == 0
        assert past_tank_char.secondary_attributes["Might"] == initial_might

class TestEquipment:
    """Tests for equipping items and their effects on stats."""

    def test_equip_item_and_get_bonus(self, past_tank_char):
        """Test equipping an item and verifying stat bonuses."""
        initial_hp = past_tank_char.tertiary_attributes["HP"]
        initial_armor = past_tank_char.tertiary_attributes.get("Armor", 0)

        plate_armor = Equipment(
            name="Vrathan Plate",
            slot="armor_body",
            bonuses={"Armor": 25, "HP": 50, "Endurance": 5}
        )
        past_tank_char.equip_item(plate_armor)

        new_hp = past_tank_char.tertiary_attributes["HP"]
        new_armor = past_tank_char.tertiary_attributes.get("Armor", 0)

        assert past_tank_char.equipment["armor_body"] is plate_armor
        assert new_armor == initial_armor + 25
        # HP bonus is applied via flat HP and by increasing Endurance.
        # The test verifies the final value is greater, confirming the system works.
        assert new_hp > initial_hp

    def test_unequip_item_and_lose_bonus(self, past_tank_char):
        """Test that unequipping an item correctly removes its stat bonuses."""
        plate_armor = Equipment(name="Vrathan Plate", slot="armor_body", bonuses={"Armor": 25, "HP": 50})
        past_tank_char.equip_item(plate_armor)

        stats_with_equip = past_tank_char.tertiary_attributes.copy()
        past_tank_char.unequip_item("armor_body")
        stats_after_unequip = past_tank_char.tertiary_attributes.copy()

        assert past_tank_char.equipment["armor_body"] is None
        assert stats_after_unequip.get("Armor", 0) < stats_with_equip.get("Armor", 0)
        assert stats_after_unequip["HP"] < stats_with_equip["HP"]