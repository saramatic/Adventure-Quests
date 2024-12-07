# quests.py

class Quest:
    def __init__(self, name, description, reward, objectives=None, required_count=None, required_item=None):
        """
        :param name: Name of the quest.
        :param description: Quest description.
        :param reward: Reward for completion (gold or item).
        :param objectives: List of objectives (multi-step).
        :param required_count: Number of tasks (e.g., defeats) to complete.
        :param required_item: Specific item needed for completion.
        """
        self.name = name
        self.description = description
        self.reward = reward
        self.objectives = objectives if objectives else []
        self.required_count = required_count
        self.required_item = required_item
        self.current_count = 0  # Progress for numeric quests
        self.status = "Not Started"  # Possible statuses: Not Started, In Progress, Completed

    def start(self, character):
        """Start the quest."""
        if self.status == "Not Started":
            print(f"Quest '{self.name}' Description: {self.description}")
            
            # Determine if the quest is auto-accepted (e.g., for story-driven quests)
            if hasattr(self, "auto_accept") and self.auto_accept:
                self.status = "In Progress"
                character.active_quests.append(self)
                print(f"Quest '{self.name}' started automatically as part of the storyline!")
            else:
                # Prompt for manual acceptance
                accept = input("Do you accept this quest? (yes/no): ").strip().lower()
                if accept == "yes":
                    self.status = "In Progress"
                    character.active_quests.append(self)
                    print(f"Quest '{self.name}' started!")
                    
                    # Special handling for quest-specific actions
                    if self.name == "The Scholar's Collection":
                        print("You have started the Scholar's special collection quest!")
                        print("The scholar will provide you with unique challenges.")
                else:
                    print(f"Quest '{self.name}' declined.")
        else:
            print(f"Quest '{self.name}' is already {self.status}.")


    def update_progress(self):
        """Update numeric progress."""
        if self.status == "In Progress" and self.required_count is not None:
            self.current_count += 1
            print(f"Quest '{self.name}' progress: {self.current_count}/{self.required_count}.")
            if self.current_count >= self.required_count:
                self.complete()

    def mark_objective_complete(self, objective):
        """Complete a specific objective."""
        if self.status == "In Progress" and objective in self.objectives:
            self.objectives.remove(objective)
            print(f"Objective '{objective}' completed!")
            if not self.objectives:  # All objectives completed
                self.complete()

    def handle_challenge_completion(self, challenge_name):
        """Handle a challenge completion if it corresponds to a quest objective."""
        if self.status == "In Progress" and challenge_name in self.objectives:
            print(f"Challenge '{challenge_name}' completed for Quest '{self.name}'!")
            self.mark_objective_complete(challenge_name)

    def complete(self, character=None):
        """Complete the quest."""
        if self.status == "In Progress":
            self.status = "Completed"
            print(f"Quest '{self.name}' completed!")
            if character:
                self.reward_character(character)

    def reward_character(self, character):
        """Reward the player."""
        if isinstance(self.reward, int):  # Gold reward
            character.gold += self.reward
            print(f"You received {self.reward} gold!")
        elif isinstance(self.reward, list):  # Multiple items as reward
            for item in self.reward:
                character.add_to_inventory(item)
                print(f"You received {item}!")
        else:  # Single item reward
            character.add_to_inventory(self.reward)
            print(f"You received {self.reward}!")


    def check_progress(self):
        """Check quest progress."""
        if self.status == "In Progress":
            if self.required_count is not None:
                print(f"Quest '{self.name}' progress: {self.current_count}/{self.required_count}.")
            elif self.objectives:
                print(f"Objectives remaining: {', '.join(self.objectives)}")
        else:
            print(f"Quest '{self.name}' is {self.status}.")

    def reset(self):
        """Reset the quest progress to allow replay."""
        if self.status == "Completed":
            self.status = "Not Started"
            self.current_count = 0
            self.objectives = self.objectives[:]  # Reset objectives if provided
            print(f"Quest '{self.name}' has been reset.")


def initialize_quests():
    """Define quests."""
    return [
        Quest("Retrieve Ancient Scroll", "Find and return the scroll to the wizard.", "Gold Coin", required_item="Ancient Scroll"),
        Quest("Defend the Scholar", "Protect the Scholar by defeating enemies.", "Shield", required_count=3),
        Quest(
            "The Scholar's Collection",
            "Help the scholar collect rare items by completing challenges.",
            40,  # Gold reward
            objectives=["Amulet", "Scroll", "Relic"],  # Linked to the word search challenge
        ),
        Quest("Mystic's Cipher", "Decode the Mystic's encrypted message.", "Magic Scroll", objectives=["Cipher Solved"]),
    ]
