# Chrono Clash Game Design Document

## Game Overview
The basic lore is that three different time periods have collided in the present day. 5000 years in the past includes swords and sorcery, present day includes tech and guns, while 5000 years in the future includes cyborgs and lasers. The players create and play individuals called **Chrono-Walkers**, humans with the rare ability of perceiving and navigating the fractured timelines. Whether through mutation, ancient bloodline, or experimental augmentation, they are uniquely perceptive to the flows of time in this collision. Their mission? Survive. Discover. Choose.

## Primary Attributes
The game will not really have races, but each of the three eras will have different "cultural" adjustments to the following "primary" attributes:
*   **Agility:** Movement speed, reflexes, and reaction time
*   **Constitution:** Stamina, endurance, and health
*   **Strength:** Raw physical power
*   **Intelligence:** Analytical thinking, memory, and learning ability
*   **Spirit:** Belief, emotional fortitude, and intuition
*   **Wisdom:** Judgement, willpower and perception of truth

These attributes start at 10 for a modern day character with slight variations for past and future eras. Additionally, at 1st level, the character starts with 10 points that they can allocate to these attributes, with a limit of no more than 3 per attribute. Then at every level, the character will receive 3 points they can distribute, with no more than 1 point per attribute.

**Time period adjustments:**
*   **Past Era:** +2 Strength, +1 Spirit, -1 Wisdom, and -2 Intelligence.
*   **Future Era:** +2 Intelligence, +1 Agility, -1 Spirit, and -2 Constitution.

## Secondary Attributes
The server calculates the following "secondary" attributes based on the previous primary attributes:

*   **Might:** Might represents how efficient a character is at using their strength.
    *   `primary_a` is Strength
    *   `primary_b` is Wisdom
    *   `primary_c` is Agility
*   **Endurance:** Endurance represents how efficient a character is at using their constitution.
    *   `primary_a` is Constitution
    *   `primary_b` is Spirit
    *   `primary_c` is Strength
*   **Speed:** Speed represents how efficient a character is at movement over time.
    *   `primary_a` is Agility
    *   `primary_b` is Intelligence
    *   `primary_c` is Constitution
*   **Energy:** Energy represents how large the character's energy pool is.
    *   `primary_a` is Intelligence
    *   `primary_b` is Constitution
    *   `primary_c` is Spirit
*   **Willpower:** Willpower represents how forceful the character is mentally.
    *   `primary_a` is Wisdom
    *   `primary_b` is Strength
    *   `primary_c` is Spirit
*   **Dexterity:** Dexterity represents how well the character can perform fine movements and accuracy of said movements.
    *   `primary_a` is Spirit
    *   `primary_b` is Agility
    *   `primary_c` is Intelligence

The secondary attributes are calculated with the following formula using the primary attributes:
`secondary = (primary_a / 2.0) + (primary_b / 4.0) + (primary_c / 4.0)`. For example, Might is `(Strength / 2.0) + (Wisdom / 4.0) + (Agility / 4.0)`.

## Tertiary Attributes
*   **HP:** Character's hit points calculated based on class, level, and the Endurance secondary attribute. This is equal to `(character level + Endurance) * class modifier`.
*   **Armor:** Used to reduce incoming damage, calculated based on their equipment only.
*   **Dodge:** Used to calculate the chance to avoid incoming melee damage and calculated based on class and Speed. This is equal to `Speed * class modifier`.
*   **Mana:** Character's pool of "mana" for use in spells and is calculated based on class, level, and the Energy secondary attribute. This is equal to `(character level + Energy) * class modifier`.
*   **Attack Power (AP):** Represents the character's base offensive capability, influencing the damage dealt by weapons and combat abilities before enemy defenses are applied.
*   **Accuracy:** Represents the character's ability to land their attacks successfully, counteracting the target's Dodge (for melee) or potentially a base evasion chance for ranged/other attacks.

## Character Flags
Character flags are used to track various states, quests, and conditions of the character. These flags can be set or cleared based on the character's actions, abilities, or status effects. The following is a list of character flags:
*   **Is Dead:** Indicates if the character is dead.
*   **Is Stunned:** Indicates if the character is stunned and unable to act.
*   **Is Frozen:** Indicates if the character is frozen and unable to move.
*   **Is Silenced:** Indicates if the character is silenced and unable to cast spells.
*   **Is Snared:** Indicates if the character is snared and able to move, but very slowly.
*   **Is Rooted:** Indicates if the character is rooted and unable to move.
*   **Is Feared:** Indicates if the character is feared and unable to act.
*   **Is Blinded:** Indicates if the character is blinded and unable to see.
*   **Is Paralyzed:** Indicates if the character is paralyzed and unable to act.
*   **Is Poisoned:** Indicates if the character is poisoned and taking damage over time.
*   **Is Burning:** Indicates if the character is burning and taking damage over time.
*   **Is Charmed:** Indicates if the character is charmed and under the control of a monster.
*   **Is Confused:** Indicates if the character is confused and unable to act normally.
*   **Is Disarmed:** Indicates if the character is disarmed and unable to use their weapon.
*   **Is In Combat:** Indicates if the character is currently in combat or agro with a monster.
*   **Is Stealthed:** Indicates if the character is stealthed and invisible to enemies. (Possible future expansion)
*   **Is Mounted:** Indicates if the character is mounted on a mount. (Possible future expansion)
*   **Is Swimming:** Indicates if the character is swimming and unable to use certain abilities. (Possible future expansion)
*   **Is Sprinting:** Indicates if the character is sprinting and unable to use certain abilities.
*   **Is Flying:** Indicates if the character is flying and able to move freely in the air. (Possible future expansion)
*   **Is Underwater:** Indicates if the character is underwater and unable to use certain abilities. (Possible future expansion)
*   **Is In Party:** Indicates if the character is in a party with other players.
*   **Is In Guild:** Indicates if the character is in a guild with other players.
*   **Is In Raid:** Indicates if the character is in a raid with other players.


## Spells
Under this system "spells" should only buff / debuff secondary attributes, and then have equipment buff / debuff the tertiary attributes. damage or heal spells are the only ones that directly affect HP.

Spells will be divided into three categories: buffs, debuffs, and damage. Buffs will increase the secondary attributes of the caster or their allies. Debuffs will decrease the secondary attributes of the target. Damage spells will deal damage to the target based on their primary attributes. Additionally, we will use specific damage types (e.g., fire, ice, lightning, etc.) that will be resisted by specific armor types. The damage type will be based on the class of the character using the spell.

Spells can be resisted, but will always hit the target. The amount of damage or healing done will be based on the primary attributes of the caster and the secondary attributes of the target. The following is a list of spell types:

*   **Buffs:** Increase the secondary attributes of the target or their allies.
    *   **Example:** Talan's Acceleration - A spell that increases the target's Speed by 10% for 10 ticks.
    *   **Example:** Might Of the Vrathan - A spell that increases the target's Might by 17% for 10 ticks.
*   **Debuffs:** Decrease the secondary attributes of the target.
    *   **Example:** Cough Of Ruin - A spell that decreases the target's Endurance by 5% for 50 ticks.
*   **Damage:** Deal damage to the target based on their primary attributes.
    *   **Example:** Energy Beam - A spell that deals 35 points of damage based on the caster's Strength and Intelligence.
    **Healing:** Heal the target based on the caster's Willpower and Energy attributes.
    *   **Example:** Healing Wave - A spell that heals, 2 points per tick for 10 ticks, the target based on the caster's Willpower and Energy attributes.

## Ultimate Abilities
Ultimates are powerful abilities that can be used once per encounter. They are unique to each class and are unlocked at level 10 and every 10 levels thereafter. Ultimates will have a cooldown of 5 minutes and will be available for use in combat. Each class will have an offensive and defensive ultimate ability. The following is a list of ultimate abilities:
*   **Flameblade:** 
    *   **Offensive:** Flame Burst - A powerful fire attack that deals 100% of the caster's Might as damage to all enemies in a 10-meter radius.
    *   **Defensive:** Flame Shield - A shield that absorbs 50% of incoming damage for 10 ticks.
*   **Hex Weaver:** 
    *   **Offensive:** Shadow Grasp - A dark spell that deals 80% of the caster's Willpower as damage over 5 ticks to a single target.
    *   **Defensive:** Ethereal Veil - A protective barrier that reduces all incoming damage by 30% for 10 ticks.
*   **Cleric:**
    *   **Offensive:** Holy Smite - A radiant attack that deals 50% of the caster's Spirit as damage to all enemies in a 10-meter radius.
    *   **Defensive:** Divine Protection - A shield that absorbs 30% of incoming damage for 10 ticks and heals the target for 20% of their max HP.
*   **Shocktrooper:**   
    *   **Offensive:** Shockwave - A powerful electric attack that deals 100% of the caster's Strength as damage to all enemies in a 10-meter radius.
    *   **Defensive:** Electric Shield - A shield that absorbs 50% of incoming damage for 10 ticks and stuns all enemies in a 5-meter radius.
*   **Grenadier:**  
    *   **Offensive:** Grenade Barrage - A powerful explosive attack that deals 80% of the caster's Intelligence as damage over 5 ticks to a single target.
    *   **Defensive:** Smoke Screen - A protective barrier that reduces all incoming damage by 30% for 10 ticks and blinds all enemies in a 5-meter radius.
*   **Field Medic:**        
    *   **Offensive:** Healing Grenade - A powerful healing attack that heals 50% of the caster's Spirit as damage to all allies in a 10-meter radius.
    *   **Defensive:** Healing Aura - A shield that absorbs 30% of incoming damage for 10 ticks and heals all allies in a 5-meter radius for 20% of their max HP.
*   **Cyberblade:**
    *   **Offensive:** Cyber Slash - A powerful cyber attack that deals 100% of the caster's Strength as damage to all enemies in a 10-meter radius.
    *   **Defensive:** Cyber Shield - A shield that absorbs 50% of incoming damage for 10 ticks and stuns all enemies in a 5-meter radius.   
*   **Pulse Mage:**
    *   **Offensive:** Pulse Wave - A powerful energy attack that deals 80% of the caster's Intelligence as damage over 5 ticks to a single target.
    *   **Defensive:** Energy Shield - A shield that absorbs 30% of incoming damage for 10 ticks and heals the target for 20% of their max HP.
*   **Nano-Surgeon:**
    *   **Offensive:** Nano Burst - A powerful AOE heal for 50% of the caster's Spirit as healing to all allies in a 10-meter radius and dealing 50% of the caster's Spirit as damage to all enemies in a 10-meter radius.
    *   **Defensive:** Nano Shield - A shield that absorbs 30% of incoming damage for 10 ticks and heals all allies in a 5-meter radius for 20% of their max HP.

## Level Range
In the base game, the level range will be levels 1 through 20. Future downloads will allow 10 level increments to the level cap.

## Character Progression and Classes
At character creation, the player will choose a class. After that, at every level divisible by 10, they will have the choice to either continue their existing class(es) or add a new class at level 1. Further if they reach a class level divisible by 10, they will gain an ability unique to that class, called **Ultimates**. These ultimates should provide mechanisms to allow for class synergies. Choosing to multiclass does not grant another starting 10 points nor does it alter the cap of one per attribute per level.

Initially we will have 9 classes, three per time period, focusing on direct / quick damage, slow / graduating time, and healing. Future downloads may include hybrid and support type classes.

**Initial Classes:**
*   **Past:**
    *   **Flameblade(Tank):** Melee damage doing quick and direct damage.
    *   **Hex Weaver(DPS):** Ranged spell damage doing damage over time.
    *   **Cleric(Healer):** Heals and buffs.
*   **Present:**
    *   **Shocktrooper(Tank):** Melee damage doing quick and direct damage.
    *   **Grenadier(DPS):** Ranged spell damage doing damage over time.
    *   **Field Medic(Healer):** Heals and buffs.
*   **Future:**
    *   **Cyberblade(Tank):** Melee damage doing quick and direct damage.
    *   **Pulse Mage(DPS):** Ranged spell damage doing damage over time.
    *   **Nano-Surgeon(Healer):** Heals and buffs.

    Initial class archetype modifiers are as follows:
*   **Tank:**
        hp_mod = (10 * class level) + endurance.
        mana_mod = (4 * class level) + energy.
        dodge_mod = (4 * class level) + dexterity.
        ap_mod = (4 * class level) + might.
        accuracy_mod = (6 * class level) + speed.
*   **DPS:**
        hp_mod = (4 * class level) + endurance.
        mana_mod = (10 * class level) + energy.
        dodge_mod = (3 * class level) + dexterity.
        ap_mod = (7 * class level) + willpower.
        accuracy_mod = (6 * class level) + speed.
*   **Healer:**
        hp_mod = (7 * class level) + endurance.
        mana_mod = (7 * class level) + energy.
        dodge_mod = (3 * class level) + dexterity.
        ap_mod = (4 * class level) + willpower.
        accuracy_mod = (4 * class level) + speed.
*   **Rogue:**
        hp_mod = (7 * class level) + endurance.
        mana_mod = (7 * class level) + energy.
        dodge_mod = (3 * class level) + dexterity.
        ap_mod = (4 * class level) + dexterity.
        accuracy_mod = (10 * class level) + speed.
*   **Pet User:**
        hp_mod = (4 * class level) + endurance.
        mana_mod = (7 * class level) + energy.
        dodge_mod = (3 * class level) + dexterity.
        ap_mod = (4 * class level) + willpower.
        accuracy_mod = (2 * class level) + speed.

**Possible Future Expansion Classes:**
*   **Rogue:**
    *   **Past:**
        *   Assassin
        *   Thief
    *   **Present:**
        *   Bounty Hunter
        *   Spy
    *   **Future:**
        *   Infiltrator
        *   Hacker
*   **Pet User:**
    *   **Past:**
        *   Beastmaster
        *   Hunter
    *   **Present:**
        *   Animal Handler
        *   Scout Sniper
    *   **Future:**
        *   Cyber Beastmaster
        *   Drone Pilot

## Monsters
Monsters will be divided into five categories: common, uncommon, rare, elite, and legendary. Monsters will have the same primary, secondary, and tertiary attributes as players. Additionally, monsters will have a level, which will determine their difficulty and the loot they drop. The level of the monster will be based on the level of the player, with a maximum level of 20, with a few exceptions, in the initial release. Health calculations will be the same as players, with the following formula: `(hp = (monster level * 10) + endurance) * category modifier`, with the following category modifiers:
*   **Common:** 1.0
*   **Uncommon:** 2.5
*   **Rare:** 5.0
*   **Elite:** 10.0
*   **Legendary:** 20.0
Monsters will also have a set of abilities that they can use in combat. These abilities will be determined based on the monster's class and will have a normal cooldown period. The following is a list of monster abilities. Monsters will have a flat AC value as they do not wear armor, but will have a dodge value based on their agility and speed secondary attributes. Further, all monsters will have special abilities, as defined in the monster's data.

## Crafting / Gathering Skills
We also need 15 - 20 crafting and gathering skills as well as a skill for salvaging equipment. The Salvaging skill will be common among the different eras. Skills will be leveled up by using them, with a maximum level of 100 (60 in the initial release). Each skill will have a set of recipes that can be learned as the skill is leveled up. The recipes will be divided into three tiers: common, uncommon, and rare. Each tier will have a set of base stats that can be modified by the player. The base stats apply flat bonuses to secondary attributes.

Additionally, we need 3 skills per time period, with three that are common across all time periods, and then three more that are unique to each time period. The common skills will be used for gathering resources, while the unique skills will be used for crafting equipment.
The common skills will be used for gathering resources, while the unique skills will be used for crafting equipment. The following is a list of skills:
*   **Common Skills:**
    *   **Salvaging:** Salvaging equipment to yield parts that can be used to craft new equipment or upgrade existing equipment.
    *   **Mining:** Gathering resources from the ground, such as ores and gems.
    *   **Herbalism:** Gathering resources from plants, such as herbs and flowers.
*   **Past Era Unique Skills:** 
    *   **Blacksmithing:** Crafting weapons and armor from metal.
    *   **Alchemy:** Crafting potions and elixirs from herbs and minerals.
    *   **Enchanting:** Imbuing items with magical properties.
*   **Present Era Unique Skills:**  
    *   **Engineering:** Crafting gadgets and devices from metal and electronics.
    *   **Chemistry:** Crafting explosives and chemical weapons from chemicals and minerals.
    *   **Hacking:** Crafting software and hardware to manipulate technology.
*   **Future Era Unique Skills:**
    *   **Nanotechnology:** Crafting devices and enhancements using nanites and advanced materials.
    *   **Cybernetics:** Crafting cybernetic implants and augmentations for characters.
    *   **Quantum Mechanics:** Crafting devices that manipulate time and space, such as teleporters or time dilation fields.

## Combat
Combat will be real-time, with players able to move and attack at the same time. Players will be able to use their primary and secondary attributes to determine their damage output and survivability. The combat system will also include a dodge mechanic, allowing players to avoid incoming attacks. Additionally, players will be able to use spells and abilities to buff or debuff themselves or their allies, as well as deal damage to enemies.

Combat will be divided into three categories: melee, ranged, and spellcasting. Each category will have its own set of abilities and mechanics. The following is a list of combat mechanics:
*   **Melee Combat:** Melee range is considered to be 5 meters or less. Players will be able to use their weapons to attack enemies in close range. Melee combat will include a basic attack, as well as abilities that can be used to deal additional damage or debuff enemies.
    *   **Basic Attack:** A quick, low-damage attack that can be used repeatedly.
    *   **Abilities:** Special attacks that can be used to deal additional damage or debuff enemies. These will have a cooldown period and require mana to use.
*   **Ranged Combat:** Ranged combat, other than spells, will be combat between 5 and 70 meters.Players will be able to use their ranged weapons to attack enemies from a distance. Ranged combat will include a basic attack, as well as abilities that can be used to deal additional damage or debuff enemies.
    *   **Basic Attack:** A quick, low-damage attack that can be used repeatedly.
    *   **Abilities:** Special attacks that can be used to deal additional damage or debuff enemies. These will have a cooldown period and require mana to use.
*   **Spellcasting:** Spells will have a range of 0 - 70 meters, Ultimate, with a range, will be effective up to 100 meters. Players will be able to use their spells to deal damage, heal allies, or debuff enemies. Spellcasting will include a basic spell, as well as abilities that can be used to deal additional damage or debuff enemies.
    *   **Basic Spell:** A quick, low-damage spell that can be used repeatedly.
    *   **Abilities:** Special spells that can be used to deal additional damage, heal allies, or debuff enemies. These will have a cooldown period and require mana to use.

### Ticks
Combat will be based on a tick system, where each tick represents a short period of time (e.g., 3 seconds). Players and monsters will regenerate a small amount of mana and health each tick, and abilities will have a cooldown period that is based on the number of ticks. Additionally, players will be able to use abilities that can affect the number of ticks, such as reducing the cooldown period or increasing the regeneration rate.

### Damage types
Damage types will be used to determine the effectiveness of attacks against different armor types. Each weapon and spell will have a damage type, and each armor type will have a resistance to certain damage types. The following is a list of damage types:
*   **Slashing:** Effective against light armor, but less effective against heavy armor.
*   **Piercing:** Effective against heavy armor, but less effective against light armor.
*   **Bludgeoning:** Effective against heavy armor, but less effective against light armor.
*   **Fire:** Effective against light armor, but less effective against heavy armor.
*   **Ice:** Effective against heavy armor, but less effective against light armor.
*   **Lightning:** Effective against light armor, but less effective against heavy armor.
*   **Acid:** Effective against heavy armor, but less effective against light armor.
*   **Void:** Effective against all armor types, but less effective against shields.
*   **Temporal:** Effective against all armor types, but less effective against shields.
*   **Kinetic:** Effective against all armor types, but less effective against shields.
  
## Equipment
All equipment is player made, including the best in slot gear and all gear can be repaired and salvaged. Additionally all equipment has a durability value that decreases with use. When the durability reaches 0, the equipment is completely destroyed. As long and the equipment has at least 1 durability point, it can be repaired by players with the appropriate crafting skill or by NPCs in towns. Salvaging equipment requires that the item's durability is at least 10, will yield parts that can be used to craft new equipment or upgrade existing equipment.

All equipment will have a level requirement, which will determine the minimum character level required to equip the item. Additionally, equipment will have a rarity value, which will determine the quality of the item. The rarity value will be based on the level requirement and the base stats of the item. The following is a list of rarity values:
*   **Common:** Minimum Level 1 (not shown), basic stats, no special properties.
*   **Uncommon:** Minimum Level 6, improved stats, minor special properties.
*   **Rare:** Minimum Level 11, significantly improved stats, moderate special properties.
*   **Elite:** Minimum Level 16, greatly improved stats, major special properties.
*   **Legendary:** Minimum Level 20, exceptional stats, unique special properties.

Level requirements to euip is the same as the level requirements to make and repair the item. The level requirements to make and repair the item are based on the rarity of the item, with common items being the easiest to make and repair, and legendary items being the most difficult.

Equipment quality will be divided into five tiers: common, uncommon, rare, elite, and legendary. Each tier will have a set of base stats that can be modified by the player. The base stats apply flat bonuses to secondary attributes:

Equipment will be broken down into three types: weapons, armor, and accessories. Each of these types will have a set of base stats that can be modified by the player. The base stats apply flat bonuses to tertiary abilities:
*   **Base Damage:** The base damage of the weapon.
*   **Base Armor:** The base armor of the armor or accessory.
*   **Base Accuracy:** The base accuracy of the weapon.
*   **Base Dodge:** The base dodge of the armor or accessory.
*   **Base HP:** The base HP of the armor or accessory.
*   **Base Mana:** The base mana of the weapon or accessory.
*   **Base AP:** The base attack power of the weapon or accessory.

Equipment location will determine the main tertiary attribute, each item can affect multiple tertiary attributes, but the main will always be included in the list. Also note that equipment can also reduce tertiary attributes, but the main tertiary attribute will always be a positive value. The following is a list of equipment locations and their main tertiary attributes:
*   **Head:** Helmets, masks, and headbands. Main tertiary attribute: Mana.
*   **Chest:** Armor, shirts, and jackets. Main tertiary attribute: Armor.
*   **Legs:** Pants, skirts, and shorts. Main tertiary attribute: Armor.
*   **Shoulders:** Pauldrons, capes, and cloaks. Main tertiary attribute: Attack Power.
*   **Arms:** Sleeves, bracers, and armguards. Main tertiary attribute: Accuracy.
*   **Feet:** Boots, shoes, and sandals. Main tertiary attribute: Dodge.
*   **Hands:** Gloves, gauntlets, and bracers. Main tertiary attribute: Accuracy.
*   **Waist:** Belts, sashes, and girdles. Main tertiary attribute: HP.
*   **Neck:** Necklaces, amulets, and pendants. Main tertiary attribute: HP.
*   **Back:** Capes, cloaks, and wings. Main tertiary attribute: Mana.
*   **Main Hand Weapon:** Swords, axes, and staves. Main tertiary attribute: Damage.
*   **Off Hand Weapon:** Shields, wands, and orbs. Main tertiary attribute: Damage.
*   **Ranged Weapon:** Bows, crossbows, and guns. Main tertiary attribute: Damage.
*   **Ring:** Signet rings, wedding bands, and magical rings. Main tertiary attribute: Mana.

## Movement
Movement will be based on a grid system, with each square representing a 1-meter by 1-meter area. Players will be able to move in any direction, including diagonally, and will be able to move through obstacles that are not solid. Additionally, players will be able to use abilities that can affect their movement, such as increasing their speed or teleporting to a different location.

Average run speed will be 2.7 meters per second (10km/h), with a maximum sprint speed of 5.4 meters per second (20km/h). Players will be able to use abilities that can increase their movement speed, such as sprinting or teleporting. Additionally, players will be able to use abilities that can affect their movement, such as slowing down enemies or teleporting to a different location.

Monsters will also be able to move in any direction, but will not be able to teleport. Additionally, monsters will have a set of movement abilities that can be used to chase down players or escape from combat. Monsters will have an average movement speed based on their category, with the following formula: `movement_speed = category_mod + 1.7` in meters per second, with the following category modifiers:
*   **Common:** 1.0
*   **Uncommon:** 1.5
*   **Rare:** 2.0
*   **Elite:** 2.5
*   **Legendary:** 3.0

### Sprinting
Players can use their abilities while moving at normal speed, but will be unable to use any abilities while sprinting.

Sprinting will temporarily decrease the player's energy pool, which will regenerate over time after they stop sprinting. This temporary loss of energy will affect appropriate tertiary attributes.

Monsters will also be able to sprint, but only when chasing down players or escaping from combat. Monsters will have a set of sprinting abilities that can be used to increase their movement speed for a short period of time.

## User Interface
The user interface will be designed to be intuitive and easy to use. The main screen will display the player's character, their health and mana bars, and their action bar. The action bar will contain the player's abilities and spells, which can be used in combat. Additionally, the user interface will include a minimap, which will display the player's location and the locations of nearby monsters and players.

### Action Bar
The action bar will be divided into three sections: abilities, spells, and items. Each section will have a set of slots that can be used to place abilities, spells, or items. Players will be able to drag and drop abilities, spells, macros, and items into the action bar, and will be able to use them in combat by clicking on the corresponding slot.

### Minimap
The minimap will display the player's location and the locations of nearby players. Players will be able to click on the minimap to set waypoints and navigate the game world.

### Character Sheet
The character sheet will display the player's primary, secondary, tertiary attributes, and resistances, as well as their equipment and inventory. Players will be able to view their character's stats, abilities, and equipment by clicking on the character sheet button in the user interface.

### Inventory Window
The inventory window will display the player's equipment, items, and resources. Players will be able to drag and drop items into their inventory, and will be able to use items by clicking on them in the inventory window. Additionally, players will be able to sort their inventory by category, rarity, or level requirement.

### Quest Log
The quest log will display the player's current quests, as well as their progress towards completing them. Players will be able to view their quests by clicking on the quest log button in the user interface. The quest log will also include a map that shows the locations of quest objectives and NPCs.

### Lore Window
The lore window will display information about the game's lore, including the history of the game world, the different factions, and the various characters that inhabit it. Players will be able to view the lore by clicking on the lore button in the user interface. This window will be populated as players progress and collect various lore, quest, and flag items.

### Map
The map will display the player's current location and the locations of nearby players, monsters, and quest objectives. Players will be able to zoom in and out of the map, and will be able to set waypoints to navigate the game world. Additionally, players will be able to view the map in different modes, such as a top-down view or a 3D view.

### Offensive Target Window
The offensive target window will display information about the player's current target, including their health, mana, and other relevant stats. Players will be able to use this window to track their target's status and make informed decisions during combat.

### Defensive Target Window
The defensive target window will display information about the player's current target, including their health, mana, and other relevant stats. Players will be able to use this window to track their target's status and make informed decisions during combat. Additionally, players will be able to use this window to track the status of their allies and make informed decisions during combat.

### Party / Group Window
The party / group window will display information about the player's party members, including their health, mana, and other relevant stats. Players will be able to use this window to track their party's status and make informed decisions during combat. Additionally, players will be able to use this window to invite other players to join their party or leave their party.

### Guild Window
The guild window will display information about the player's guild, including their members, their leader, and their guild level. Players will be able to use this window to track their guild's status and make informed decisions during gameplay. Additionally, players will be able to invite other players to join their guild or leave their guild.

### Raid Window
The raid window will display information about the player's current raid, including their members, their leader, and their raid level. Players will be able to use this window to track their raid's status and make informed decisions during gameplay. Additionally, players will be able to invite other players to join their raid or leave their raid.

### Macro Window
The macro window will allow players to create and manage macros, which are custom commands that can be used to automate certain actions in the game. Players will be able to create macros for abilities, spells, items, and other actions, and will be able to assign them to hotkeys for quick access during gameplay. The macro system will support a wide range of commands, including conditional statements, loops, and timers, allowing players to create complex macros that can enhance their gameplay experience.

### Chat Window
The user interface will also include a chat window, which will allow players to communicate with each other. The chat window will support both text and voice chat, and will allow players to create and join channels for specific topics or groups.

The chat system will support multiple channels, including:
*   **Global:** A channel for all players to communicate with each other.
*   **Trade:** A channel for players to buy and sell items.
*   **Guild:** A channel for players to communicate with their guild members.
*   **Party:** A channel for players to communicate with their party members.
*   **Whisper:** A private channel for players to communicate with each other.

Additionally, items can be linked in the chat window, allowing players to share information about items they have found or crafted. Players can also use emotes to express themselves in the chat window, such as waving or dancing.

Ultimately, we would like to make the chat system extensible, allowing for custom channels and commands to be added by players or server administrators, with support for external chat services like Discord or Slack.

## Inventory
The inventory system will be designed to be intuitive and easy to use. Players will have a limited number of inventory slots, which will be used to store their equipment, items, and resources. The inventory will be divided into three categories: equipment, items, and resources.
*   **Equipment:** This category will include the player's weapons, armor, and accessories. Each piece of equipment will have a level requirement and a rarity value, which will determine its quality and effectiveness.
*   **Items:** This category will include consumable items, such as potions and food, as well as quest items and crafting materials. Items will have a limited number of uses or a limited duration, after which they will be consumed or expire.
*   **Resources:** This category will include crafting materials, such as ores and herbs.
Players will be able to gather resources from the environment, such as mining ores or harvesting herbs, and will be able to use these resources to craft new equipment or upgrade existing equipment.
The inventory system will also include a search function, allowing players to quickly find specific items or equipment. Additionally, players will be able to sort their inventory by category, rarity, or level requirement.

## Quests
Quests will be divided into three categories: main quests, side quests, and daily quests. Quests will be used to guide players through the game and provide them with rewards for completing specific tasks. The following is a list of quest types:
*   **Main Quests:** These quests will be the primary storyline of the game and will guide players through the main plot. Completing main quests will unlock new areas, abilities, and equipment.
*   **Side Quests:** These quests will be optional and will provide players with additional rewards and challenges. Side quests will often involve helping NPCs, defeating monsters, or gathering resources.
*   **Daily Quests:** These quests will reset every day and will provide players with a set of tasks to complete for additional rewards. Daily quests will often involve defeating specific monsters, gathering resources, or completing specific objectives.

Quest items will be converted to character flags on acquisition, ensuring that quest items do not take up inventory space. Additionally, quest items will be automatically removed from the player's inventory when the quest is completed, allowing players to focus on their current objectives without cluttering their inventory with quest-related items. In the case of manufactured quest items, they will convert to inventory items upon completion of the quest, allowing players to keep the item for future use or trade.

## Currency and Economy
“Chronite glows faintly when near temporal rifts. Some say it was once part of the Vrathan’s loom.” – Marta Hahland 

The game will have a currency system that will be used to buy and sell items, equipment, and schematics. The currency system will include both a base currency only and will only be used for p2p transactions and trades and costs of renting "crafting" stations.

The in-game currency will be called Chronite (CRN) and is an era-agnostic currency. It will be used to buy and sell items, equipment, and schematics. Players will be able to earn Chronite by completing quests, defeating monsters, and selling items to vendors or other players.
Additionally, players will be able to trade items and equipment with each other using Chronite as the currency. The economy will be player-driven, with players setting the prices for items and equipment based on supply and demand.

The game will include a coin sink to help balance the economy and prevent inflation. The coin sink will include:
*   **Repair Costs:** Players will need to pay a fee to repair their equipment, which will help to remove excess currency from the economy.
*   **Crafting Costs:** Players will need to pay a fee to craft new equipment, which will help to remove excess currency from the economy.
*   **Trading Costs:** Players will need to pay a fee to trade items and equipment with each other.
*   **Auction House Fees:** Players will need to pay a fee to list items for sale in the auction house, which will help to remove excess currency from the economy.
*   **Guild Fees:** Players will need to pay a fee to create or maintain a guild, which will help to remove excess currency from the economy. Additionally, guilds will be able to set a small fee for using their guild's crafting stations

### Obtaining CRN
  **Monster Loot:** Every monster drops Chronite and loot based on its level and rarity.
  Common: 3–5 CRN
  Uncommon: 5–10 CRN
  Rare: 10–30 CRN
  Elite: 30–55 CRN
  Legendary: 55–75 CRN

  **Daily Monster Quotas:** Players can complete daily kill lists for bonus Chronite (e.g., “Slay 10 Elite Chrono-Mummies”).
