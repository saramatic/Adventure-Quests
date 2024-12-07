# Adventure Quests

Adventure Quests is a Python-based game where players embark on exciting quests filled with challenges, combat, and exploration. Players can interact with characters, battle enemies, collect items, and save their progress as they navigate through an immersive world.

---

## Features

### Core Gameplay
- **Quests:** Players can embark on various quests with unique challenges and rewards.
- **Combat System:** Engage in turn-based battles with NPCs and enemies.
- **Locations:** Explore different areas with unique settings and encounters.

### Characters
- **Customizable Characters:** Players can create and manage their own characters.
- **NPC Interactions:** Meet non-playable characters (NPCs) who provide information, quests, or items.

### Items and Inventory
- **Collect Items:** Discover and use items to aid your journey.
- **Inventory Management:** Track your items, gear, and resources.

### Save and Load
- **Save Progress:** Save your game state to continue your adventure later.
- **Load Saved Games:** Resume from where you left off.

---

## Requirements

- Python 3.8+
- Required dependencies (install with `pip`):
  - None currently specified (update as necessary).

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/saramatic/Adventure-Quests.git
   cd Adventure-Quests
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the game:
   ```bash
   python main.py
   ```

---

## Folder Structure

```plaintext
Adventure-Quests/
├── main.py         # Entry point of the game
├── character.py    # Character-related functionality
├── quests.py       # Quest logic and data
├── combat.py       # Combat system mechanics
├── locations.py    # Game locations and exploration
├── items.py        # Item handling and inventory
├── utils.py        # Helper functions
├── save_load.py    # Save and load game functionality
├── players.txt     # Example player data
├── savegame.json   # Save file (ignored in .gitignore)
└── __pycache__/    # Compiled Python files (ignored in .gitignore)
```

---

## How to Play

1. Launch the game by running `main.py`.
2. Create your character and choose your first quest.
3. Explore locations, interact with NPCs, and collect items.
4. Save your progress anytime and resume later.

---

## Challenges and Feedback
We are actively developing Adventure Quests and would love to hear your thoughts! If you encounter any issues or have suggestions for new features, feel free to [open an issue](https://github.com/saramatic/Adventure-Quests/issues) or leave feedback.

---

## Future Plans
- Enhanced NPC dialogue system
- Additional quests and storylines
- Multiplayer support for collaborative gameplay
- Visual interface for easier navigation

---

## Contributing

We welcome contributions! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Submit a pull request with a detailed description of your changes.

---

## License

Adventure Quests is licensed under the [MIT License](LICENSE).

