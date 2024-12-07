# locations.py
import random
from npcs import NPC  # Assuming the NPC class is in the npcs.py file


class GameMap:
    def __init__(self):
        """Initialize the game map."""
        self.game_map = {
            (0, 0): "Starting Point",
            (0, 1): "Uncharted Territory",
            (0, 2): "Magical Spring",
            (0, 3): "Ancient Ruins",
            (0, 4): "Haunted Forest",
            (1, 0): "Abandoned Village",
            (1, 1): "Uncharted Territory",
            (1, 2): "Mystical City",
            (1, 3): "Ancient Ruins",
            (1, 4): "Magical Spring",
            (2, 0): "Haunted Forest",
            (2, 1): "Mystical City",
            (2, 2): "Uncharted Territory",
            (2, 3): "Abandoned Village",
            (2, 4): "Uncharted Territory",
            (3, 0): "Mystical City",
            (3, 1): "Haunted Forest",
            (3, 2): "Abandoned Village",
            (3, 3): "Uncharted Territory",
            (3, 4): "Ancient Ruins",
            (4, 0): "Magical Spring",
            (4, 1): "Mystical City",
            (4, 2): "Haunted Forest",
            (4, 3): "Abandoned Village",
            (4, 4): "Enchanted Castle",  # Final goal
        }

        # Items available at specific locations
        self.items_at_location = {
            (0, 1): ["Old Sword", "Health Potion"],
            (1, 0): ["Gold Coin"],
            (1, 3): ["Magic Scroll"],
            (2, 2): ["Enchanted Amulet"],
            (2, 3): ["Shield"],
            (4, 4): ["Ancient Relic"],
        }

        # NPCs at specific locations
        self.npcs_at_location = {
            (0, 0): {"name": "Wandering Merchant", "dialogue": "Care to trade?", "role": "trader"},
            (1, 0): {"name": "Village Elder", "dialogue": "I have a quest for you.", "role": "quest_giver"},
            (3, 3): {"name": "Mystic", "dialogue": "Will you unlock the mysteries of the Cipher?", "role": "quest_giver"},
            (4, 4): {"name": "Castle Guardian", "dialogue": "Welcome, hero!", "role": "ally"},
        }

        self.visited_locations = set()
        self.ensure_ancient_scroll_placement()  # Ensure dynamic placement of Ancient Scroll

    def ensure_ancient_scroll_placement(self):
        """Ensure the Ancient Scroll exists in the game, dynamically placing it if needed."""
        scroll_already_exists = any(
            "Ancient Scroll" in items for items in self.items_at_location.values()
        )
        if not scroll_already_exists:
            available_locations = [
                loc for loc in self.game_map.keys() if loc not in self.items_at_location and loc != (0, 0)
            ]
            if available_locations:
                random_location = random.choice(available_locations)
                self.items_at_location[random_location] = ["Ancient Scroll"]

    def get_location_description(self, location):
        """Get the description of a given location."""
        return self.game_map.get(location, "Uncharted Territory")

    def move(self, direction, character):
        """Move the player to a new location based on direction."""
        x, y = character.location
        if direction == "n":
            new_location = (x, y - 1)
        elif direction == "s":
            new_location = (x, y + 1)
        elif direction == "e":
            new_location = (x + 1, y)
        elif direction == "w":
            new_location = (x - 1, y)
        else:
            print("Invalid direction.")
            return

        if new_location in self.game_map:
            character.location = new_location
            self.visited_locations.add(new_location)
            print(f"You moved to {self.get_location_description(character.location)} ({character.location}).")
        else:
            print("You can't move in that direction! There's nothing beyond.")

        input("Press Enter to continue...")

    def display_map(self, character):
        """Display the game map with the player's current position."""
        while True:
            print("=" * 80)
            print(" " * 30 + "Game Map")
            print("=" * 80)
            for y in range(5):
                row = ""
                for x in range(5):
                    if (x, y) == character.location:
                        row += " P "  # Player's position
                    elif (x, y) in self.visited_locations:
                        row += " X "  # Visited location
                    else:
                        row += " . "  # Uncharted territory
                print(row)
            print("=" * 80)
            choice = input("Press 'q' to return to the menu: ").strip().lower()
            if choice == "q":
                break
            else:
                print("Invalid input. Press 'q' to exit the map.")

    def get_items_at_location(self, location):
        """Get the list of items available at a location."""
        return self.items_at_location.get(location, [])

    def add_item_to_location(self, location, item):
        """Add an item to a location."""
        if location not in self.items_at_location:
            self.items_at_location[location] = []
        self.items_at_location[location].append(item)

    def remove_item_from_location(self, location, item):
        """Remove an item from a location."""
        if location in self.items_at_location and item in self.items_at_location[location]:
            self.items_at_location[location].remove(item)
            if not self.items_at_location[location]:
                del self.items_at_location[location]

    def get_npc_at_location(self, location):
        """Retrieve the NPC at the given location."""
        npc_data = self.npcs_at_location.get(location)
        if npc_data:
            return NPC(
                name=npc_data["name"],
                location=location,
                dialogue=npc_data["dialogue"],
                role=npc_data["role"],
            )
        return None

    def trigger_random_event(self, character):
        """Trigger a random event at the player's current location."""
        event_type = random.choice(["none", "enemy", "treasure"])
        if event_type == "enemy":
            print("An enemy appears! Prepare for battle!")
            enemies = [("Goblin", 30, 5, "Gold Coin"), ("Feral Beast", 50, 8, "Health Potion")]
            enemy = random.choice(enemies)
            combat = Combat(character, enemy[0], enemy[1], enemy[2], [enemy[3], "Gold Coin"])
            combat.engage()
        elif event_type == "treasure":
            treasure = random.choice(["Gold Coin", "Health Potion"])
            character.add_to_inventory(treasure)
            print(f"You found a {treasure}!")
