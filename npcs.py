# npcs.py
from challenges import initialize_challenges
import random


class NPC:
    def __init__(self, name, location, dialogue, role="neutral", quest=None, inventory=None, required_item=None, riddles=None):
        """
        :param riddles: List of dictionaries containing riddle questions and answers.
        """
        self.name = name
        self.location = location
        self.dialogue = dialogue
        self.role = role  # Roles: quest_giver, trader, mystic, ally, enemy, neutral
        self.quest = quest  # Associated quest, if any
        self.inventory = inventory if inventory else []  # Items for traders
        self.required_item = required_item  # Item needed for the quest
        self.interacted = False  # Tracks if the NPC has been interacted with
        self.challenges = initialize_challenges()  # Challenges for Scholar, Mystic, etc.
        self.current_challenge_index = 0  # Tracks the next challenge
        self.riddles = riddles if riddles else []  # Riddles for variety

    def start(self, character):
        """Start the quest."""
        if self.status == "Not Started":
            self.status = "In Progress"
            character.active_quests.append(self)
        else:
            print(f"Quest '{self.name}' is already {self.status}.")

    
    def interact(self, character):
        """Handle interaction with the NPC."""
        print("=" * 80)
        print(f"You encounter {self.name}.")
        print(f"{self.name}: {self.dialogue}")

        if self.role == "quest_giver":
            self.handle_quest_giver(character)
        elif self.role == "mystic":
            self.offer_challenge(character)
        elif self.role == "trader":
            self.trade_with_player(character)
        elif self.role == "ally":
            print(f"{self.name} offers assistance!")
        elif self.role == "enemy":
            self.handle_enemy(character)
        elif self.required_item:
            self.handle_required_item(character)
        else:
            print(f"{self.name} doesn't seem to have anything specific to offer.")

        # Centralized input prompt
        input("Press Enter to continue...")


    def handle_quest_giver(self, character):
        """Handle quest giver interactions."""
        if self.name == "Elder" and self.quest and self.quest.status == "Not Started":
            print("You meet the Elder:")
            print(f"Elder says: '{self.dialogue}'")
            accept = input(f"Do you want to accept the quest '{self.quest.name}'? (yes/no): ").strip().lower()

            if accept == "yes":
                self.quest.start(character)
                print("The Elder says: 'Thank you. You must travel to the Enchanted Castle and retrieve the Ancient Scroll to protect our village.'")
                print(f"Quest '{self.quest.name}' has been added to your quest log.")
                # Offer a riddle
                self.offer_riddle(character)
            else:
                print("The Elder says: 'Ah, adventurer, perhaps courage isn't your strength today, but I shall await your return.'")

        elif self.name == "Elder" and self.quest and self.quest.status == "In Progress":
            print(f"The Elder says: 'Have you retrieved the {self.quest.required_item}? Drop it here so I may protect the village.'")
            if self.quest.required_item in character.inventory:
                choice = input(f"Do you want to drop the {self.quest.required_item}? (yes/no): ").strip().lower()
                if choice == "yes":
                    character.remove_from_inventory(self.quest.required_item)
                    self.quest.complete(character)
                    print(f"The Elder says: 'You have done well, adventurer! The {self.quest.name} is complete. Our village owes you a great debt.'")
                else:
                    print("The Elder says: 'Return when you are ready to part with the Ancient Scroll.'")
            else:
                print("The Elder says: 'You have not yet retrieved the Ancient Scroll. Please return when you have it.'")

        elif self.name == "Scholar" and self.quest and self.quest.status == "Not Started":
            print("You meet the Scholar:")
            print(f"Scholar says: '{self.dialogue}'")
            accept = input(f"Do you want to accept the quest '{self.quest.name}'? (yes/no): ").strip().lower()

            if accept == "yes":
                self.quest.start(character)
                print("The Scholar says: 'Thank you. Help me locate the three rare items I need to find scattered here.'")
                print(f"Quest '{self.quest.name}' has been added to your quest log.")
                self.present_word_search(character)
                # Offer a riddle
                self.offer_riddle(character)
            else:
                print("The Scholar says: 'Oh well, perhaps you're more interested in easy adventures? I'll be here when you're ready to use your brain!'")

        elif self.name == "Scholar" and self.quest and self.quest.status == "In Progress":
            self.present_word_search(character)

        elif self.name == "Mystic" and self.quest and self.quest.status == "Not Started":
            print("You meet the Mystic:")
            print(f"Mystic says: '{self.dialogue}'")
            accept = input(f"Do you want to attempt the challenge '{self.quest.name}'? (yes/no): ").strip().lower()

            if accept == "yes":
                self.quest.start(character)
                print("The Mystic says: 'Excellent. Here is your challenge:'")
                self.present_cipher(character)
                # Offer a riddle
                self.offer_riddle(character)
            else:
                print("The Mystic says: 'Not ready? Perhaps the stars will align for you another time.'")

        elif self.name == "Mystic" and self.quest and self.quest.status == "In Progress":
            self.present_cipher(character)

        elif self.quest and self.quest.status == "Completed":
            print(f"{self.name} says: 'You have already completed '{self.quest.name}'. Thank you for your help!'")

        # Single prompt to exit interaction
        input("Press Enter to continue...")



    def offer_quest(self, character):
        """Offer a quest to the player."""
        if self.quest.status == "Not Started":
            # Directly start the quest using the Quest's `start` method
            self.quest.start(character)
        else:
            print(f"{self.name} says: 'You are already working on or have completed the quest: {self.quest.name}.'")


    def offer_riddle(self, character):
        """Offer a riddle to the player after accepting a quest."""
        if self.riddles:
            print(f"{self.name} says: 'Before you go, would you like to try a riddle for a bonus reward?'")
            choice = input("Would you like to hear the riddle? (yes/no): ").strip().lower()

            if choice == "yes":
                riddle = random.choice(self.riddles)
                print(f"{self.name} asks: '{riddle['riddle']}'")
                answer = input("Your answer: ").strip().lower()

                if answer == riddle["answer"].lower():
                    print(f"{self.name} says: 'Correct! You are clever indeed.'")
                    character.add_to_inventory("Gold Coin")  # Example reward
                    print("You received a Gold Coin as a reward!")
                else:
                    print(f"{self.name} says: 'That is incorrect. The correct answer was {riddle['answer']}.'")
                    print(f"{self.name} says: 'No worries, adventurer! Perhaps next time!'")
            elif choice == "no":
                print(f"{self.name} says: 'Very well, perhaps another time. Safe travels!'")
            else:
                print(f"{self.name} says: 'I couldn't quite understand that. Let us move on.'")
        else:
            print(f"{self.name} says: 'I have no riddles for you at the moment.'")

    
    def offer_challenge(self, character):
        """Offer a quest or challenge to the player if available."""
        if self.name == "Elder" and self.quest:
            # Handle Elder's quests
            if self.quest.status == "Not Started":
                # Offer the quest if not started
                print(f"{self.name} offers you a quest: {self.quest.name}")
                print(f"Quest '{self.quest.name}' Description: {self.quest.description}")
                accept = input("Do you accept this quest? (yes/no): ").strip().lower()
                if accept == "yes":
                    self.quest.start(character)  # Update the quest to "In Progress"
                    print(f"You have accepted the quest: {self.quest.name}")
                else:
                    print(f"{self.name} says: 'Very well. Let me know if you change your mind.'")
            elif self.quest.status == "In Progress":
                # Handle in-progress quest
                if self.quest.required_item in character.inventory:
                    # Check if the player has the required item
                    print(f"{self.name} says: 'Ah, I see you have the {self.quest.required_item}. May I have it?'")
                    give_item = input(f"Do you want to give the {self.quest.required_item} to {self.name}? (yes/no): ").strip().lower()
                    if give_item == "yes":
                        character.remove_from_inventory(self.quest.required_item)
                        self.quest.complete(character)  # Mark the quest as complete
                        print(f"{self.name} says: 'Thank you for returning the {self.quest.required_item}. The {self.quest.name} is complete!'")
                    else:
                        print(f"{self.name} says: 'Please return when you are ready to hand over the {self.quest.required_item}.'")
                else:
                    # Offer a riddle if the item is not found
                    print(f"{self.name} says: 'The {self.quest.name} is still in progress. Perhaps a riddle to aid your journey?'")
                    self.ask_riddle(character)
            elif self.quest.status == "Completed":
                # Completed quest interaction
                print(f"{self.name} says: 'You have already completed the quest: {self.quest.name}. Thank you for your help!'")
        elif self.name == "Scholar" and self.quest:
            # Handle Scholar's challenges
            if self.quest.status == "Not Started":
                # Offer the challenge
                print(f"{self.name} offers you a challenge: {self.quest.name}")
                print(f"Challenge '{self.quest.name}' Description: {self.quest.description}")
                accept = input("Do you accept this challenge? (yes/no): ").strip().lower()
                if accept == "yes":
                    self.quest.start(character)  # Update the quest to "In Progress"
                    print(f"You have started the challenge: {self.quest.name}")
                    self.present_word_search(character)  # Directly present the word search challenge
                else:
                    print(f"{self.name} says: 'Very well. Let me know if you change your mind.'")
            elif self.quest.status == "In Progress":
                # Handle in-progress challenge
                print(f"{self.name} says: 'You are already working on the challenge: {self.quest.name}.'")
                self.present_word_search(character)  # Retry the word search challenge
            elif self.quest.status == "Completed":
                # Completed challenge interaction
                print(f"{self.name} says: 'You have already completed the challenge: {self.quest.name}. Well done!'")
        elif self.name == "Mystic" and self.quest:
            # Handle Mystic's cipher challenges
            if self.quest.status == "Not Started":
                # Offer the cipher challenge
                print(f"{self.name} offers you a cipher challenge: {self.quest.name}")
                print(f"Cipher '{self.quest.name}' Description: {self.quest.description}")
                accept = input("Do you accept this cipher challenge? (yes/no): ").strip().lower()
                if accept == "yes":
                    self.quest.start(character)  # Update the quest to "In Progress"
                    print(f"You have started the cipher challenge: {self.quest.name}")
                    self.present_cipher(character)  # Directly present the cipher challenge
                else:
                    print(f"{self.name} says: 'Very well. Let me know if you change your mind.'")
            elif self.quest.status == "In Progress":
                # Handle in-progress cipher challenge
                print(f"{self.name} says: 'You are already working on the cipher challenge: {self.quest.name}.'")
                self.present_cipher(character)  # Retry the cipher challenge
            elif self.quest.status == "Completed":
                # Completed cipher interaction
                print(f"{self.name} says: 'You have already completed the cipher challenge: {self.quest.name}. Well done!'")


    def present_word_search(self, character):
        """Present the word search challenge for 'The Scholar's Collection'."""
        print("=" * 80)
        print("The Scholar presents you with a word search challenge:")
        challenge = next((ch for ch in self.challenges if ch.name == "The Scholar's Collection"), None)

        if not challenge:
            print("The Scholar seems to have forgotten the challenge. Please report this issue.")
            return

        print(challenge.description)
        answer = input("Enter the words you found, separated by commas: ").strip().lower()
        user_answers = set(answer.replace(" ", "").split(","))
        correct_answers = set(challenge.solution.replace(" ", "").split(","))

        if user_answers == correct_answers:
            print("The Scholar says: 'You have completed 'The Scholar's Collection' quest. You have earned 40 gold coins and gained the knowledge of the scholar's research in level experience.'")
            challenge.reward_character(character)
            self.quest.complete(character)
        else:
            missing_answers = correct_answers - user_answers
            extra_answers = user_answers - correct_answers

            if missing_answers:
                print(f"You missed the following correct items: {', '.join(missing_answers)}.")
            if extra_answers:
                print(f"You included incorrect items: {', '.join(extra_answers)}.")

            print("The Scholar says: 'Well, that didn't go as planned. But remember, even the greatest minds fail before they succeed!'")


    def trade_with_player(self, character):
        """Trade items with the player."""
        if not self.inventory:
            print(f"{self.name} says: 'I have nothing to sell at the moment. Come back later!'")
            return

        print(f"{self.name} sets up a small stall and says:")
        print(f"'Welcome, adventurer! Feast your eyes on my magnificent wares! Here's what I have for you today:'")
        print("=" * 40)
        for index, item in enumerate(self.inventory, start=1):
            print(f"{index}. {item['name']} - {item['price']} gold")
        print("=" * 40)

        choice = input("Would you like to buy something? (yes/no): ").strip().lower()
        if choice == "yes":
            print(f"{self.name} exclaims: 'Ah, a discerning buyer! Let’s see what catches your fancy.'")
            self.buy_item(character)
        else:
            print(f"{self.name} says: 'Ah, no worries! Perhaps next time, my friend. Safe travels!'")


    def buy_item(self, character):
        """Handle item purchase."""
        try:
            item_choice = int(input("Enter the number of the item to buy: ")) - 1
            if 0 <= item_choice < len(self.inventory):
                item = self.inventory[item_choice]
                if character.gold >= item["price"]:
                    character.gold -= item["price"]
                    character.add_to_inventory(item["name"])
                    print(f"You bought {item['name']} for {item['price']} gold.")
                else:
                    print("You don't have enough gold!")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a valid number.")

    def handle_in_progress_quest(self, character):
        """Handle in-progress quest interactions."""
        if self.required_item and self.required_item in character.inventory:
            print(f"{self.name} says: 'Have you found the {self.required_item}?'")
            choice = input(f"Do you want to give the {self.required_item} to {self.name}? (yes/no): ").strip().lower()
            if choice == "yes":
                character.remove_from_inventory(self.required_item)
                print(f"You gave the {self.required_item} to {self.name}.")
                self.required_item = None
                self.quest.mark_objective_complete(self.required_item)
                if not self.quest.objectives:
                    self.quest.complete(character)
                    print(f"{self.name} says: 'Thank you! The {self.quest.name} is complete.'")
            else:
                print(f"{self.name} says: 'Please return when you have the {self.required_item}.'")
        else:
            print(f"{self.name} says: 'The {self.quest.name} is still in progress.'")
            self.ask_riddle(character)

    def handle_enemy(self, character):
        """Initiate combat with the player."""
        from combat import Combat
        print(f"{self.name} appears hostile!")
        combat = Combat(
            character,
            enemy_name=self.name,
            enemy_health=50,
            enemy_strength=8,
            reward="Gold Coin",
            gold_reward=20,
        )
        combat.engage()

    
    def ask_riddle(self, character):
        """Ask a single riddle to the player."""
        if self.riddles:
            riddle = random.choice(self.riddles)
            print(f"{self.name} asks: '{riddle['riddle']}'")
            accept = input("Would you like to answer the riddle? (yes/no): ").strip().lower()
            if accept == "yes":
                answer = input("Your answer: ").strip().lower()
                if answer == riddle["answer"].lower():
                    print(f"{self.name} says: 'Correct! You are clever indeed.'")
                    character.add_to_inventory("Gold Coin")  # Example reward
                    print("You received a Gold Coin as a reward!")
                else:
                    print(f"{self.name} says: 'That is incorrect. The correct answer was {riddle['answer']}.'")
            elif accept == "no":
                print(f"{self.name} says: 'Very well. Come back when you wish to try again.'")
            else:
                print(f"{self.name} says: 'I couldn't quite understand that. Please try again later.'")
        else:
            print(f"{self.name} says: 'I have no riddles for you at the moment.'")

    def present_cipher(self, character):
        """Present a cipher decoding challenge to the player."""
        challenge = self.challenges[self.current_challenge_index]

        print("=" * 80)
        print(f"The Mystic presents you with a cipher challenge: {challenge.name}")
        print(f"Cipher: {challenge.description}")

        answer = input("Your answer: ").strip().lower()

        if answer == challenge.solution.lower():
            print(f"{self.name} says: 'Excellent! You have decoded the message.'")
            challenge.reward_character(character)
            print(f"You have been rewarded with: {challenge.reward}")
            self.quest.complete(character)
        else:
            print(f"{self.name} says: 'That is incorrect. The correct solution was \"{challenge.solution}\".'")
            print("The Mystic says: 'Even the stars stumble before they shine. Try again when you feel ready!'")

        self.current_challenge_index = (self.current_challenge_index + 1) % len(self.challenges)

    def handle_required_item(self, character):
        """Handle giving the required item to the NPC."""
        if self.required_item in character.inventory:
            print(f"{self.name} needs the {self.required_item}.")
            choice = input(f"Do you want to give the {self.required_item} to {self.name}? (yes/no): ").strip().lower()
            if choice == "yes":
                character.remove_from_inventory(self.required_item)
                print(f"You gave the {self.required_item} to {self.name}.")
                self.required_item = None
                if self.quest:
                    self.quest.mark_objective_complete(self.required_item)
                    if not self.quest.objectives:
                        self.quest.complete(character)
            else:
                print("You decided not to give the item.")
        else:
            print(f"{self.name} says: 'I need the {self.required_item}. Come back when you have it.'")

    def offer_help(self):
        """Offer help for ally NPCs."""
        print(f"{self.name} offers their assistance!")