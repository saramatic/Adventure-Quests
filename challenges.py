# challenges.py

class Challenge:
    def __init__(self, name, description, solution, reward):
        self.name = name
        self.description = description
        self.solution = solution
        self.reward = reward
        self.completed = False  # Track if the challenge has been completed

    def present(self, character):
        """Present the challenge to the player."""
        if self.completed:
            print(f"You have already completed the challenge: {self.name}.")
            return True  # Prevent repeating completed challenges

        print("=" * 80)
        print(f"Challenge: {self.name}")
        print(self.description)
        print("Type 'exit' if you'd like to leave and come back later.")
        
        attempts = 3
        while attempts > 0:
            answer = input("Enter your answer: ").strip().lower()
            if answer == "exit":
                print("You chose to leave the challenge. Come back anytime!")
                return False  # Allow the player to leave and revisit later
            elif answer == self.solution.lower():
                print("Correct! Challenge completed.")
                self.reward_character(character)
                self.completed = True  # Mark challenge as completed
                return True
            else:
                attempts -= 1
                print(f"Incorrect! Attempts remaining: {attempts}")

        print("Challenge failed. Better luck next time!")
        return False

    def reward_character(self, character):
        """Give the reward to the player."""
        if isinstance(self.reward, int):
            character.gold += self.reward
            print(f"You received {self.reward} gold!")
        elif isinstance(self.reward, list):  # Multiple rewards
            for item in self.reward:
                character.add_to_inventory(item)
            print(f"You received: {', '.join(self.reward)}!")
        else:
            character.add_to_inventory(self.reward)
            print(f"You received {self.reward}!")

# Define multiple challenges
def initialize_challenges():
    return [
        # Existing challenges
        Challenge("Solve the Riddle", "What has keys but can't open locks?", "keyboard", "Gold Coin"),
        Challenge("Logic Puzzle", "What comes next in the sequence: 2, 4, 8, 16, ?", "32", "Health Potion"),
        Challenge("Memory Test", "Remember the pattern: circle, square, triangle.", "circle, square, triangle", "Magic Scroll"),

        # New word search challenge
        Challenge(
            "The Scholar's Collection",
            """To find the three rare items, locate the words in this word search:
            S C R O L L T Q A
            R M A G I K K I N
            E X E T R A I O R
            L R E L I C P U S
            I E A M U L E T E
            C K T R E A S U R
            Enter all three words, separated by commas.""",
            "amulet, scroll, relic",  # Solution
            40  # Reward in gold
        ),

        # New cipher decoding challenge
        Challenge(
            "The Mystic's Cipher",
            """Decode the following phrase: "Uifsf jt b tfdsfu jtmboe"
            (Hint: Each letter is shifted one step forward in the alphabet.)""",
            "there is a secret island",  # Solution
            "Ancient Map"  # Reward
        ),

        # Additional riddles
        Challenge(
            "Riddle: Morning, Noon, and Night",
            "What walks on four legs in the morning, two legs at noon, and three legs in the evening?",
            "human",
            "Gold Coin"
        ),
        Challenge(
            "Riddle of the Sphinx",
            "The more you take, the more you leave behind. What am I?",
            "footsteps",
            "Health Potion"
        ),
        Challenge(
            "Logic Riddle",
            "What has to be broken before you can use it?",
            "egg",
            "Magic Scroll"
        ),
        Challenge(
            "Classic Puzzle",
            "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?",
            "echo",
            "Gold Coin"
        ),
    ]
