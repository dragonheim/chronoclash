from mechanics import Character, Effect, INITIAL_ATTRIBUTE_POINTS, MAX_INITIAL_ALLOCATION_PER_ATTRIBUTE

if __name__ == "__main__":
    print("========= Chrono Clash Character System Tests =========\n")

    # --- 1. Character Creation ---
    print("--- Test: Character Creation & Initial Point Allocation ---")
    # Valerius (Tank - Flameblade, Past Era)
    valerius = Character(name="Valerius", time_period="Past", archetype="Tank", char_class_name="Flameblade")
    valerius_initial_alloc = {"Strength": 3, "Constitution": 3, "Spirit": 2, "Wisdom": 2} # 10 points
    print(f"\nAllocating initial points for {valerius.name}...")
    valerius.allocate_primary_points(INITIAL_ATTRIBUTE_POINTS, MAX_INITIAL_ALLOCATION_PER_ATTRIBUTE, valerius_initial_alloc)
    valerius.display_stats(title="Valerius - After Creation & Initial Allocation")

    # Lyra (DPS - Pulse Mage, Future Era)
    lyra = Character(name="Lyra", time_period="Future", archetype="DPS", char_class_name="Pulse Mage")
    lyra_initial_alloc = {"Intelligence": 3, "Wisdom": 3, "Spirit": 2, "Agility": 2} # 10 points
    print(f"\nAllocating initial points for {lyra.name}...")
    lyra.allocate_primary_points(INITIAL_ATTRIBUTE_POINTS, MAX_INITIAL_ALLOCATION_PER_ATTRIBUTE, lyra_initial_alloc)
    lyra.display_stats(title="Lyra - After Creation & Initial Allocation")

    # Carlan (Healer - Field Medic, Present Era)
    carlan = Character(name="Carlan", time_period="Present", archetype="Healer", char_class_name="Field Medic")
    carlan_initial_alloc = {"Intelligence": 1, "Wisdom": 3, "Spirit": 3, "Agility": 1, "Constitution": 2} # 10 points
    print(f"\nAllocating initial points for {carlan.name}...")
    carlan.allocate_primary_points(INITIAL_ATTRIBUTE_POINTS, MAX_INITIAL_ALLOCATION_PER_ATTRIBUTE, carlan_initial_alloc)
    carlan.display_stats(title="Carlan - After Creation & Initial Allocation")

    # --- 2. Level Advancement ---
    print("\n\n--- Test: Level Advancement ---")
    
    # Leveling Valerius (Tank) to Level 10
    print(f"\n--- Leveling {valerius.name} ---")
    # Lvl 1 -> 2: +1 Str, +1 Con, +1 Spi
    valerius.level_up({"Strength": 1, "Constitution": 1, "Spirit": 1})
    # Lvl 2 -> 3: +1 Str, +1 Con, +1 Wis
    valerius.level_up({"Strength": 1, "Constitution": 1, "Wisdom": 1})
    if valerius.character_level == 3:
        valerius.display_stats(title=f"{valerius.name} - Level 3")

    # Lvl 3 -> 4: +1 Str, +1 Con, +1 Spi
    valerius.level_up({"Strength": 1, "Constitution": 1, "Spirit": 1})
    # Lvl 4 -> 5: +1 Str, +1 Con, +1 Wis
    valerius.level_up({"Strength": 1, "Constitution": 1, "Wisdom": 1})
    if valerius.character_level == 5:
        valerius.display_stats(title=f"{valerius.name} - Level 5")

    # Lvl 5 -> 6: +1 Str, +1 Con, +1 Spi
    valerius.level_up({"Strength": 1, "Constitution": 1, "Spirit": 1})
    # Lvl 6 -> 7: +1 Str, +1 Con, +1 Wis
    valerius.level_up({"Strength": 1, "Constitution": 1, "Wisdom": 1})
    if valerius.character_level == 7:
        valerius.display_stats(title=f"{valerius.name} - Level 7")
    
    # Lvl 7 -> 8: +1 Str, +1 Con, +1 Spi
    valerius.level_up({"Strength": 1, "Constitution": 1, "Spirit": 1})
    # Lvl 8 -> 9: +1 Str, +1 Con, +1 Wis
    valerius.level_up({"Strength": 1, "Constitution": 1, "Wisdom": 1})
    # Lvl 9 -> 10: +1 Str, +1 Con, +1 Spi
    valerius.level_up({"Strength": 1, "Constitution": 1, "Spirit": 1})
    if valerius.character_level == 10:
        valerius.display_stats(title=f"{valerius.name} - Level 10")

    # Leveling Lyra (DPS) to Level 10
    print(f"\n--- Leveling {lyra.name} ---")
    # Lvl 1 -> 2: +1 Int, +1 Wis, +1 Spi
    lyra.level_up({"Intelligence": 1, "Wisdom": 1, "Spirit": 1})
    # Lvl 2 -> 3: +1 Int, +1 Wis, +1 Agi
    lyra.level_up({"Intelligence": 1, "Wisdom": 1, "Agility": 1})
    if lyra.character_level == 3:
        lyra.display_stats(title=f"{lyra.name} - Level 3")

    # Lvl 3 -> 4: +1 Int, +1 Wis, +1 Spi
    lyra.level_up({"Intelligence": 1, "Wisdom": 1, "Spirit": 1})
    # Lvl 4 -> 5: +1 Int, +1 Wis, +1 Agi
    lyra.level_up({"Intelligence": 1, "Wisdom": 1, "Agility": 1})
    if lyra.character_level == 5:
        lyra.display_stats(title=f"{lyra.name} - Level 5")

    # Lvl 5 -> 6: +1 Int, +1 Wis, +1 Spi
    lyra.level_up({"Intelligence": 1, "Wisdom": 1, "Spirit": 1})
    # Lvl 6 -> 7: +1 Int, +1 Wis, +1 Agi
    lyra.level_up({"Intelligence": 1, "Wisdom": 1, "Agility": 1})
    if lyra.character_level == 7:
        lyra.display_stats(title=f"{lyra.name} - Level 7")

    # Lvl 7 -> 8: +1 Int, +1 Wis, +1 Spi
    lyra.level_up({"Intelligence": 1, "Wisdom": 1, "Spirit": 1})
    # Lvl 8 -> 9: +1 Int, +1 Wis, +1 Agi
    lyra.level_up({"Intelligence": 1, "Wisdom": 1, "Agility": 1})
    # Lvl 9 -> 10: +1 Int, +1 Wis, +1 Spi
    lyra.level_up({"Intelligence": 1, "Wisdom": 1, "Spirit": 1})
    if lyra.character_level == 10:
        lyra.display_stats(title=f"{lyra.name} - Level 10")


    # --- 3. Buffing / Debuffing ---
    print("\n\n--- Test: Buffing and Debuffing ---")

    # Buff Valerius (L10 Tank)
    print(f"\n--- Buffing {valerius.name} ---")
    might_buff = Effect(name="Might Of the Vrathan", target_attribute="Might", modifier_type="percentage", value=17, duration_ticks=3)
    valerius.apply_effect(might_buff)
    valerius.display_stats(title=f"{valerius.name} - After Might Buff Applied")
    
    valerius.tick_effects() # Tick 1
    valerius.display_stats(title=f"{valerius.name} - After 1 tick (Might Buff)")
    valerius.tick_effects() # Tick 2
    valerius.display_stats(title=f"{valerius.name} - After 2 ticks (Might Buff)")
    valerius.tick_effects() # Tick 3 (Buff expires)
    valerius.display_stats(title=f"{valerius.name} - After Might Buff Expired")

    # Debuff Lyra (L10 DPS)
    print(f"\n--- Debuffing {lyra.name} ---")
    endurance_debuff = Effect(name="Cough Of Ruin", target_attribute="Endurance", modifier_type="percentage", value=-20, duration_ticks=2) # -20% for 2 ticks
    lyra.apply_effect(endurance_debuff)
    lyra.display_stats(title=f"{lyra.name} - After Endurance Debuff Applied")

    lyra.tick_effects() # Tick 1
    lyra.display_stats(title=f"{lyra.name} - After 1 tick (Endurance Debuff)")
    lyra.tick_effects() # Tick 2 (Debuff expires)
    lyra.display_stats(title=f"{lyra.name} - After Endurance Debuff Expired")

    # Apply multiple effects
    print(f"\n--- Applying Multiple Effects to {valerius.name} ---")
    speed_buff = Effect(name="Talan's Acceleration", target_attribute="Speed", modifier_type="percentage", value=10, duration_ticks=2)
    dex_debuff_flat = Effect(name="Clumsiness Curse", target_attribute="Dexterity", modifier_type="flat", value=-2, duration_ticks=3)
    
    valerius.apply_effect(speed_buff)
    valerius.apply_effect(dex_debuff_flat)
    valerius.display_stats(title=f"{valerius.name} - Speed Buff & Dex Debuff Applied")

    valerius.tick_effects() # Tick 1
    valerius.display_stats(title=f"{valerius.name} - Multi-Effect Tick 1")
    valerius.tick_effects() # Tick 2 (Speed Buff expires)
    valerius.display_stats(title=f"{valerius.name} - Multi-Effect Tick 2")
    valerius.tick_effects() # Tick 3 (Dex Debuff expires)
    valerius.display_stats(title=f"{valerius.name} - All Effects Expired")

    print("\n========= End of Character System Tests =========")
