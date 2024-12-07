# character.py

class Character:
    def __init__(self, name, health=100, strength=10, magic=0, gold=0, level=1, inventory=None, location=(0, 0)):
        self.name = name
        self.health = health
        self.strength = strength
        self.magic = magic
        self.gold = gold
        self.level = level
        self.inventory = inventory if inventory else []
        self.location = location
        self.active_quests = []  # Track active quests
        self.temporary_effects = {}  # Track temporary boosts (e.g., strength boost)

    def view_inventory(self):
        """Display the player's inventory and gold."""
        print("=" * 80)
        print(" " * 30 + "Inventory")
        print("=" * 80)
        if not self.inventory:
            print("- No items in inventory.")
        else:
            for item in self.inventory:
                print(f"- {item}")
        print(f"Gold: {self.gold}")
        print("=" * 80)

    def add_to_inventory(self, item):
        """Add an item to the player's inventory."""
        if item.lower() == "gold coin":
            coin_value = 10  # Each Gold Coin adds 10 gold
            self.gold += coin_value
            print(f"You picked up a Gold Coin worth {coin_value} gold! Total Gold: {self.gold}")
        else:
            self.inventory.append(item)
            print(f"{item} added to inventory.")

    def add_multiple_rewards(self, rewards):
        """Add multiple rewards (e.g., items, gold) to the player."""
        for reward in rewards:
            if reward.lower() == "gold coin":
                self.add_to_inventory("gold coin")
            else:
                self.add_to_inventory(reward)

    def remove_from_inventory(self, item):
        """Remove an item from the player's inventory."""
        if item in self.inventory:
            self.inventory.remove(item)
            print(f"{item} removed from inventory.")
        else:
            print(f"{item} is not in your inventory.")

    def update_status(self, health_change=0, strength_change=0, magic_change=0):
        """Update the player's health, strength, and magic."""
        self.health = max(0, self.health + health_change)  # Prevent health from going below 0
        self.strength = max(0, self.strength + strength_change)  # Prevent strength from going below 0
        self.magic = max(0, self.magic + magic_change)  # Prevent magic from going below 0
        print(f"{self.name}'s status updated: Health = {self.health}, Strength = {self.strength}, Magic = {self.magic}")

    def use_item(self, item):
        """Use an item from the inventory and apply its effects."""
        if item in self.inventory:
            print(f"Using {item}...")
            if item.lower() == "health potion":
                self.update_status(health_change=20)
                print(f"Health Potion used. {self.name}'s health increased by 20.")
            elif item.lower() == "strength potion":
                self.update_status(strength_change=10)
                print(f"Strength Potion used. {self.name}'s strength increased by 10.")
            elif item.lower() == "magic scroll":
                self.update_status(magic_change=15)
                print(f"Magic Scroll used. {self.name}'s magic increased by 15.")
            elif item.lower() == "old sword":
                self.update_status(strength_change=5)
                self.temporary_effects["strength_boost"] = 5
                print(f"You equipped the Old Sword. Your strength increased by 5!")
            else:
                print(f"{item} has no special effect.")
            self.remove_from_inventory(item)
        else:
            print(f"You don't have {item} in your inventory.")

    def move(self, direction, boundaries=(5, 5)):
        """Move the player in a specified direction."""
        x, y = self.location
        if direction == "n":
            y -= 1
        elif direction == "s":
            y += 1
        elif direction == "e":
            x += 1
        elif direction == "w":
            x -= 1
        else:
            print("Invalid direction.")
            return

        # Check for boundaries
        if 0 <= x < boundaries[0] and 0 <= y < boundaries[1]:
            self.location = (x, y)
            print(f"{self.name} moved to {self.location}.")
        else:
            print("You can't move in that direction. It's out of bounds.")

    def add_active_quest(self, quest):
        """Add a quest to the active quests."""
        self.active_quests.append(quest)
        print(f"Quest '{quest.name}' added to your active quests.")

    def remove_active_quest(self, quest_name):
        """Remove a quest from the active quests."""
        quest_to_remove = next((q for q in self.active_quests if q.name == quest_name), None)
        if quest_to_remove:
            self.active_quests.remove(quest_to_remove)
            print(f"Quest '{quest_name}' removed from active quests.")
        else:
            print(f"Quest '{quest_name}' not found in active quests.")

    def check_temporary_effects(self):
        """Check and apply temporary effects."""
        for effect, value in self.temporary_effects.items():
            if effect == "strength_boost":
                print(f"You feel the lingering effect of the Old Sword. Strength: {self.strength} (+{value})")

    def reward_after_combat(self, rewards):
        """Give combat rewards like gold and health potions."""
        print("You are victorious in combat!")
        self.add_multiple_rewards(rewards)
        print(f"Total Gold: {self.gold}, Inventory: {', '.join(self.inventory)}")
