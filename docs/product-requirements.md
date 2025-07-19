# Product Requirements Document: Chrono Clash

**Version:** 1.0

**Date:** May 24, 2024

## 1. Introduction

### 1.1. Overview
Chrono Clash is a foundational, cooperative PVE (Player vs. Environment) MMORPG project where three distinct time periods—a magical Past, a technological Present, and a cybernetic Future—have catastrophically collided. Players assume the role of "Chrono-Walkers," rare individuals capable of perceiving and navigating the fractured timelines. The project serves as both a playable game prototype and a learning resource for MMORPG development, demonstrating core concepts like networking, character progression, and combat on a large world grid.

### 1.2. Purpose
This document outlines the product requirements for the initial release (Minimum Viable Product) of the Chrono Clash server and client. It defines the scope, features, and functionality required to deliver a core gameplay experience.

### 1.3. Target Audience
*   **Players:** Fans of MMORPGs who enjoy theory-crafting character builds, exploring unique worlds, and engaging in cooperative PVE combat and crafting.
*   **Developers:** Individuals and teams interested in learning about or contributing to open-source MMO game development.

## 2. Project Goals & Objectives

*   **Primary Goal:** To create a stable, functional server and a simple client that demonstrates the core gameplay loop of an MMORPG.
*   **Learning Objective:** To serve as a learning resource and a foundational codebase for exploring MMO architecture, including networking, game mechanics, and data management.
*   **Community Objective:** To build a potential starting point for a larger, open-source, community-driven MMO project.

## 3. Features & Requirements

### 3.1. Core Gameplay Loop

*   **FR-3.1.1: Combat:** The game must support real-time combat.
    *   **FR-3.1.1.1:** Combat shall be tick-based (defined as 3 seconds per tick) for status effects, cooldowns, and resource regeneration.
    *   **FR-3.1.1.2:** Melee (<=5m), Ranged (5-70m), and Spell (0-70m) combat categories must be implemented with distinct ranges.
    *   **FR-3.1.1.3:** A damage system incorporating weapon base damage, Attack Power, and target armor must be implemented.
    *   **FR-3.1.1.4:** The system must support multiple damage types (e.g., Slashing, Fire, Temporal) and resistances.
*   **FR-3.1.2: Leveling & Progression:**
    *   **FR-3.1.2.1:** The character level cap for the initial release shall be 20.
    *   **FR-3.1.2.2:** Players shall receive attribute points upon leveling up to distribute among primary attributes.
*   **FR-3.1.3: Quests:**
    *   **FR-3.1.3.1:** The system must support Main, Side, and Daily quests.
    *   **FR-3.1.3.2:** Quest items must be handled as character flags to avoid using inventory space, converting to real items only upon quest completion if applicable.

### 3.2. Character System

*   **FR-3.2.1: Character Creation:**
    *   **FR-3.2.1.1:** Players must be able to create a character by selecting a name, a time period (Past, Present, Future), and an initial class.
    *   **FR-3.2.1.2:** Players must be able to allocate an initial pool of 10 attribute points, with a maximum of 3 points per attribute.
*   **FR-3.2.2: Attributes:**
    *   **FR-3.2.2.1:** Characters shall have 6 Primary Attributes (Agility, Constitution, Strength, Intelligence, Spirit, Wisdom).
    *   **FR-3.2.2.2:** Time period selection must apply predefined modifiers to starting primary attributes.
    *   **FR-3.2.2.3:** 6 Secondary Attributes (Might, Endurance, etc.) must be calculated from Primary Attributes based on the GDD formula.
    *   **FR-3.2.2.4:** Tertiary Attributes (HP, Mana, etc.) must be calculated based on class, level, and Secondary Attributes.
*   **FR-3.2.3: Classes & Abilities:**
    *   **FR-3.2.3.1:** The initial release must include 9 classes, three for each time period, covering Tank, DPS, and Healer archetypes.
    *   **FR-3.2.3.2:** The system must support multiclassing at level 10.
    *   **FR-3.2.3.3:** Each class must have access to unique offensive and defensive "Ultimate" abilities, unlocked at level 10.
    *   **FR-3.2.3.4:** The system must support buff and debuff spells that modify secondary attributes.
*   **FR-3.2.4: Character State:**
    *   **FR-3.2.4.1:** A character flag system must be implemented to track states (e.g., Is Dead, Is In Combat, Is Stunned).

### 3.3. World & Environment

*   **FR-3.3.1: Zones:**
    *   **FR-3.3.1.1:** The game world shall be grid-based (1m x 1m squares).
    *   **FR-3.3.1.2:** The initial release must include at least two zones: Seattle (starting zone, Lvl 1-5) and Echo Vale (Lvl 1-10).
*   **FR-3.3.2: Monsters:**
    *   **FR-3.3.2.1:** The system must support monsters with attributes, levels, and abilities similar to players.
    *   **FR-3.3.2.2:** Monster difficulty shall be categorized (Common, Uncommon, Rare, Elite, Legendary), affecting their stats and loot.
    *   **FR-3.3.2.3:** Monsters from the provided bestiary shall be implemented in their respective zones.
*   **FR-3.3.3: NPCs:**
    *   **FR-3.3.3.1:** The system must support non-player characters for quest-giving, vending, and lore exposition.
    *   **FR-3.3.3.2:** Key lore characters (e.g., Lythia Culverson, Dr. Elias Kwan) shall be present in Seattle to guide players.

### 3.4. Systems

*   **FR-3.4.1: Equipment:**
    *   **FR-3.4.1.1:** The system must support equippable items in various slots (Head, Chest, Weapon, etc.).
    *   **FR-3.4.1.2:** Equipment shall have rarity tiers (Common to Legendary) with corresponding level requirements.
    *   **FR-3.4.1.3:** Equipment must have a durability value that decreases with use and can be repaired.
    *   **FR-3.4.1.4:** All equipment must be craftable by players.
*   **FR-3.4.2: Crafting & Gathering:**
    *   **FR-3.4.2.1:** The initial release must include 3 common gathering skills (Salvaging, Mining, Herbalism) and at least one crafting skill per era (e.g., Blacksmithing, Engineering, Nanotechnology).
    *   **FR-3.4.2.2:** Skills shall be leveled up through use, up to a cap of 60 for the initial release.
*   **FR-3.4.3: Inventory:**
    *   **FR-3.4.3.1:** Players must have a personal inventory with a limited number of slots to store equipment, items, and resources.
*   **FR-3.4.4: Economy:**
    *   **FR-3.4.4.1:** The game shall have a single currency, Chronite (CRN).
    *   **FR-3.4.4.2:** The system must support player-to-player trading.
    *   **FR-3.4.4.3:** Basic coin sinks (e.g., repair costs, crafting station fees) must be implemented.

### 3.5. User Interface (UI)

*   **FR-3.5.1:** A simple client UI must be developed, including the following windows/elements:
    *   Main display (Health/Mana bars, Action Bar)
    *   Character Sheet (displaying all attributes and equipment)
    *   Inventory Window
    *   Quest Log
    *   Map & Minimap
    *   Chat Window
    *   Targeting Windows (Offensive/Defensive)
    *   Party/Group Window

### 3.6. Social Features

*   **FR-3.6.1: Chat:**
    *   **FR-3.6.1.1:** The chat system must support multiple channels (Global, Party, Whisper).
    *   **FR-3.6.1.2:** Players must be able to link items in chat.
*   **FR-3.6.2: Grouping:**
    *   **FR-3.6.2.1:** Players must be able to form parties to play together.

### 3.7. Technical Requirements

*   **TR-3.7.1:** A server application must be developed to manage game state, character data, and network communication. The server must run in a Linux container and support up to 1000 concurrent players. The server will need to log all character and player interactions for diagnostic purposes.
*   **TR-3.7.2:** A simple client application must be developed for players to connect to the server and interact with the game world. The client must run on Windows and Linux, using Unreal Engine 5.
*   **TR-3.7.3:** Player data (character progression, inventory) must be saved, though initial implementation will use SQLite3.

## 4. Scope

### 4.1. In Scope (MVP)

*   Character levels 1-20.
*   The 9 initial classes (3 per era).
*   Core combat, leveling, and questing mechanics.
*   At least two zones: Seattle and Echo Vale.
*   Basic crafting, gathering, and salvaging.
*   Player-made equipment system.
*   Player-to-player trading.
*   Party system.
*   Basic UI for all core features.
*   File-based persistence for player data.

### 4.2. Out of Scope (Future Development)

*   Level cap increases beyond 20.
*   Hybrid/Support classes (Rogue, Pet User).
*   Advanced combat features (complex skill trees, detailed balancing).
*   PvP Arenas.
*   Guild and Raid systems..
*   Auction House.
*   Advanced NPC AI and boss mechanics.
*   Additional zones (Neo-Babylon, Silicon Desert, etc.).
*   Graphical client (initial client is simple Unreal Engine 5 with 3D assets).
*   Improved database integration (e.g. MySQL / MariaDB).
*   UI Customization and modding support.
*   Monetization features.

## 5. Assumptions

*   The initial client will be simple and functional, focusing on mechanics over graphical fidelity.
*   The initial server will be designed for a small number of concurrent users. Scalability is a future concern.
*   The game mechanics described in the GDD and implemented in `game_mechanics.py` are the source of truth for calculations.

## 6. Success Metrics

*   **Technical Stability:** The server remains online and responsive under a test load of 10-20 concurrent players.
*   **Core Loop Completion:** A player can create a character, level up to 10, fight monsters, complete several quests, and craft a basic item.
*   **Feature Implementation:** All "In Scope" features listed in section 4.1 are implemented and functional.
*   **Community Engagement:** The project attracts interest from at least 3 external contributors post-release.