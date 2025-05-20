# "Chrono Clash" (Working Title)

This project is a foundational example of an MMORPG server and a simple text-based (rogue-like) client, both written in Rust. It demonstrates core concepts like basic networking, player movement on a large grid, and a character attribute system.

The current lore concept involves three time periods (Past, Present, Future) colliding, allowing for diverse character origins and playstyles.

## Project Goals

*   To explore building an MMORPG backend in Rust.
*   To implement a flexible character attribute system.
*   To create a very simple, accessible text-based client for testing and basic gameplay.
*   To serve as a learning resource and a potential starting point for a more complex open-source MMO.

## Current Features

*   **Rust Server:**
    *   Asynchronous TCP server using Tokio.
    *   Manages player connections and basic state (ID, position).
    *   Simple 10,000 x 10,000 unit map (conceptual, not fully rendered server-side).
    *   **Character Attribute System:**
        *   Primary Attributes (Agility, Constitution, Strength, Intelligence, Spirit, Wisdom).
        *   Time-period based "cultural adjustments" to starting attributes.
        *   Player-allocated attribute points at creation and level-up.
        *   Calculated Secondary Attributes (Power, Endurance, Speed, Mana, Willpower, Dexterity).
        *   Calculated Tertiary Attributes (HP, Armor, Dodge, Energy, AttackPower, Accuracy) influenced by class, level, and secondary attributes.
        *   Framework for spell/buff modifiers (affecting secondary) and equipment modifiers (affecting tertiary).
    *   Basic command handling for player movement (`MOVE UP/DOWN/LEFT/RIGHT`).
    *   Basic command handling for attribute allocation (`ALLOCATE Strength 1 ...`).
    *   Sends a limited "view" of the map to the client centered on the player.
*   **Rust Client:**
    *   Simple text-based client using `crossterm` for TUI.
    *   Connects to the server and receives a player ID and initial position.
    *   Renders the map view received from the server (`.` for empty, `@` for self, `?` for others).
    *   Allows player movement using arrow keys.
    *   Displays basic status information (ID, position, server messages).

## Technology Stack

*   **Language:** Rust (latest stable)
*   **Server:**
    *   `tokio` for asynchronous networking and runtime.
    *   `fxhash` for potentially faster HashMap operations.
    *   `lazy_static` for global static data.
*   **Client:**
    *   `tokio` for asynchronous networking.
    *   `crossterm` for terminal manipulation (TUI).

## Getting Started

### Prerequisites

*   Rust toolchain (install from [rustup.rs](https://rustup.rs/))

### Building

1.  Clone the repository:
    ```bash
    git clone <your-repo-url>
    cd <your-repo-name>
    ```
2.  Build the server:
    ```bash
    cd simple_mmo_server
    cargo build
    cd ..
    ```
3.  Build the client:
    ```bash
    cd simple_mmo_client
    cargo build
    cd ..
    ```

### Running

1.  **Start the Server:**
    Open a terminal and navigate to the project's root directory.
    ```bash
    ./simple_mmo_server/target/debug/simple_mmo_server
    ```
    The server will start listening on `127.0.0.1:8080`.

2.  **Start the Client(s):**
    Open one or more new terminal windows and navigate to the project's root directory.
    ```bash
    ./simple_mmo_client/target/debug/simple_mmo_client
    ```
    *   Use **arrow keys** to move.
    *   Press **'q'** or **'Esc'** to quit the client.

## Future Development Ideas

*   **Persistence:** Database integration (e.g., PostgreSQL, SQLite) to save player data.
*   **Advanced Combat:** Implement skills, spells, damage calculations based on attributes.
*   **NPCs and Monsters:** Add non-player characters with AI.
*   **Terrain and World Details:** Define actual map terrain, interactable objects.
*   **Inventory and Items:** System for players to collect and use items.
*   **Quests:** Implement a questing system.
*   **Chat System:** Allow players to communicate.
*   **Improved Networking:** More robust serialization (e.g., Serde with Bincode/JSON), error handling, and security.
*   **Spatial Partitioning:** Optimize updates for large numbers of players (e.g., quadtrees).
*   **Graphical Client:** Eventually, a more visually appealing client (e.g., using Bevy, Fyrox, or a web client).
*   **Server Scalability:** Explore strategies for handling more concurrent users.

## Contributing

This project is open source and contributions are welcome! Please feel free to:

*   Report bugs or issues.
*   Suggest new features.
*   Submit pull requests for improvements or new functionality.

When contributing, please try to follow the existing code style and provide clear commit messages.

## License

This project is licensed under the [MIT License](LICENSE.md) (or choose another like Apache 2.0, specify here).
