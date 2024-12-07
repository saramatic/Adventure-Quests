# combat.py

import random


class Combat:
    def __init__(self, player, enemy_name, enemy_health, enemy_strength, reward, gold_reward=10):
        """
        Initialize a combat instance.
        :param player: The player character instance.
        :param enemy_name: Name of the enemy.
        :param enemy_health: Health points of the enemy.
        :param enemy_strength: Attack strength of the enemy.
        :param reward: Reward item for defeating the enemy.
        :param gold_reward: Gold coins rewarded for defeating the enemy.
        """
        self.player = player
        self.enemy_name = enemy_name
        self.enemy_health = enemy_health
        self.enemy_strength = enemy_strength
        self.reward = reward if isinstance(reward, list) else [reward]
        self.gold_reward = gold_reward
        self.player_damage_range = (15, 20)  # Damage range for player attacks
        self.enemy_damage_range = (8, 12)  # Damage range for enemy attacks

    def engage(self):
        """Start combat between the player and the enemy."""
        print(f"A wild {self.enemy_name} appears!")
        print(f"{self.enemy_name} has {self.enemy_health} health and {self.enemy_strength} strength.")
        print(f"If you defeat the {self.enemy_name}, you will earn {self.gold_reward} gold and the following rewards: {', '.join(self.reward)}!")

        turn_count = 0  # To limit combat rounds
        max_turns = 4   # Maximum rounds before auto-resolution

        while self.player.health > 0 and self.enemy_health > 0:
            print(f"\n{self.enemy_name}'s Health: {self.enemy_health}")
            print(f"{self.player.name}'s Health: {self.player.health}")
            action = input("Choose an action: attack (a), defend (d), run (r): ").strip().lower()

            if action in ["a", "attack"]:
                self.player_attack()
            elif action in ["d", "defend"]:
                self.player_defend()
            elif action in ["r", "run"]:
                if self.run():
                    return  # Escape the combat
            else:
                print("Invalid action. Please choose attack (a), defend (d), or run (r).")
                continue

            # Check if the enemy is defeated after player's action
            if self.enemy_health <= 0:
                self.reward_player()
                return

            # Enemy's turn to attack
            self.enemy_attack()

            # Check if the player is defeated after enemy's action
            if self.player.health <= 0:
                print("You were defeated in battle.")
                return

            # Increment turn counter and check for auto-resolution
            turn_count += 1
            if turn_count >= max_turns:
                print("The battle concludes after multiple rounds of fierce fighting!")
                if self.enemy_health > 0:
                    print(f"{self.enemy_name} retreats with remaining health!")
                else:
                    self.reward_player()
                return

    def player_attack(self):
        """Handle player's attack on the enemy."""
        damage = random.randint(*self.player_damage_range)
        self.enemy_health -= damage
        print(f"You attack {self.enemy_name} for {damage} damage!")

    def enemy_attack(self):
        """Handle enemy's attack on the player."""
        damage = random.randint(*self.enemy_damage_range)
        self.player.health -= damage
        print(f"{self.enemy_name} attacks you for {damage} damage!")

    def player_defend(self):
        """Handle player's defense to reduce enemy damage."""
        reduced_damage = max(0, random.randint(*self.enemy_damage_range) - random.randint(5, 10))
        self.player.health -= reduced_damage
        print(f"You defend against {self.enemy_name}'s attack! You take {reduced_damage} damage.")

    def run(self):
        """Attempt to flee from combat."""
        if random.random() < 0.5:  # 50% chance to escape
            print("You successfully escaped!")
            return True
        else:
            damage = random.randint(*self.enemy_damage_range)
            self.player.health -= damage
            print(f"You failed to escape! {self.enemy_name} attacks you for {damage} damage.")
            return False

    def reward_player(self):
        """Reward the player upon victory."""
        print(f"You defeated {self.enemy_name}!")

        # Reward gold
        self.player.gold += self.gold_reward
        print(f"You received {self.gold_reward} gold!")

        # Reward the specified items
        if self.reward:
            for item in self.reward:
                self.player.add_to_inventory(item)
            print(f"You received: {', '.join(self.reward)}!")
