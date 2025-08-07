import math
from typing import Dict, List
import asyncio
from .constants import *
from .effects import Effect
from .equipment import Equipment
from game_data import XP_FOR_LEVEL, MAX_LEVEL


class Character:
    def __init__(self, name, time_period, archetype, char_class_name="DefaultClass"):
        self.name = name
        self.time_period = time_period
        self.archetype = archetype # "Tank", "DPS", "Healer"
        self.char_class_name = char_class_name # Specific class name like "Flameblade"

        self.character_level = 1
        self.class_level = 1 # For single class, this is same as character_level

        self.primary_attributes = {attr: 10 for attr in PRIMARY_ATTRIBUTES_LIST}
        self._apply_time_period_mods()

        self.equipment = {
            "weapon": None,
            "armor_body": None,
            "accessory1": None,
            "accessory2": None
        }

        self.secondary_attributes = {}
        self.tertiary_attributes = {}
        self.status_flags: Dict[str, int] = {} # e.g., {"Stunned": 3}
        self.spell_cooldowns: Dict[str, float] = {} # e.g., {"chrono-blast": 1678886400.123}
        self.active_effects = []
        self.is_in_combat = False
        self.combat_target = None
        self.experience = 0
        self.attribute_points = 0 # Points to spend on leveling up
        self.experience_to_next_level = XP_FOR_LEVEL.get(self.character_level, 999999)

        # Set current resource pools
        self.recalculate_all_stats()

    def _apply_time_period_mods(self):
        if self.time_period in TIME_PERIOD_ADJUSTMENTS:
            for attr, mod in TIME_PERIOD_ADJUSTMENTS[self.time_period].items():
                self.primary_attributes[attr] += mod

    def _calculate_secondary_attributes(self):
        base_secondary = {}
        for sec_attr, primaries in SECONDARY_ATTRIBUTES_DEF.items():
            pa_val = self.primary_attributes[primaries["a"]]
            pb_val = self.primary_attributes[primaries["b"]]
            pc_val = self.primary_attributes[primaries["c"]]
            base_secondary[sec_attr] = (pa_val / 2.0) + (pb_val / 4.0) + (pc_val / 4.0)

        # Apply flat bonuses from equipment to secondary attributes
        for item in self.equipment.values():
            if item:
                for stat, value in item.bonuses.items():
                    if stat in base_secondary:
                        base_secondary[stat] += value

        # Apply active spell effects (buffs/debuffs) to secondary attributes
        # These effects are applied to the base calculated values.
        current_secondary_with_effects = base_secondary.copy()
        for effect in self.active_effects:
            if effect.target_attribute in current_secondary_with_effects:
                if effect.modifier_type == "percentage":
                    # Apply percentage to the current value of the attribute
                    current_secondary_with_effects[effect.target_attribute] *= (1 + effect.value / 100.0)
                elif effect.modifier_type == "flat":
                    current_secondary_with_effects[effect.target_attribute] += effect.value
        
        # Ensure non-negative values after effects
        for attr in current_secondary_with_effects:
            current_secondary_with_effects[attr] = max(0, current_secondary_with_effects[attr])
        
        self.secondary_attributes = current_secondary_with_effects


    def _calculate_tertiary_attributes(self):
        calculated_tertiary = {}
        if self.archetype not in TERTIARY_ARCHETYPE_FORMULAS:
            print(f"Warning: Archetype {self.archetype} not found in TERTIARY_ARCHETYPE_FORMULAS. Using default empty tertiary stats.")
            self.tertiary_attributes = {}
            return

        formulas = TERTIARY_ARCHETYPE_FORMULAS[self.archetype]
        for tert_stat_name, (coeff, rel_sec_stat_name) in formulas.items():
            secondary_value = self.secondary_attributes.get(rel_sec_stat_name, 0)
            calculated_tertiary[tert_stat_name] = (coeff * self.class_level) + secondary_value

        # Apply flat bonuses from equipment to tertiary attributes
        for item in self.equipment.values():
            if item:
                for stat, value in item.bonuses.items():
                    if stat in calculated_tertiary:
                        calculated_tertiary[stat] += value
                    # Handle Armor specifically, as it's only from equipment
                    elif stat == "Armor":
                        calculated_tertiary[stat] = calculated_tertiary.get(stat, 0) + value
        
        # Armor is from equipment only (not implemented in this script version)
        calculated_tertiary["Armor"] = calculated_tertiary.get("Armor", 0) 

        # --- Resistances ---
        # Initialize all resistances to 0. Equipment can add to these.
        calculated_tertiary["resistances"] = {res_type: 0 for res_type in DAMAGE_TYPES}
        # TODO: Apply equipment bonuses to resistances here.

        self.tertiary_attributes = calculated_tertiary


    def recalculate_all_stats(self):
        """
        Recalculates all secondary and tertiary stats.
        This method preserves current HP/Mana, adjusting them relative to
        changes in max HP/Mana (e.g., from leveling up or equipment).
        """
        # Store old max values to see if they changed
        old_max_hp = self.tertiary_attributes.get("HP", 0)
        old_max_mana = self.tertiary_attributes.get("Mana", 0)

        self._calculate_secondary_attributes()  # Effects are applied inside here
        self._calculate_tertiary_attributes()

        new_max_hp = self.tertiary_attributes.get("HP", 0)
        new_max_mana = self.tertiary_attributes.get("Mana", 0)

        # --- Adjust Current HP ---
        # If current_hp doesn't exist yet (on first run), initialize it to max.
        if not hasattr(self, 'current_hp'):
             self.current_hp = new_max_hp
        # If max HP increased (e.g. level up, new gear), add the difference to current HP.
        elif new_max_hp > old_max_hp:
            self.current_hp += (new_max_hp - old_max_hp)
        # Ensure current HP doesn't exceed the new max (e.g. if an item was unequipped).
        self.current_hp = min(self.current_hp, new_max_hp)

        # --- Adjust Current Mana (similar logic) ---
        if not hasattr(self, 'current_mana'):
            self.current_mana = new_max_mana
        elif new_max_mana > old_max_mana:
            self.current_mana += (new_max_mana - old_max_mana)
        self.current_mana = min(self.current_mana, new_max_mana)

    def spend_attribute_points(self, allocations: Dict[str, int]):
        """
        Spends available attribute points based on a dictionary of allocations.
        Returns a tuple of (success: bool, message: str).
        """
        if not allocations:
            return False, "No allocations provided."

        total_to_spend = 0
        for attr, value in allocations.items():
            if attr not in self.primary_attributes:
                return False, f"Invalid attribute '{attr}'."
            if not isinstance(value, int) or value < 0:
                return False, f"Allocation for '{attr}' must be a non-negative integer."
            total_to_spend += value

        if total_to_spend <= 0:
            return False, "You must allocate at least one point."

        if total_to_spend > self.attribute_points:
            return False, f"You tried to spend {total_to_spend} points, but only have {self.attribute_points} available."

        # All checks passed, apply the points
        for attr, value in allocations.items():
            self.primary_attributes[attr] += value
        
        self.attribute_points -= total_to_spend
        self.recalculate_all_stats()
        return True, f"Successfully spent {total_to_spend} points. You have {self.attribute_points} remaining."

    def gain_experience(self, amount):
        """
        Adds experience to the character and checks for level-ups.
        Returns a list of messages generated during the process (e.g., level up notifications).
        """
        if self.character_level >= MAX_LEVEL:
            return [] # At max level, no more XP gain

        self.experience += amount
        leveled_up = False
        messages = []

        # Use a while loop in case of multiple level-ups from one XP gain
        while self.experience >= self.experience_to_next_level and self.character_level < MAX_LEVEL:
            leveled_up = True
            messages.append(self._level_up())

        if leveled_up:
            # The final message includes the current XP status
            messages.append(f"You are now Level {self.character_level}. (XP: {self.experience}/{self.experience_to_next_level})")
        
        return messages

    def _level_up(self):
        """Internal method to handle the logic for a character leveling up."""
        self.experience -= self.experience_to_next_level
        self.character_level += 1
        self.class_level += 1 # For now, class level is tied to character level
        self.attribute_points += LEVEL_UP_ATTRIBUTE_POINTS
        self.experience_to_next_level = XP_FOR_LEVEL.get(self.character_level, 999999)
        self.recalculate_all_stats()
        return f"** DING! You have reached Level {self.character_level}! You gain {LEVEL_UP_ATTRIBUTE_POINTS} attribute points! **"

    def equip_item(self, item: Equipment):
        """Equips an item to the appropriate slot and recalculates stats."""
        if item.slot not in self.equipment:
            print(f"Error: Invalid equipment slot '{item.slot}'.")
            return
        if self.equipment[item.slot]:
            print(f"Unequipping {self.equipment[item.slot].name} from {item.slot}.")
        self.equipment[item.slot] = item
        print(f"Equipped {item.name} to {item.slot}.")
        self.recalculate_all_stats()

    def unequip_item(self, slot):
        """Unequips an item from a slot and recalculates stats."""
        if slot not in self.equipment:
            print(f"Error: Invalid equipment slot '{slot}'.")
            return
        if not self.equipment[slot]:
            print(f"No item equipped in {slot}.")
            return
        
        item_name = self.equipment[slot].name
        self.equipment[slot] = None
        print(f"Unequipped {item_name} from {slot}.")
        self.recalculate_all_stats()

    def apply_effect(self, effect: Effect):
        # Remove existing effects with the same name to prevent simple stacking (implement stacking rules if needed)
        self.active_effects = [e for e in self.active_effects if e.name != effect.name]
        # Add a new instance of the effect to ensure its duration is reset
        new_effect_instance = Effect(
            effect.name, effect.target_attribute, effect.modifier_type, effect.value, effect.duration_ticks,
            dot_damage=effect.dot_damage, dot_type=effect.dot_type
        )
        self.active_effects.append(new_effect_instance)
        # This print is for server-side logging/debugging
        print(f"Applied effect '{effect.name}' to {self.name} for {effect.duration_ticks} ticks.")
        self.recalculate_all_stats()

    def apply_status_flag(self, flag_name: str, duration_ticks: int):
        """Applies a status flag for a certain duration."""
        self.status_flags[flag_name] = duration_ticks
        # This print is for server-side logging/debugging
        print(f"Applied status '{flag_name}' to {self.name} for {duration_ticks} ticks.")

    def has_flag(self, flag_name: str) -> bool:
        """Checks if a character currently has a given status flag."""
        return self.status_flags.get(flag_name, 0) > 0

    def tick_down_effects(self) -> List[str]:
        """
        Ticks down all timed effects and status flags.
        Returns a list of messages for effects that have expired or ticked.
        """
        messages = []
        recalc_needed = False

        # Tick down stat-modifying effects
        new_active_effects = []
        for effect in self.active_effects:
            # --- Process DoT damage for this tick ---
            if effect.dot_damage > 0:
                damage = effect.dot_damage
                self.current_hp -= damage
                dot_message = f"You take {damage} {effect.dot_type or 'damage'} damage from '{effect.name}'."
                messages.append(dot_message)

            effect.remaining_ticks -= 1
            if effect.remaining_ticks > 0:
                new_active_effects.append(effect)
            else:
                messages.append(f"The effect '{effect.name}' has worn off.")
                recalc_needed = True
        self.active_effects = new_active_effects

        # Tick down status flags
        new_status_flags = {}
        for flag, duration in self.status_flags.items():
            duration -= 1
            if duration > 0:
                new_status_flags[flag] = duration
            else:
                # A more generic message for flags wearing off
                messages.append(f"You are no longer {flag}.")
        self.status_flags = new_status_flags

        # If any stat-modifying effect expired, we need to recalculate stats.
        if recalc_needed:
            self.recalculate_all_stats()

        return messages

    def can_cast(self, spell_name: str, spell_data: Dict) -> (bool, str):
        """
        Checks if the character can cast a given spell based on mana and cooldown.
        Returns a tuple of (can_cast: bool, reason: str).
        """
        # Check mana
        mana_cost = spell_data.get("mana_cost", 0)
        if self.current_mana < mana_cost:
            return False, f"Not enough mana. Requires {mana_cost}, you have {self.current_mana:.0f}."

        # Check cooldown
        cooldown_end_time = self.spell_cooldowns.get(spell_name)
        if cooldown_end_time and asyncio.get_event_loop().time() < cooldown_end_time:
            remaining = cooldown_end_time - asyncio.get_event_loop().time()
            return False, f"Spell '{spell_name}' is on cooldown for {remaining:.1f} more seconds."

        return True, ""

    def put_on_cooldown(self, spell_name: str, spell_data: Dict):
        """Puts a spell on cooldown by recording its end time."""
        cooldown_duration = spell_data.get("cooldown", 0)
        if cooldown_duration > 0:
            self.spell_cooldowns[spell_name] = asyncio.get_event_loop().time() + cooldown_duration

    def heal(self, amount: float) -> float:
        """
        Heals the character for a given amount, capped at max HP.
        Returns the actual amount healed.
        """
        max_hp = self.tertiary_attributes.get("HP", 0)
        if self.current_hp >= max_hp:
            return 0.0

        missing_hp = max_hp - self.current_hp
        amount_to_heal = min(amount, missing_hp)
        self.current_hp += amount_to_heal
        return amount_to_heal

    def display_stats(self, title="Character Stats"):
        print(f"\n--- {title}: {self.name} (Lvl {self.character_level} {self.time_period} {self.archetype} {self.char_class_name}) ---")
        print(f"  HP: {self.current_hp:.0f} / {self.tertiary_attributes.get('HP', 0):.0f} | Mana: {self.current_mana:.0f} / {self.tertiary_attributes.get('Mana', 0):.0f}")
        print(f"  XP: {self.experience} / {self.experience_to_next_level} | Points to Spend: {self.attribute_points}")
        print("-" * 60)
        print("Primary Attributes:")
        for attr, val in self.primary_attributes.items():
            print(f"  {attr:<15}: {val}")
        print("Secondary Attributes (Calculated, with effects):")
        for attr, val in self.secondary_attributes.items():
            print(f"  {attr:<15}: {val:.2f}")
        print("Tertiary Attributes (Calculated):")
        for attr, val in self.tertiary_attributes.items():
            print(f"  {attr:<15}: {val:.2f}")
        print("Equipment:")
        # Resistances are nested, display them separately for clarity
        if "resistances" in self.tertiary_attributes:
            print("Resistances:")
            for res_type, val in self.tertiary_attributes["resistances"].items():
                print(f"  {res_type:<15}: {val}")
        for slot, item in self.equipment.items():
            print(f"  {slot.capitalize()}: {item.name if item else 'None'}")
        if self.active_effects:
            print("Active Effects:")
            for effect in self.active_effects:
                print(f"  {effect}")
        else:
            print("Active Effects: None")


class Monster(Character):
    """
    Represents a monster in the game. Inherits from Character to reuse
    attribute calculation logic but has its own HP scaling and initialization.
    """
    def __init__(self, name, level, archetype, char_class_name, primary_attributes_override, category="Common"):
        # Set category before calling super, as the parent's __init__ will trigger
        # the overridden recalculate_all_stats, which depends on the category.
        self.category = category
        # Call the parent constructor. We use "Present" as the time period
        # because it has no inherent modifiers, making it a neutral base for monsters.
        super().__init__(name=name, time_period="Present", archetype=archetype, char_class_name=char_class_name)

        # --- Override Player-Specific Defaults ---
        self.character_level = level
        self.class_level = level
        self.primary_attributes = primary_attributes_override.copy()

        # Monsters do not have player-specific progression attributes.
        # It's good practice to remove them from the instance.
        if hasattr(self, 'experience'):
            del self.experience
        if hasattr(self, 'attribute_points'):
            del self.attribute_points
        if hasattr(self, 'experience_to_next_level'):
            del self.experience_to_next_level

        # Recalculate stats with the correct monster level and attributes.
        self.recalculate_all_stats()

    def recalculate_all_stats(self):
        """
        Recalculates all monster stats. Overrides Character method to ensure
        the category HP modifier is applied correctly.
        """
        # First, run the standard calculations from the parent.
        self._calculate_secondary_attributes()
        self._calculate_tertiary_attributes()

        # Now, apply the monster-specific HP modifier based on its category.
        modifiers = {
            "Common": 1.0, "Uncommon": 2.5, "Rare": 5.0,
            "Elite": 10.0, "Legendary": 20.0
        }
        modifier = modifiers.get(self.category, 1.0)

        # The base HP was just calculated by _calculate_tertiary_attributes.
        # We apply the modifier to it.
        if "HP" in self.tertiary_attributes:
            self.tertiary_attributes["HP"] *= modifier

        # Finally, set current HP/Mana to the new maximums.
        self.current_hp = self.tertiary_attributes.get("HP", 0)
        self.current_mana = self.tertiary_attributes.get("Mana", 0)

    def display_stats(self, title="Monster Stats"):
        """A simplified stat display for monsters."""
        hp = self.tertiary_attributes.get('HP', 0)
        print(f"\n--- {title}: {self.name} (Lvl {self.character_level} {self.category} {self.char_class_name}) ---")
        print(f"  HP: {self.current_hp:.2f} / {hp:.2f}")
        print(f"  AP: {self.tertiary_attributes.get('AP', 0):.2f}")
        print(f"  Armor: {self.tertiary_attributes.get('Armor', 0):.2f}")
        print("--- End Stats ---")