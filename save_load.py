# save_load.py

import json
import os
from character import Character
from quests import Quest


class SaveLoad:
    def __init__(self, filename="savegame.json"):
        self.filename = filename

    def save_game(self, character, items_at_location, quests, visited_locations, npc_interactions):
        """Save the current game state to a file."""
        try:
            # Prepare the data to be saved
            save_data = {
                "character": {
                    "name": character.name,
                    "health": character.health,
                    "strength": character.strength,
                    "magic": character.magic,
                    "gold": character.gold,
                    "level": character.level,
                    "inventory": character.inventory,
                    "location": character.location,
                    "active_quests": [quest.name for quest in character.active_quests],
                },
                "items_at_location": {
                    str(loc): items for loc, items in items_at_location.items()
                },
                "quests": [
                    {
                        "name": quest.name,
                        "description": quest.description,
                        "reward": quest.reward,
                        "objectives": quest.objectives,
                        "status": quest.status,
                    }
                    for quest in quests
                ],
                "visited_locations": [list(loc) for loc in visited_locations],
                "npc_interactions": npc_interactions,
            }

            # Write the data to a JSON file
            with open(self.filename, "w") as file:
                json.dump(save_data, file, indent=4)
            print("Game saved successfully!")
        except Exception as e:
            print(f"Error saving game: {e}")

    def load_game(self, player_name):
        """Load a saved game state from a file."""
        try:
            if not os.path.exists(self.filename):
                print("Save file not found.")
                return None

            with open(self.filename, "r") as file:
                save_data = json.load(file)

            character_data = save_data["character"]
            if character_data["name"] != player_name:
                print(f"No data found for {player_name}.")
                return None

            # Reconstruct the Character object
            character = Character(
                name=character_data["name"],
                health=character_data["health"],
                strength=character_data["strength"],
                magic=character_data["magic"],
                gold=character_data["gold"],
                level=character_data["level"],
                inventory=character_data["inventory"],
                location=tuple(character_data["location"]),
            )

            # Reconstruct the active quests
            all_quests = save_data["quests"]
            character.active_quests = [
                Quest(
                    name=q["name"],
                    description=q["description"],
                    reward=q["reward"],
                    objectives=q["objectives"],
                    status=q["status"]
                )
                for q in all_quests
                if q["name"] in character_data["active_quests"]
            ]

            # Reconstruct items at locations
            items_at_location = {
                eval(loc): items for loc, items in save_data["items_at_location"].items()
            }

            # Reconstruct visited locations
            visited_locations = set(tuple(loc) for loc in save_data["visited_locations"])

            # Reconstruct NPC interactions
            npc_interactions = save_data["npc_interactions"]

            print(f"\nGame loaded successfully! Welcome back, {character.name}!")
            return character, items_at_location, all_quests, visited_locations, npc_interactions
        except Exception as e:
            print(f"Error loading game: {e}")
            return None
