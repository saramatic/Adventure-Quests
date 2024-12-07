# main.py
import os
import random
from character import Character
from locations import GameMap
from save_load import SaveLoad
from quests import initialize_quests
from challenges import initialize_challenges
from npcs import NPC
from combat import Combat
from textwrap import dedent


class Game:
    def __init__(self):
        self.character = None
        self.game_map = GameMap()
        self.save_load = SaveLoad()
        self.quests = initialize_quests()
        self.challenges = initialize_challenges()
        self.running = True
        self.npcs = self.initialize_npcs()

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def initialize_npcs(self):
        """Initialize NPCs with their roles, dialogues, and locations."""
        return [
            NPC(
                "Elder",
                (1, 0),
                "Greetings, adventurer! I have an important task for you.",
                role="quest_giver",
                quest=self.quests[0],
                riddles=[
                    {"riddle": "What walks on four legs in the morning, two legs at noon, and three legs in the evening?", "answer": "human"},
                    {"riddle": "I speak without a mouth and hear without ears. What am I?", "answer": "echo"},
                ],
            ),
            NPC(
                "Scholar",
                (1, 1),
                "Ah, a curious mind! Can you help me solve a fascinating challenge?",
                role="quest_giver",
                quest=self.quests[2],
                riddles=[
                    {"riddle": "The more you take, the more you leave behind. What am I?", "answer": "footsteps"},
                    {"riddle": "I am always in front of you but can never be seen. What am I?", "answer": "future"},
                ],
            ),
            NPC(
                "Mystic",
                (3, 3),
                "Greetings, seeker. Will you unlock the mysteries of the Cipher?",
                role="quest_giver",
                quest=self.quests[3],
                riddles=[
                    {"riddle": "What has to be broken before you can use it?", "answer": "egg"},
                    {"riddle": "I’m light as a feather, yet the strongest person can’t hold me for five minutes. What am I?", "answer": "breath"},
                ],
            ),
            NPC(
                "Wandering Trader",
                (0, 0),
                "Welcome, traveler! Care to trade?",
                role="trader",
                inventory=[
                    {"name": "Health Potion", "price": 10},
                    {"name": "Old Sword", "price": 25},
                    {"name": "Magic Scroll", "price": 40},
                ],
            ),
            NPC(
                "Wandering Trader",
                (2, 2),
                "Hello, adventurer! Care to browse my wares?",
                role="trader",
                inventory=[
                    {"name": "Shield", "price": 50},
                    {"name": "Enchanted Amulet", "price": 100},
                ],
            ),
        ]

    def main_menu(self):
        self.clear_screen()
        print("=" * 80)
        print(" " * 30 + "Adventure Quest")
        print("=" * 80)
        print("Welcome to Adventure Quest!\n")
        print("In this mystical land, you will embark on a thrilling journey to find the Enchanted")
        print("Castle, rescue allies, and rebuild communities. Along the way, you will encounter")
        print("various challenges, meet different characters, and collect valuable resources.")
        print("Good luck on your adventure!\n")
        print("=" * 80)
        print("| Main Menu:                                                                    |")
        print("| 1. Start New Game                                                             |")
        print("| 2. Load Game                                                                  |")
        print("| 3. Quit                                                                       |")
        print("=" * 80)
        return input("Please select an option: ").strip()

    def start_new_game(self):
        self.clear_screen()
        self.running = True
        print("=" * 80)
        print(" " * 30 + "Adventure Quest")
        print("=" * 80)
        print("Create your Character!\n")

        # Prompt for a valid name
        while True:
            name = input("Enter your character's name: ").strip()
            if name:  # Check if the name is not empty
                break
            else:
                print("Sorry, you need to create a name before starting the game.")

        # Proceed with the game setup
        self.character = Character(name)
        print(f"\nCharacter created! Name: {self.character.name}, Health: 100, Strength: 10")
        input("Press Enter to continue...")
        self.game_loop()


    def load_game(self):
        self.clear_screen()
        print("=" * 80)
        print(" " * 30 + "Adventure Quest")
        print("=" * 80)
        print("Load a Saved Game!\n")

        if not os.path.exists(self.save_load.filename) or os.path.getsize(self.save_load.filename) == 0:
            print("No saved games available. Returning to the main menu.")
            input("Press Enter to continue...")
            return

        name = input("Enter your character's name: ").strip()
        loaded_data = self.save_load.load_game(name)
        if loaded_data:
            (
                self.character,
                self.game_map.items_at_location,
                self.quests,
                self.game_map.visited_locations,
                npc_interactions,
            ) = loaded_data

            for npc in self.npcs:
                interaction_data = npc_interactions.get(npc.name)
                if interaction_data:
                    npc.location = interaction_data["location"]
                    npc.interacted = interaction_data["status"] == "interacted"

            print(f"\nGame loaded successfully! Welcome back, {self.character.name}!")
            input("Press Enter to continue...")
            self.running = True
            self.game_loop()
        else:
            print(f"No saved game found for '{name}'. Returning to the main menu.")
            input("Press Enter to continue...")

    def quit_game(self):
        choice = input("Do you want to save your game before quitting? (yes/no): ").strip().lower()
        if choice == "yes":
            self.save_load.save_game(
                self.character,
                self.game_map.items_at_location,
                self.quests,
                self.game_map.visited_locations,
                {}
            )
        print("Thank you for playing Adventure Quest!")
        self.running = False
        self.clear_screen()

    def view_quests(self):
        """Display the list of active quests."""
        self.clear_screen()
        print("=" * 80)
        print(" " * 30 + "Active Quests")
        print("=" * 80)
        if not self.character.active_quests:
            print("You have no active quests.")
        else:
            for quest in self.character.active_quests:
                print(f"Quest Name: {quest.name}")
                print(f"Description: {quest.description}")
                print(f"Status: {quest.status}")
                print("-" * 80)
        input("Press Enter to return to the game...")

    def inspect(self):
        """Inspect the surroundings for items or clues."""
        location_description = self.game_map.get_location_description(self.character.location)
        items = self.game_map.get_items_at_location(self.character.location)
        print("=" * 80)
        print(f"You inspect your surroundings: {location_description}")
        if items:
            print("You find the following items:")
            for item in items:
                print(f"- {item}")
        else:
            print("You don't find anything of interest here.")
        print("=" * 80)
        input("Press Enter to continue...")

    def interact(self):
        """Interact with NPCs or objects at the current location."""
        npc = next((npc for npc in self.npcs if npc.location == self.character.location), None)
        if npc:
            # Directly delegate interaction to the NPC
            npc.interact(self.character)
        else:
            print("There is nothing to interact with here.")
        input("Press Enter to continue...")


    def pick_up_item(self):
        """Pick up an item at the current location."""
        items = self.game_map.get_items_at_location(self.character.location)
        if not items:
            print("There are no items to pick up.")
            return

        print("Items available to pick up:")
        for idx, item in enumerate(items, start=1):
            print(f"{idx}. {item}")
        choice = input("Enter the number of the item to pick up: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(items):
            item = items[int(choice) - 1]
            if item.lower() == "gold coin":
                coin_value = 10
                self.character.gold += coin_value
                print(f"You picked up a Gold Coin worth {coin_value} gold! Total Gold: {self.character.gold}")
            else:
                self.character.add_to_inventory(item)
                print(f"You picked up {item}.")
            self.game_map.remove_item_from_location(self.character.location, item)
        else:
            print("Invalid choice.")
        input("Press Enter to continue...")

    def drop_item(self):
        """Drop an item from the inventory or give it to an NPC."""
        if not self.character.inventory:
            print("You have no items to drop.")
            return

        print("Your inventory:")
        for idx, item in enumerate(self.character.inventory, start=1):
            print(f"{idx}. {item}")

        choice = input("Enter the number of the item to drop: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(self.character.inventory):
            item = self.character.inventory[int(choice) - 1]

            # Check if there's an NPC at the current location
            npc = next((npc for npc in self.npcs if npc.location == self.character.location), None)
            if npc:
                # If NPC has a quest and the item matches the required item
                if npc.quest and npc.quest.required_item == item and npc.quest.status == "In Progress":
                    print(f"You give the {item} to {npc.name}.")
                    self.character.remove_from_inventory(item)
                    npc.quest.complete(self.character)  # Mark quest as complete
                    print(f"{npc.name} says: 'Thank you for the {item}. The quest is now complete!'")
                else:
                    # NPC doesn't need the item or there's no active quest
                    print(f"{npc.name} says: 'I don't need this item right now.'")
            else:
                # Drop the item on the ground if no relevant NPC or quest
                self.character.remove_from_inventory(item)
                self.game_map.add_item_to_location(self.character.location, item)
                print(f"You dropped {item}.")
        else:
            print("Invalid choice.")

        input("Press Enter to continue...")


    def use_item(self):
        """Use an item from the inventory."""
        if not self.character.inventory:
            print("You have no items to use.")
            return

        print("Your inventory:")
        for idx, item in enumerate(self.character.inventory, start=1):
            print(f"{idx}. {item}")
        choice = input("Enter the number of the item to use: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(self.character.inventory):
            item = self.character.inventory[int(choice) - 1]
            self.character.use_item(item)
            print(f"You used {item}.")
        else:
            print("Invalid choice.")
        input("Press Enter to continue...")

    def random_encounter(self):
        """Randomly trigger an encounter with an enemy or find treasure."""
        if random.random() < 0.5:
            enemies = [
                ("Goblin", 30, 5, ["Gold Coin", "Health Potion"]),
                ("Feral Beast", 50, 8, ["Gold Coin", "Health Potion"]),
            ]
            enemy = random.choice(enemies)
            print(f"A wild {enemy[0]} appears!")
            print(f"{enemy[0]} has {enemy[1]} health and {enemy[2]} strength.")
            combat = Combat(
                self.character,
                enemy_name=enemy[0],
                enemy_health=enemy[1],
                enemy_strength=enemy[2],
                reward=enemy[3],
            )
            if combat.engage():
                for item in enemy[3]:
                    if item.lower() == "gold coin":
                        self.character.gold += 10
                    else:
                        self.character.add_to_inventory(item)
                print(f"You defeated the {enemy[0]} and earned {', '.join(enemy[3])}!")
            else:
                print("You were defeated. Better luck next time!")
        else:
            print("The area is quiet. No enemies nearby.")

    def game_loop(self):
        while self.running:
            self.clear_screen()
            print("=" * 80)
            print(f"Location: {self.game_map.get_location_description(self.character.location)} ({self.character.location})")
            print("=" * 80)
            print(f"| Name: {self.character.name:<15} Health: {self.character.health:<5} Strength: {self.character.strength:<5} |")
            print(f"| Level: {self.character.level:<5} Gold: {self.character.gold:<5} Magic: {self.character.magic:<5} |")
            print("=" * 80)
            print("| Available Commands:                                                           |")
            print("| - Move: north (n), south (s), east (e), west (w)                              |")
            print("| - Actions: inspect (c), interact (t)                                          |")
            print("| - Item Actions: pick up (p), drop (d), use (u)                                |")
            print("| - View Inventory (i)                                                          |")
            print("| - View Map (m)                                                                |")
            print("| - View Quests (qv)                                                            |")
            print("| - Quit (q)                                                                    |")
            print("=" * 80)
            command = input("Enter your command: ").strip().lower()

            if command in ["n", "s", "e", "w"]:
                self.random_encounter()
                self.game_map.move(command, self.character)
            elif command == "c":
                self.inspect()
            elif command == "t":
                self.interact()
            elif command == "qv":
                self.view_quests()
            elif command == "p":
                self.pick_up_item()
            elif command == "d":
                self.drop_item()
            elif command == "u":
                self.use_item()
            elif command == "i":
                self.character.view_inventory()
                input("Press Enter to continue...")
            elif command == "m":
                self.game_map.display_map(self.character)
            elif command == "q":
                self.quit_game()
            else:
                print("Invalid command.")
                input("Press Enter to continue...")


if __name__ == "__main__":
    game = Game()
    try:
        while True:
            choice = game.main_menu()
            if choice == "1":
                game.start_new_game()
            elif choice == "2":
                game.load_game()
            elif choice == "3":
                print("Goodbye, until we meet again!")
                break
            else:
                print("Invalid selection. Please try again.")
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Goodbye!")

