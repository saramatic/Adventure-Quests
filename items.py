# items.py
class Item:
    def __init__(self, name, effect=None):
        self.name = name
        self.effect = effect  # Effects like "heal", "boost", "unlock"

    def use(self, character):
        """Apply the item's effect to the character."""
        if self.effect == "heal":
            character.health = min(100, character.health + 20)
            print(f"{self.name} used! {character.name}'s health increased by 20.")
        elif self.effect == "boost":
            character.strength += 10
            print(f"{self.name} used! {character.name}'s strength increased by 10.")
        else:
            print(f"{self.name} has no special effect.")

    @staticmethod
    def pick_up(character, item_name, location_items):
        """Pick up an item from the location and add it to the character's inventory."""
        if item_name in location_items:
            character.add_to_inventory(item_name)
            location_items.remove(item_name)
            print(f"{item_name} added to inventory.")
        else:
            print(f"{item_name} is not available here.")

    @staticmethod
    def drop(character, item_name, location_items):
        """Drop an item from the character's inventory at the current location."""
        if item_name in character.inventory:
            character.remove_from_inventory(item_name)
            location_items.append(item_name)
            print(f"{item_name} dropped at the location.")
        else:
            print(f"{item_name} is not in your inventory.")
