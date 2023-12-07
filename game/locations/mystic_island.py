# mystic_island.py in locations/ folder

from game import location
import game.config as config
from game.display import announce
from game.events import *
import game.items as items


class MysticIsland(location.Location):
    def __init__(self, x, y, w):
        super().__init__(x, y, w)
        self.name = "Mystic Island"
        self.symbol = "M"
        self.visitable = True
        self.starting_location = MysticBeach(self)
        self.locations = {
            "beach": self.starting_location,
            "forest": MysticForest(self),
            "cave": MysticCave(self),
            "cliff": MysticCliff(self),
            "lagoon": MysticLagoon(self),
        }

    def enter(self, ship):
        announce("You've arrived at the mysterious Mystic Island.")

    def visit(self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()
        while config.the_player.visiting:
            self.start_turn ()
            self.process_turn ()
            self.end_turn ()
         # Reset to default after visit
        config.the_player.location = config.the_player.ship
        config.the_player.next_loc = None


class MysticBeach(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "beach"  # Change "forest" to "beach"
        self.verbs["beach"] = self
        self.verbs["forest"] = self
        self.verbs["cave"] = self
        self.verbs["cliff"] = self
        self.verbs["lagoon"] = self
        self.verbs["leave"] = self

        self.treasure_collected = False
        self.treasure = items.TreasureItem("Mystic Ruby", 100)

    def enter(self):
        announce(
            " Choose a location to visit: \nMystic Beach \nMystic Forest  \nMystic Cave  \nMystic Cliff \nMystic Lagoon \nLeave Mystic Island\n"
        )
        if not self.treasure_collected:
            announce(
                "You step onto the sandy shores of the Mystic Beach, noticing something glinting in the sand."
            )
            config.the_player.collect_treasure(self.treasure)
            self.treasure_collected = True
        else:
            announce("You walk along the familiar sandy shores of the Mystic Beach.")

        announce(
            "You are on the Mystic Beach. Choose a location to explore: \nBeach  \nForest  \nCave  \nCliff  \nLagoon\n"
        )

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "beach":
            config.the_player.next_loc = self.main_location.locations["beach"]
        if verb == "forest":
            config.the_player.next_loc = self.main_location.locations["forest"]
        if verb == "cave":
            config.the_player.next_loc = self.main_location.locations["cave"]
        if verb == "cliff":
            config.the_player.next_loc = self.main_location.locations["cliff"]
        if verb == "lagoon":
            config.the_player.next_loc = self.main_location.locations["lagoon"]
        if verb == "leave":
            announce("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False


class MysticForest(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "forest"
        self.verbs["beach"] = self
        self.verbs["forest"] = self
        self.verbs["cave"] = self
        self.verbs["cliff"] = self
        self.verbs["lagoon"] = self
        self.verbs["leave"] = self
        self.event_chance = 25
        self.events.append (seagull.Seagull())
        self.events.append(drowned_pirates.DrownedPirates())

        self.riddle_solved = False
        self.treasures = [
            items.TreasureItem("Mystic Ruby", 100),
            items.TreasureItem("Mystic Sapphire", 100),
            items.TreasureItem("Mystic Topaz", 100),
        ]
        self.treasures_collected = False

    def enter(self):
        if not self.treasures_collected and not self.riddle_solved:
            announce(
                "You venture into the dense, mysterious forest, sensing hidden treasures and a wise old parrot awaiting with a challenge."
            )
            self.collect_treasures()
            self.treasures_collected = True
            self.start_encounter()
        elif not self.riddle_solved:
            announce(
                "The dense forest seems less mysterious now, but the wise old parrot still awaits with its unsolved riddle."
            )
            self.start_encounter()
        else:
            announce(
                "The forest is peaceful, and the wise old parrot nods in respect, its riddle now a memory."
            )

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "beach":
            config.the_player.next_loc = self.main_location.locations["beach"]
        if verb == "forest":
            config.the_player.next_loc = self.main_location.locations["forest"]
        if verb == "cave":
            config.the_player.next_loc = self.main_location.locations["cave"]
        if verb == "cliff":
            config.the_player.next_loc = self.main_location.locations["cliff"]
        if verb == "lagoon":
            config.the_player.next_loc = self.main_location.locations["lagoon"]
        if verb == "leave":
            announce("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        

    def collect_treasures(self):
        for treasure in self.treasures:
            announce(f"You found a {treasure.name} worth {treasure.value} points!")
            config.the_player.collect_treasure(treasure)
        announce("You have collected all the scattered treasures in the forest!")

    def start_encounter(self):
        announce(
            "The parrot squawks: 'Solve my riddle to pass: Forward I am heavy, but backward I am not. What am I?'"
        )
        self.solve_riddle()

    def solve_riddle(self):
        player_answer = input("Your answer: ").strip().lower()
        if player_answer == "ton":
            announce("Correct! The parrot squawks in approval and allows you to pass.")
            self.riddle_solved = True
            # Add a friendly squirrel that offers to guide you deeper into the forest
            announce(
                "A friendly squirrel named Nutty offers to guide you deeper into the forest. The squirrel gives you a map for water7 your big next adventure."
            )
        else:
            announce("Incorrect! The parrot squawks loudly. Try again.")
            self.start_encounter()


class MysticCave(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "cave"
        self.verbs["beach"] = self
        self.verbs["forest"] = self
        self.verbs["cave"] = self
        self.verbs["cliff"] = self
        self.verbs["lagoon"] = self
        self.verbs["leave"] = self

        self.special_item = items.MysticSword()
        self.item_collected = False
        self.puzzle_solved = False

    def enter(self):
        if not self.item_collected and not self.puzzle_solved:
            announce(
                "You enter a dark cave, sensing the presence of a hidden item and mysterious figures with a puzzle to solve."
            )
            config.the_player.collect_treasure(self.special_item)
            self.item_collected = True
            self.start_puzzle()
        elif not self.puzzle_solved:
            announce(
                "The cave, now less intimidating with the special item in your possession, still holds the unsolved puzzle."
            )
            self.start_puzzle()
        else:
            announce(
                "The cave is quiet now, the figures and their puzzle just echoes in the dark."
            )

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "beach":
            config.the_player.next_loc = self.main_location.locations["beach"]
        if verb == "forest":
            config.the_player.next_loc = self.main_location.locations["forest"]
        if verb == "cave":
            config.the_player.next_loc = self.main_location.locations["cave"]
        if verb == "cliff":
            config.the_player.next_loc = self.main_location.locations["cliff"]
        if verb == "lagoon":
            config.the_player.next_loc = self.main_location.locations["lagoon"]
        if verb == "leave":
            announce("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
    def start_puzzle(self):
        announce("A says, 'B is a Knave.'")
        announce("B says, 'We are both Knaves.'")
        self.solve_puzzle()

    def solve_puzzle(self):
        max_guess = 3
        while max_guess != 0:
            announce(f"You have {max_guess} chance to solve it")
            player_answer = input("Who is the Knight? (A/B): ").strip().lower()
            if player_answer == "a":
                announce("Correct! A is the Knight, and B is the Knave.")
                self.puzzle_solved = True
                max_guess = 0
                # Add a mysterious figure that reveals a hidden passage deeper into the cave
                announce(
                    "A mysterious figure appears and reveals a hidden passage deeper into the cave."
                )
                announce("You go inside there and find a trasure and leave the cave.")
            elif player_answer == "b":
                announce("That's not right. Think carefully and try again.")
                max_guess -= 1
                announce(f"{max_guess} chances left. Do you think you can do it !!!!!!")
                if max_guess == 0:
                    announce("YOUU LOSTTTT !!! LEAVE THE ISLAND!!!!")

                # self.start_puzzle()


class MysticCliff(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "cliff"
        self.verbs["beach"] = self
        self.verbs["forest"] = self
        self.verbs["cave"] = self
        self.verbs["cliff"] = self
        self.verbs["lagoon"] = self
        self.verbs["leave"] = self

        self.event_chance = 20
        self.treasure = items.TreasureItem("Ancient Coin", 200)
        self.treasure_collected = False
        self.events.append (seagull.Seagull())
        self.events.append(drowned_pirates.DrownedPirates())

    def enter(self):
        if not self.treasure_collected:
            announce(
                "You stand at the edge of a high cliff, a glint from the ground catching your eye."
            )
            config.the_player.collect_treasure(self.treasure)
            self.treasure_collected = True
            # Add an event where you can try paragliding from the cliff
            announce(
                "You notice a paragliding kit nearby. Would you like to try paragliding from the cliff? (yes/no)"
            )
            choice = input().strip().lower()
            if choice == "yes":
                announce(
                    "You take the leap and experience an exhilarating paragliding adventure!"
                )
            elif choice == "no":
                announce(
                    "You decide to enjoy the breathtaking view from the cliff's edge."
                )
        else:
            announce(
                "The cliff offers a breathtaking view of the sea, the mystery of the hidden treasure now solved."
            )

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "beach":
            config.the_player.next_loc = self.main_location.locations["beach"]
        if verb == "forest":
            config.the_player.next_loc = self.main_location.locations["forest"]
        if verb == "cave":
            config.the_player.next_loc = self.main_location.locations["cave"]
        if verb == "cliff":
            config.the_player.next_loc = self.main_location.locations["cliff"]
        if verb == "lagoon":
            config.the_player.next_loc = self.main_location.locations["lagoon"]
        if verb == "leave":
            announce("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        


class MysticLagoon(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "lagoon"
        self.verbs["beach"] = self
        self.verbs["forest"] = self
        self.verbs["cave"] = self
        self.verbs["cliff"] = self
        self.verbs["lagoon"] = self
        self.verbs["leave"] = self

        self.event_chance = 35
        self.treasure = items.TreasureItem("Pearl Necklace", 350)
        self.treasure_collected = False

    def enter(self):
        if not self.treasure_collected:
            announce(
                "You discover a hidden lagoon, its serene beauty hiding something valuable."
            )
            config.the_player.collect_treasure(self.treasure)
            self.treasure_collected = True
            # Add an event where you can go swimming in the lagoon
            announce("Would you like to go swimming in the lagoon? (yes/no)")
            choice = input().strip().lower()
            if choice == "yes":
                announce(
                    "You take a refreshing swim in the crystal-clear waters of the lagoon. You think about the places you explored in this island and the riddles you solved and treasures you collected"
                
                )
            elif choice == "no":
                announce(
                    "You decide to stay by the lagoon's edge and enjoy the tranquility. At last you realize that the inner peace is the biggest treasure."
                )
        else:
            announce(
                "The lagoon, now familiar, still whispers secrets of its hidden depths."
            )

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "beach":
            config.the_player.next_loc = self.main_location.locations["beach"]
        if verb == "forest":
            config.the_player.next_loc = self.main_location.locations["forest"]
        if verb == "cave":
            config.the_player.next_loc = self.main_location.locations["cave"]
        if verb == "cliff":
            config.the_player.next_loc = self.main_location.locations["cliff"]
        if verb == "lagoon":
            config.the_player.next_loc = self.main_location.locations["lagoon"]
        if verb == "leave":
            announce("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        



