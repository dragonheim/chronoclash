# Chrono Clash Game Design Document

## Game Overview
The basic lore is that three different time periods have collided in the present day. 5000 years in the past includes swords and sorcery, present day includes tech and guns, while 5000 years in the future includes cyborgs and lasers. The players create and play individuals called **Chrono-Walkers**, humans with the rare ability of perceiving and navigating the fractured timelines. Whether through mutation, ancient bloodline, or experimental augmentation, they are uniquely perceptive to the flows of time in this collision. Their mission? Survive. Discover. Choose.

## Races and Cultural Adjustments
The game will not really have races, but each of the three time periods have different "cultural" adjustments to the following "primary" attributes:

*   **Agility:** Movement speed, reflexes, and reaction time
*   **Constitution:** Stamina, endurance, and health
*   **Strength:** Raw physical power
*   **Intelligence:** Analytical thinking, memory, and learning ability
*   **Spirit:** Belief, emotional fortitude, and intuition
*   **Wisdom:** Judgement, willpower and perception of truth

These attributes start at 10 for a modern day character with slight variations for past and future eras. Additionally, at 1st level, the character starts with 10 points that they can allocate to these attributes, with a limit of no more than 3 per attribute. Then at every level, the character will receive 3 points they can distribute, with no more than 1 point per attribute.

**Time period adjustments:**
*   **Past Era:** +2 Strength, +1 Spirit, and -2 Intelligence.
*   **Future Era:** +2 Intelligence, +1 Agility, and -2 Constitution.

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
`secondary = (primary_a / 2.0) + (primary_b / 4.0) + (primary_c / 4.0)`

For example, Might is `(Strength / 2.0) + (Wisdom / 4.0) + (Agility / 4.0)`.

## Tertiary Attributes
*   **HP:** Character's hit points calculated based on class, level, and the Endurance secondary attribute. This is equal to `(character level + Endurance) * class modifier`.
*   **Armor:** Used to reduce incoming damage, calculated based on their equipment only.
*   **Dodge:** Used to calculate the chance to avoid incoming melee damage and calculated based on class and Speed. This is equal to `Speed * class modifier`.
*   **Mana:** Character's pool of "mana" for use in spells and is calculated based on class, level, and the Energy secondary attribute. This is equal to `(character level + Energy) * class modifier`.
*   **Attack Power (AP):** Represents the character's base offensive capability, influencing the damage dealt by weapons and combat abilities before enemy defenses are applied.
*   **Accuracy:** Represents the character's ability to land their attacks successfully, counteracting the target's Dodge (for melee) or potentially a base evasion chance for ranged/other attacks.

## Spells and Equipment
Under this system "spells" should only buff / debuff secondary attributes, and then have equipment buff / debuff the tertiary attributes, which are:

## Level Range
In the base game, the level range will be levels 1 through 20. Future downloads will allow 10 level increments to the level cap.

## Character Progression and Classes
At character creation, the player will choose a class. After that, at every level divisible by 10, they will have the choice to either continue their existing class(es) or add a new class at level 1. Further if they reach a class level divisible by 10, they will gain an ability unique to that class, called **Ultimates**. These ultimates should provide mechanisms to allow for class synergies. Choosing to multiclass does not grant another starting 10 points nor does it alter the cap of one per attribute per level.

Initially we will have 9 classes, three per time period, focusing on direct / quick damage, slow / graduating time, and healing. Future downloads may include hybrid and support type classes.

**Initial Classes:**
*   **Past:**
    *   **Flameblade:** Melee damage doing quick and direct damage
    *   **Hex Weaver:** Ranged spell damage doing damage over time
    *   **Cleric:** Heals and buffs
*   **Present:**
    *   **Shocktrooper:** Melee damage doing quick and direct damage
    *   **Grenadier:** Ranged spell damage doing damage over time
    *   **Field Medic:** Heals and buffs
*   **Future:**
    *   **Cyberblade:** Melee damage doing quick and direct damage
    *   **Pulse Mage:** Ranged spell damage doing damage over time
    *   **Nano-Surgeon:** Heals and buffs

**Future Expansion Archetypes:**
*   **Tank:**
    *   **Past:**
        *   Champion
    *   **Present:**
        *   Shield
    *   **Future:**
        *   Battleframe
*   **Rogue:**
    *   **Past:**
        *   Thief
    *   **Present:**
        *   Spy
    *   **Future:**
        *   Hacker
*   **Pet users:**
    *   **Past:**
        *   Hunter
    *   **Present:**
        *   Scout Sniper
    *   **Future:**
        *   Drone Pilot

## Skills
We also need 30 - 40 skills, with six that are unique to each time period. Further one skill should be a salvage skill for salvaging equipment for parts.

## Equipment
All equipment is player made, including the best in slot gear and all gear can be repaired and / salvaged.

Equipment will be broken down into three categories: weapons, armor, and accessories. Each of these categories will have a set of base stats that can be modified by the player. The base stats are:
*   **Base Damage:** The base damage of the weapon.
*   **Base Armor:** The base armor of the weapon, armor, or accessory.
*   **Base Accuracy:** The base accuracy of the weapon, armor, or accessory.
*   **Base Dodge:** The base dodge of the weapon, armor, or accessory.
*   **Base HP:** The base HP of the weapon, armor, or accessory.
*   **Base Mana:** The base mana of the weapon, armor, or accessory.
*   **Base Energy:** The base energy of the weapon, armor, or accessory.
*   **Base Speed:** The base speed of the weapon, armor, or accessory.
*   **Base Might:** The base might of the weapon, armor, or accessory.
*   **Base Endurance:** The base endurance of the weapon, armor, or accessory.
*   **Base Willpower:** The base willpower of the weapon, armor, or accessory.
*   **Base Dexterity:** The base dexterity of the weapon, armor, or accessory.

## Zones	
## Initial Zone Descriptions & Details
### 1. Echo Vale - The Scar of Collision
*   **Eras Mixed:** All 3 (Past, Present, Future)
*   **Core Concept:** The chaotic, unstable ground zero where the three timelines first violently merged. Temporal storms constantly shift the landscape, and pockets of pure, unadulterated time from each era can spontaneously manifest and dissipate.
*   **Visuals:** A shattered landscape. Crumbling medieval castle walls are impaled by twisted girders from a modern skyscraper, which itself is partially phased out by shimmering energy fields from a future megastructure. Patches of overgrown forest, cracked asphalt, and crystalline alien flora exist side-by-side. The sky is a maelstrom of colors, with rifts occasionally showing glimpses into other times.
*   **Environmental Hazards:**
    *   **Temporal Storms:** Areas where the dominant time period rapidly shifts, potentially buffing/debuffing players based on their own era (e.g., a Past character getting a boost in a "Past" pocket, but a debuff in a "Future" pocket). May also spawn era-specific temporary hazards (e.g., a hail of arrows, a burst of radiation, a laser grid).
    *   **Echoes:** Ghostly figures and events from different times replay themselves, sometimes harmless, sometimes manifesting as temporary hostile entities.
    *   **Unstable Terrain:** Ground that shifts, disappears, or changes properties.
*   **Inhabitants:**
    *   **Lost Souls:** Confused and desperate individuals from all three eras, often hostile.
    *   **Temporal Scavengers:** Creatures (and humanoids) that have adapted to the chaotic energies, preying on the weak.
    *   **Manifestations:** Purely temporal beings or constructs spawned by the storms.
    *   **Early Faction Scouts:** Representatives from small, fledgling groups trying to understand and survive the collision.
*   **Quest Hooks:**
    *   "Stabilize the Rift": Players help researchers deploy devices to temporarily calm small temporal storms.
    *   "Rescue the Lost": Find and escort stranded individuals to makeshift safe zones.
    *   "Echoes of the Past/Present/Future": Investigate specific, recurring temporal echoes to learn more about the collision or find lost artifacts.
    *   "Resource Scramble": Collect rare, erratically appearing resources unique to the Vale's unstable nature.
*   **Player Level:** Likely a starting zone (1-5 or 1-10), but with dangerous, higher-level pockets that encourage return visits.

### 2. Neo-Babylon - The Ascended & The Ancient
*   **Eras Mixed:** Ancient + Future
*   **Core Concept:** A magnificent, technologically advanced city-state from the Future, which, during the collision, materialized directly above and integrated with a sprawling complex of ancient ziggurats and temples from the Past. The future tech now powers and augments the ancient structures, creating a unique hybrid civilization.
*   **Visuals:** Gleaming chrome and energy conduits snake around weathered stone ziggurats. Hover platforms dock at ancient archways. Holographic displays illuminate hieroglyph-covered walls. The city floats, tethered by massive energy beams to the ziggurat foundations, with cultivated hanging gardens spilling over both future-tech balconies and ancient stone ledges.
*   **Environmental Hazards:**
    *   **Power Fluctuations:** Areas where future-tech systems overload or ancient wards fail, causing energy discharges or magical traps.
    *   **Guard Drones/Constructs:** Automated defenses from both eras.
    *   **Vertigo:** Being a floating city, falling is a real danger.
*   **Inhabitants:**
    *   **Neo-Babylonians:** A society formed from the fusion. Perhaps a ruling class of Future-era humans who have embraced or subjugated the descendants of the Past-era inhabitants.
    *   **Ancient Guardians:** Magically animated statues or spirits bound to the ziggurats, now potentially augmented or corrupted by future tech.
    *   **Tech-Shamans/Priest-Engineers:** Individuals who blend ancient mysticism with future science.
    *   **Dissidents:** Those who resist the fusion or the ruling powers.
*   **Quest Hooks:**
    *   "The Power Core": Investigate instabilities in the city's power source, which might involve navigating both ancient magical wards and future security systems.
    *   "Whispers from Below": Explore the deeper, untouched levels of the ziggurats for ancient secrets or to quell restless spirits.
    *   "Cultural Exchange (or Conflict)": Mediate disputes or pick sides between factions representing the old ways and the new tech.
    *   "Artifact Fusion": Help a craftsman combine ancient relics with future components to create powerful new items.
*   **Player Level:** Mid-level zone (e.g., 10-15 or 15-20).

### 3. Silicon Desert - The Wastes of Progress
*   **Eras Mixed:** Modern + Future
*   **Core Concept:** Once a bustling modern-day technological hub (think Silicon Valley), now a desolate, irradiated wasteland after its advanced AI research facilities went rogue during the collision, unleashing experimental future weaponry and nanites. Scavengers and desperate survivors pick through the ruins.
*   **Visuals:** Sand-blasted ruins of skyscrapers, server farms, and research labs. Rusted husks of modern vehicles alongside sleek, damaged future-tech transports. Patches of the desert glow with eerie radiation or are covered in self-replicating grey goo (nanites). Makeshift settlements huddle in the shadows of colossal, inert war machines.
*   **Environmental Hazards:**
    *   **Radiation Zones:** Areas with high ambient radiation, causing damage over time.
    *   **Rogue AI Defenses:** Automated turrets, security bots, and deadly traps still active.
    *   **Nanite Swarms:** Clouds of microscopic robots that can deconstruct matter (including players) or cause bizarre mutations.
    *   **Sandstorms:** Reduce visibility and can carry hazardous materials.
*   **Inhabitants:**
    *   **Rogue AI Constructs:** From repurposed security bots to terrifying experimental war machines.
    *   **Scavenger Gangs:** Desperate groups of modern and future survivors fighting over scraps.
    *   **Mutated Wildlife:** Creatures warped by radiation and nanites.
    *   **Cyber-Nomads:** Tech-savvy survivors who have adapted to the harsh environment using salvaged future tech.
    *   **The AI "Presence":** Perhaps a non-corporeal, omnipresent AI that communicates or influences events.
*   **Quest Hooks:**
    *   "Data Recovery": Venture into a ruined server farm to retrieve vital information for a faction.
    *   "Silence the Machines": Disable a key AI facility or a particularly dangerous rogue war machine.
    *   "Water Wars": Compete with scavenger gangs for control of scarce, clean water sources.
    *   "Nanite Plague": Find a way to counteract or control a localized nanite outbreak.
*   **Player Level:** Mid-to-high level zone (e.g., 15-20, or a section scaling higher).

### 4. The Verdant Rift - Nature Reclaims, Strangely
*   **Eras Mixed:** Ancient + Modern
*   **Core Concept:** A deep chasm or valley where the collision caused an explosion of hyper-accelerated, unnatural growth. Ancient forests and jungles have violently erupted through modern towns and wilderness areas, with flora and fauna exhibiting bizarre mutations and luminescent properties, often with a "neon" or "bio-digital" aesthetic where nature mimics technology.
*   **Visuals:** Towering, glowing trees with circuit-like patterns on their bark. Vines that pulse with light, ensnaring rusted cars and remnants of modern buildings. Ancient stone ruins overgrown with luminescent moss and flowers that emit strange energies. Rivers flow with glowing, alchemically altered water.
*   **Environmental Hazards:**
    *   **Aggressive Flora:** Carnivorous plants, entangling vines, spore-releasing fungi with various effects (hallucinations, poison, paralysis).
    *   **Unstable Ground:** Overgrown areas hiding pitfalls or quicksand-like bogs.
    *   **Wild Magic Zones:** Pockets where the ancient magic and modern pollutants have created unpredictable magical effects.
*   **Inhabitants:**
    *   **Mutated Wildlife:** Animals from both eras, now warped into fantastical and dangerous forms (e.g., giant insects with metallic carapaces, deer with glowing antlers that discharge energy).
    *   **Primal Cultists:** Modern humans who have regressed, worshipping the bizarre new nature, or ancient tribes empowered by it.
    *   **Dryads/Nature Spirits:** Beings from the ancient world, now altered and potentially hostile due to the unnatural fusion.
    *   **Lost Explorers/Scientists:** Modern individuals trapped while studying the phenomenon.
*   **Quest Hooks:**
    *   "The Heart of the Growth": Investigate the source of the unnatural bloom.
    *   "Purify the Land/Embrace the Change": Choose to help factions seeking to restore balance or those who wish to harness the new energies.
    *   "Specimen Collection": Gather samples of unique flora/fauna for researchers (or alchemists).
    *   "Ruins of the Old World": Explore ancient temples now intertwined with modern debris, seeking lost knowledge or artifacts.
*   **Player Level:** Mid-level zone (e.g., 10-20).

### 5. Chrono Nexus - The Eye of the Storm
*   **Eras Mixed:** All 3 (Past, Present, Future) - Concentrated and Raw
*   **Core Concept:** The absolute epicenter of the temporal collision, a highly volatile and dangerous zone where the fabric of reality is thinnest. Only accessible to high-level, well-prepared players, this area holds profound secrets about the cataclysm and potentially the means to influence it.
*   **Visuals:** A breathtaking and terrifying spectacle. Islands of land from all three eras float in a swirling vortex of raw temporal energy. Fragments of buildings, landscapes, and even starfields from different times are suspended, phasing in and out. Crystallized time formations, rifts showing glimpses into pure past/present/future, and massive, enigmatic structures of unknown origin dominate the "sky."
*   **Environmental Hazards:**
    *   **Extreme Temporal Flux:** Constant, unpredictable shifts in game rules, enemy spawns, and environmental effects. Players might find their abilities suddenly enhanced or nullified.
    *   **Reality Tears:** Unstable rifts that can teleport players, deal massive damage, or summon powerful entities.
    *   **Chrono Radiation:** A unique form of energy that drains resources or inflicts bizarre debuffs.
    *   **Guardians of Time:** Powerful, enigmatic beings that protect the Nexus.
*   **Inhabitants:**
    *   **Temporal Elementals/Aberrations:** Beings made of pure, raw time-energy or creatures catastrophically warped by it.
    *   **Elite Faction Operatives:** The most powerful members of various groups vying for control or understanding of the Nexus.
    *   **Echoes of Primordial Beings:** Entities from before or beyond the known timelines.
    *   **The "Architects" (or their remnants):** Hints of whoever or whatever *caused* the collision, or is trying to manage it.
*   **Quest Hooks:**
    *   "The Final Key": The culmination of a major storyline, seeking an artifact or piece of knowledge within the Nexus.
    *   "Closing the Wound (or Widening It)": A choice-driven quest to either help stabilize the Nexus or harness its chaotic power.
    *   "Confront the Source": Face a powerful entity believed to be responsible for, or a key to understanding, the collision.
    *   "Legendary Materials": The Nexus is the only place to find components for the absolute most powerful crafted gear.
*   **Player Level:** Endgame zone (e.g., Level 20, and scaling higher with expansions). Likely requires attunement quests or group efforts to even enter.
