from game import location
import game.config as config
from game.display import announce
from game.events import *
from game.items import Item
import random
import numpy
from game import event
from game.combat import Monster
import game.combat as combat
from game.display import menu

REPAIR_TOOLS_COUNTER = 9


class Water7(location.Location):
    def __init__(self, x, y, world):
        super().__init__(x, y, world)
        self.name = "Water 7"
        self.symbol = "Y"
        self.visitable = True
        self.starting_location = Harbor(self)
        self.locations = {
            "harbor": self.starting_location,
            "dryDock1": DryDock1(self),
            "marketDistrict": MarketDistrict(self),
            "fountainOfYouth": FountainOfYouth(self),
            "lightHouse": LightHouse(self),
            "iceburghMansion": IceburghMansion(self),
            "blueprintArchives": BluePrintArchives(self),
            "workshops": WorkShops(self),
        }

    def enter(self, ship):
        announce(
            "As your ship approaches the fabled island of Water 7, you notice strange interference causing all your instruments to malfunction."
        )

    def visit(self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

    def end_turn(self):
        global REPAIR_TOOLS_COUNTER
        if REPAIR_TOOLS_COUNTER == 10:
            config.the_player.next_loc = self.locations["workshops"]
        if config.the_player.next_loc != None:
            config.the_player.location = config.the_player.next_loc
        config.the_player.location.enter()
        config.the_player.next_loc = None


class Harbor(location.SubLocation):
    def __init__(self, mainlocation):
        super().__init__(mainlocation)
        self.name = "harbor"
        self.verbs["north"] = self
        self.verbs["harbor"] = self
        self.verbs["dryDock1"] = self
        self.verbs["marketDistrict"] = self
        self.verbs["fountainOfYouth"] = self
        self.verbs["lightHouse"] = self
        self.verbs["iceburghMansion"] = self
        self.verbs["blueprintArchives"] = self
        self.verbs["workshops"] = self
        self.verbs["enter"] = self
        self.verbs["map"] = self
        self.description_printed = False

    def enter(self):
        if not self.description_printed:
            announce(
                "As your ship nears the island, you spot the white stone lighthouse perched atop rocky cliffs that jut sharply from the sea."
            )
            announce(
                "Its beacon helps guide your malfunctioning ship towards the busy harbor."
            )
            announce(
                "Huge mechanical cranes operated by teams of overall-clad workers rise from the piers, loading and unloading cargo from ships docked in the bustling port."
            )
            announce(
                "Together, you dock the ship and set out to repair it on the island."
            )

        self.description_printed = True

        announce("You can use map command to navigate.")
        announce("Type go (placename) without any space in between them to go there.")

    def process_verb(self, verb, cmd_list, nouns):
        global REPAIR_TOOLS_COUNTER
        if verb == "north" and REPAIR_TOOLS_COUNTER == 20:
            announce("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False

        elif verb == "harbor":
            config.the_player.next_loc = self.main_location.locations["harbor"]

        elif verb == "drydock1":
            config.the_player.next_loc = self.main_location.locations["dryDock1"]

        elif verb == "marketdistrict":
            config.the_player.next_loc = self.main_location.locations["marketDistrict"]

        elif verb == "fountainofyouth":
            config.the_player.next_loc = self.main_location.locations["fountainOfYouth"]

        elif verb == "lighthouse":
            config.the_player.next_loc = self.main_location.locations["lightHouse"]

        elif verb == "iceburghmansion":
            config.the_player.next_loc = self.main_location.locations["iceburghMansion"]

        elif verb == "blueprintarchives":
            config.the_player.next_loc = self.main_location.locations[
                "blueprintArchives"
            ]

        elif verb == "workshops":
            config.the_player.next_loc = self.main_location.locations["workshops"]

        elif verb == "map":
            self.print_map()

        else:
            announce(
                "You cannot return to your ship unless the malfunctioning of the ship is not fixed."
            )

    def print_map(self):
        map = (
            "OCEANSide                                                    OCEANSide              "
            + "\n"
        )
        map += (
            "TTTTTTTTTTTTTTTTT                                           TTTTTTTTTTTTTTTTT        "
            + "\n"
        )
        map += (
            "TTT~~~~~^^^^^^^~~~~~TTT        LIGHTHOUSE                    TTT~~~~~^^^^^^^~~~~~TTT  "
            + "\n"
        )
        map += (
            "TTT                    TTT                                 TTT                    TTT  "
            + "\n"
        )
        map += (
            "NORTH               TTT   T BLUEPRINT ARCHIVES             TTT                     TTT  "
            + "\n"
        )
        map += (
            "                   TTT^^^^^TTT                              TTT^^^^^^^DOCKS^^^^^^^TTT  "
            + "\n"
        )
        map += (
            "                TT        TT                             TT          HARBOR       TT "
            + "\n"
        )
        map += (
            "                T ICEBERG'S TT                           T                        T "
            + "\n"
        )
        map += (
            "                T  MANSION   TT                          T                         T "
            + "\n"
        )
        map += (
            "                T             T                         T                          T "
            + "\n"
        )
        map += (
            "            |              |                        |                           |     "
            + "\n"
        )
        map += (
            "WORKSHOPS --> |                                         |             DRYDOCK1     |  "
            + "\n"
        )
        map += (
            "|    |    |    |                                            & FOREMAN KAKU         |  "
            + "\n"
        )
        map += (
            "|    |    |    |                                                               |     "
            + "\n"
        )
        map += (
            "|~~~ |    |    |                                                               |    "
            + "\n"
        )
        map += (
            "|    |    |    |                                                               |   "
            + "\n"
        )
        map += (
            "|    |    |    |                                                                 |"
            + "\n"
        )
        map += (
            "WEST     W   |                                                                 | "
            + "\n"
        )
        map += (
            "            |                                                               "
            + "\n"
        )
        map += (
            "            |                                  MARKET DISTRICT                       "
            + "\n"
        )
        map += (
            "            |                      5 spaces-->                                "
            + "\n"
        )
        map += (
            "                20 spaces                             <-5 spaces-->|         "
            + "\n"
        )
        map += (
            "                            |              |                     TTT        "
            + "\n"
        )
        map += (
            "                            |              |                    TTT         "
            + "\n"
        )
        map += (
            "                            |              |                   TTT         "
            + "\n"
        )
        map += (
            "                                25 spaces FOUNTAIN OF  25 spaces            TTTTT       "
            + "\n"
        )
        map += "                                            YOUTH                               TTTTTT"

        print(map)


class DryDock1(location.SubLocation):
    def __init__(self, mainlocation):
        super().__init__(mainlocation)
        self.name = "dryDock1"
        self.verbs["harbor"] = self
        self.verbs["dryDock1"] = self
        self.verbs["marketDistrict"] = self
        self.verbs["fountainOfYouth"] = self
        self.verbs["lightHouse"] = self
        self.verbs["iceburghMansion"] = self
        self.verbs["blueprintArchives"] = self
        self.verbs["workshops"] = self
        self.verbs["enter"] = self
        self.verbs["map"] = self

        self.event_chance = 50
        self.events.append(seagull.Seagull())
        self.events.append(drowned_pirates.DrownedPirates())
        self.events.append(man_eating_monkeys.ManEatingMonkeys())

    def enter(self):
        description1 = "After working to bring your damaged ship to the central Dry Docks with Foreman Kaku's approval, he criticizes your old and malfunctioning mechanical systems.\n"
        description2 = "He gestures to the warehouses of salvaged ship parts and challenges your crew to build replacement systems from scratch using your own innovation and limited resources.\n"
        description3 = "You are tasked with combining bits of broken ships - timber supports, metal plates, barrels, gears, coal engines, ropes and pulleys - to construct new steering, power, and navigation mechanisms for your unresponsive vessel.\n"
        description4 = "You'll have to calculatedly measure, lift, fasten and position the parts together into functioning apparatuses.\n"
        description5 = "Kaku's favor depends on whether the new systems operate efficiently when installed."

        announce(
            "Kaku's approval is needed for you to access the tools and materials to fix your own ship."
        )
        announce(description1)
        announce(description2)
        announce(description3)
        announce(description4)
        announce(description5)

        global REPAIR_TOOLS_COUNTER
        if REPAIR_TOOLS_COUNTER == 19:
            announce(
                "Kaku is overjoyed to see that you have brought all of the repair tools he requested."
            )
            announce(
                "In order for you to fix your ship and navigate the seas, he provides you the last of the repair tools."
            )
            # annpunce that they can now go back to their ship
            REPAIR_TOOLS_COUNTER += 1

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "harbor":
            config.the_player.next_loc = self.main_location.locations["harbor"]

        if verb == "drydock1":
            config.the_player.next_loc = self.main_location.locations["dryDock1"]

        if verb == "marketdistrict":
            config.the_player.next_loc = self.main_location.locations["marketDistrict"]

        if verb == "fountainofyouth":
            config.the_player.next_loc = self.main_location.locations["fountainOfYouth"]

        if verb == "lighthouse":
            config.the_player.next_loc = self.main_location.locations["lightHouse"]

        if verb == "iceburghmansion":
            config.the_player.next_loc = self.main_location.locations["iceburghMansion"]

        if verb == "blueprintarchives":
            config.the_player.next_loc = self.main_location.locations[
                "blueprintArchives"
            ]

        if verb == "workshops":
            config.the_player.next_loc = self.main_location.locations["workshops"]

        if verb == "map":
            Harbor.print_map(self)


class MarketDistrict(location.SubLocation):
    def __init__(self, mainlocation):
        super().__init__(mainlocation)
        self.name = "marketDistrict"
        self.verbs["harbor"] = self
        self.verbs["dryDock1"] = self
        self.verbs["marketDistrict"] = self
        self.verbs["fountainOfYouth"] = self
        self.verbs["lightHouse"] = self
        self.verbs["iceburghMansion"] = self
        self.verbs["blueprintArchives"] = self
        self.verbs["workshops"] = self
        self.verbs["enter"] = self
        self.verbs["map"] = self

        self.event_chance = 50
        self.events.append(seagull.Seagull())
        self.events.append(drowned_pirates.DrownedPirates())
        self.events.append(man_eating_monkeys.ManEatingMonkeys())

        self.marketDistrictUsed = False
        self.RIDDLE_AMOUNT = 3

    def enter(self):
        announce(
            "A wide canal cuts directly through the market square, buzzing with small fishing boats unloading their catch onto floating docks."
        )
        announce(
            "Bridges arch over the waterway, connecting the fishmongers to the butchers, bakers and traders on the opposite bank."
        )
        announce(
            "In between shops lie crowded taverns and inns, filled with sailors, travelers and workers taking their breakfast."
        )
        announce(
            "You overhear a group whispering about secret warehouses full of rescued shipwrecks - and the treasures within."
        )
        announce("You can find some repair tools there. Do you wanna enter?")

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "harbor":
            config.the_player.next_loc = self.main_location.locations["harbor"]

        if verb == "drydock1":
            config.the_player.next_loc = self.main_location.locations["dryDock1"]

        if verb == "marketdistrict":
            config.the_player.next_loc = self.main_location.locations["marketDistrict"]

        if verb == "fountainofyouth":
            config.the_player.next_loc = self.main_location.locations["fountainOfYouth"]

        if verb == "lighthouse":
            config.the_player.next_loc = self.main_location.locations["lightHouse"]

        if verb == "iceburghmansion":
            config.the_player.next_loc = self.main_location.locations["iceburghMansion"]

        if verb == "blueprintarchives":
            config.the_player.next_loc = self.main_location.locations[
                "blueprintArchives"
            ]

        if verb == "workshops":
            config.the_player.next_loc = self.main_location.locations["workshops"]

        if verb == "enter":
            self.handleMarketDistrict()

        if verb == "map":
            Harbor.print_map(self)

    def handleMarketDistrict(self):
        if not self.marketDistrictUsed:
            announce(
                "A rowdy gang comes and challenge you in Riddle battle. If you win they will provide you with 3 anchor (woodworking tools)"
            )
            choice = input("Do you except their challenge (yes/no): ")
            if "yes" in choice.lower():
                self.handleRiddleBattle()
            else:
                announce("You turn away from the challenge.")
        else:
            announce("The gang mocks and laughs at you.")

    def handleRiddleBattle(self):
        riddleBattle = self.getRiddleAndAnswer()
        max_guess = self.RIDDLE_AMOUNT
        self.riddleBattlePlayed = True

        while max_guess > 0:
            print(riddleBattle[0])
            plural = ""
            if max_guess != 1:
                plural = "s"

            print(f"You have {max_guess} guesses left.")
            choice = input("What's your guess? ")

            if riddleBattle[1] in choice.lower():
                self.riddleBattleReward()
                announce("You get the reward and leave the place.")
                max_guess = 0
            else:
                max_guess -= 1
                announce("Your guess is incorrect.")

    def riddleBattleReward(self):
        global REPAIR_TOOLS_COUNTER
        REPAIR_TOOLS_COUNTER += 3

    def getRiddleAndAnswer(self):
        riddleList = [
            (
                "Pronounced as 1 letter, And written with 3, 2 letters there are, and 2 only in me. I’m double, I’m single, I’m black blue, and gray, I’m read from both ends, and the same either way. What am I?",
                "eye",
            )
        ]
        return random.choice(riddleList)


class LightHouse(location.SubLocation):
    def __init__(self, mainlocation):
        super().__init__(mainlocation)
        self.name = "lightHouse"
        self.verbs["harbor"] = self
        self.verbs["dryDock1"] = self
        self.verbs["marketDistrict"] = self
        self.verbs["fountainOfYouth"] = self
        self.verbs["lightHouse"] = self
        self.verbs["iceburghMansion"] = self
        self.verbs["blueprintArchives"] = self
        self.verbs["workshops"] = self
        self.verbs["enter"] = self
        self.verbs["map"] = self

        self.event_chance = 50
        self.events.append(man_eating_monkeys.ManEatingMonkeys())
        self.events.append(drowned_pirates.DrownedPirates())

        self.lightHouseUsed = False
        self.RIDDLE_AMOUNT = 3

    def enter(self):
        announce(
            "Perched atop lonely, wind-swept cliffs on the northwestern coast sits the weathered Lighthouse of Hidden Rock."
        )
        announce(
            "Its once bright white facade now faded and cracked, the tall tower stands silent, its beacon long extinguished."
        )
        announce(
            "The cliffs form a natural barrier from inland access, with only a precarious path winding down the sheer rock face to where waves smash against the stony foundations."
        )
        announce("You can enter the Light House.")

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "harbor":
            config.the_player.next_loc = self.main_location.locations["harbor"]

        if verb == "drydock1":
            config.the_player.next_loc = self.main_location.locations["dryDock1"]

        if verb == "marketdistrict":
            config.the_player.next_loc = self.main_location.locations["marketDistrict"]

        if verb == "fountainofyouth":
            config.the_player.next_loc = self.main_location.locations["fountainOfYouth"]

        if verb == "lighthouse":
            config.the_player.next_loc = self.main_location.locations["lightHouse"]

        if verb == "iceburghmansion":
            config.the_player.next_loc = self.main_location.locations["iceburghMansion"]

        if verb == "blueprintarchives":
            config.the_player.next_loc = self.main_location.locations[
                "blueprintArchives"
            ]

        if verb == "workshops":
            config.the_player.next_loc = self.main_location.locations["workshops"]

        if verb == "enter":
            self.handleLightHouse()

        if verb == "map":
            Harbor.print_map(self)

    def handleLightHouse(self):
        if not self.lightHouseUsed:
            announce(
                "Inside at the old keeper's desk lays a worn logbook with a riddle. You can solve this riddle"
            )
            choice = input(
                "Deciphering this will give you repair tools. Do you wanna solve the riddle?(yes/no): "
            )
            if "yes" in choice.lower():
                self.handlePoemRiddles()
            else:
                announce("You leave the Light House.")
        else:
            announce("The Light House is Untouched.")

    def handlePoemRiddles(self):
        poemRiddle = self.getPoemRiddleAndAnswer()
        max_guess = self.RIDDLE_AMOUNT
        self.lightHouseUsed = True

        while max_guess > 0:
            print(poemRiddle[0])
            plural = ""
            if max_guess != 1:
                plural = "s"

            print(f"You have {max_guess} guesses left.")
            choice = input("What's your guess? ")

            if poemRiddle[1] in choice.lower():
                self.poemRiddleReward()
                announce(
                    "You got the correct answer and have been awarded 2 repair tools bucket and hammer"
                )
                max_guess = 0
            else:
                max_guess -= 1
                announce("Your guess is incorrect.")

    def poemRiddleReward(self):
        global REPAIR_TOOLS_COUNTER
        REPAIR_TOOLS_COUNTER += 2

        for i in config.the_player.get_pirates():
            i.health = i.max_health

    def getPoemRiddleAndAnswer(self):
        riddleList = [
            (
                "I am an odd number. Take away a letter and I become even. What number am I?",
                "seven",
            )
        ]
        return random.choice(riddleList)


class IceburghMansion(location.SubLocation):
    def __init__(self, mainlocation):
        super().__init__(mainlocation)
        self.name = "iceburghMansion"
        self.verbs["harbor"] = self
        self.verbs["dryDock1"] = self
        self.verbs["marketDistrict"] = self
        self.verbs["fountainOfYouth"] = self
        self.verbs["lightHouse"] = self
        self.verbs["iceburghMansion"] = self
        self.verbs["blueprintArchives"] = self
        self.verbs["workshops"] = self
        self.verbs["enter"] = self
        self.verbs["map"] = self

        self.IceburghMansionUsed = False
        self.RIDDLE_AMOUNT = 3

        self.event_chance = 50
        self.events.append(seagull.Seagull())
        self.events.append(drowned_pirates.DrownedPirates())
        self.events.append(man_eating_monkeys.ManEatingMonkeys())

    def enter(self):
        description1 = "The stately manor of Water 7’s reclusive mayor and chief shipwright, Iceberg, lies inland guarded by high walls."
        description2 = "Invitees occasionally emerge relating fantastic sketches of impenetrable vessels soon to be constructed here using hidden means."
        description3 = "You can enter the mansion and try to impress the mayor."

        announce(description1)
        announce(description2)
        announce(description3)

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "harbor":
            config.the_player.next_loc = self.main_location.locations["harbor"]

        if verb == "drydock1":
            config.the_player.next_loc = self.main_location.locations["dryDock1"]

        if verb == "marketdistrict":
            config.the_player.next_loc = self.main_location.locations["marketDistrict"]

        if verb == "fountainofyouth":
            config.the_player.next_loc = self.main_location.locations["fountainOfYouth"]

        if verb == "lighthouse":
            config.the_player.next_loc = self.main_location.locations["lightHouse"]

        if verb == "iceburghmansion":
            config.the_player.next_loc = self.main_location.locations["iceburghMansion"]

        if verb == "blueprintarchives":
            config.the_player.next_loc = self.main_location.locations[
                "blueprintArchives"
            ]

        if verb == "workshops":
            config.the_player.next_loc = self.main_location.locations["workshops"]

        if verb == "map":
            Harbor.print_map(self)

        if verb == "enter":
            self.handleIceburghMansion()

    def handleIceburghMansion(self):
        if not self.IceburghMansionUsed:
            announce(
                "You found the mayor who is very fond of riddle. He challenges you with his riddle."
            )
            choice = input("Do you accept the challenge(yes/no): ")
            if "yes" in choice.lower():
                self.handleRiddleBattle()
            else:
                announce("You just talk with mayor.")
        else:
            announce("You exit the Mansion.")

    def handleRiddleBattle(self):
        riddleBattle = self.getRiddleAndAnswer()
        max_guess = self.RIDDLE_AMOUNT
        self.riddleBattlePlayed = True

        while max_guess > 0:
            print(riddleBattle[0])
            plural = ""
            if max_guess != 1:
                plural = "s"

            print(f"You have {max_guess} guesses left.")
            choice = input("What's your guess? ")

            if riddleBattle[1] in choice.lower():
                self.riddleBattleReward()
                announce(
                    "Mayor gets very happy by your answers and rewards you 2 repair tools."
                )
                max_guess = 0
            else:
                max_guess -= 1
                announce("Your guess is incorrect.")

    def riddleBattleReward(self):
        global REPAIR_TOOLS_COUNTER
        REPAIR_TOOLS_COUNTER += 2

    def getRiddleAndAnswer(self):
        riddleList = [
            (
                "I come from a mine and get surrounded by wood always. Everyone uses me. What am I?",
                "pencil",
            )
        ]
        return random.choice(riddleList)


class BluePrintArchives(location.SubLocation):
    def __init__(self, mainlocation):
        super().__init__(mainlocation)
        self.name = "blueprintArchive"
        self.verbs["harbor"] = self
        self.verbs["dryDock1"] = self
        self.verbs["marketDistrict"] = self
        self.verbs["fountainOfYouth"] = self
        self.verbs["lightHouse"] = self
        self.verbs["iceburghMansion"] = self
        self.verbs["blueprintArchives"] = self
        self.verbs["workshops"] = self
        self.verbs["enter"] = self
        self.verbs["map"] = self

        self.BlueprintArchiveUsed = False
        self.RIDDLE_AMOUNT = 3

        self.event_chance = 50
        self.events.append(seagull.Seagull())
        self.events.append(drowned_pirates.DrownedPirates())
        self.events.append(man_eating_monkeys.ManEatingMonkeys())

    def enter(self):
        description1 = "In a squat domed hall, rows of intricate mechanical receptacles house the island’s revolutionary schematics and daring theoretical designs."
        description2 = "Good luck winning favor with its stern gatekeeper for access to the innovative breakthroughs within. Just enter inside it."

        announce(description1)
        announce(description2)

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "harbor":
            config.the_player.next_loc = self.main_location.locations["harbor"]

        if verb == "drydock1":
            config.the_player.next_loc = self.main_location.locations["dryDock1"]

        if verb == "marketdistrict":
            config.the_player.next_loc = self.main_location.locations["marketDistrict"]

        if verb == "fountainofyouth":
            config.the_player.next_loc = self.main_location.locations["fountainOfYouth"]

        if verb == "lighthouse":
            config.the_player.next_loc = self.main_location.locations["lightHouse"]

        if verb == "iceburghmansion":
            config.the_player.next_loc = self.main_location.locations["iceburghMansion"]

        if verb == "blueprintarchives":
            config.the_player.next_loc = self.main_location.locations[
                "blueprintArchives"
            ]

        if verb == "workshops":
            config.the_player.next_loc = self.main_location.locations["workshops"]

        if verb == "map":
            Harbor.print_map(self)

        if verb == "enter":
            self.handleBlueprintArchive()

    def handleBlueprintArchive(self):
        if not self.BlueprintArchiveUsed:
            announce(
                "The gatekeeper asks you a riddle. If you can solve it you will get 1 repair tool."
            )
            choice = input("Do you wanna take this challenge(yes/no): ")
            if "yes" in choice.lower():
                self.handleRiddleBattle()
            else:
                announce("You turn away from the challenge.")
        else:
            announce("The gatekeeper kicks you out.")

    def handleRiddleBattle(self):
        riddleBattle = self.getRiddleAndAnswer()
        max_guess = self.RIDDLE_AMOUNT
        self.riddlePlayed = True

        while max_guess > 0:
            print(riddleBattle[0])
            plural = ""
            if max_guess != 1:
                plural = "s"

            print(f"You have {max_guess} guesses left.")
            choice = input("What's your guess? ")

            if riddleBattle[1] in choice.lower():
                self.riddleBattleReward()
                announce("You guessed it correctly and received 1 repair tool.")
                max_guess = 0
            else:
                max_guess -= 1
                announce("Your guess is incorrect.")

    def riddleBattleReward(self):
        global REPAIR_TOOLS_COUNTER
        REPAIR_TOOLS_COUNTER += 1

        for i in config.the_player.get_pirates():
            i.health = i.max_health

    def getRiddleAndAnswer(self):
        riddleList = [
            (
                "I have cities, but no houses. I have mountains, but no trees. I have water, but no fish. What am I?",
                "map",
            )
        ]
        return random.choice(riddleList)


class WorkShops(location.SubLocation):
    def __init__(self, mainlocation):
        super().__init__(mainlocation)
        self.name = "workshops"
        self.verbs["harbor"] = self
        self.verbs["dryDock1"] = self
        self.verbs["marketDistrict"] = self
        self.verbs["fountainOfYouth"] = self
        self.verbs["lightHouse"] = self
        self.verbs["iceburghMansion"] = self
        self.verbs["blueprintArchives"] = self
        self.verbs["workshops"] = self
        self.verbs["enter"] = self
        self.verbs["map"] = self

        self.fireEventDone = False
        self.RIDDLE_AMOUNT = 3

        self.event_chance = 50
        self.events.append(seagull.Seagull())
        self.events.append(drowned_pirates.DrownedPirates())
        self.events.append(man_eating_monkeys.ManEatingMonkeys())

    def enter(self):
        global REPAIR_TOOLS_COUNTER

        if REPAIR_TOOLS_COUNTER < 10 or REPAIR_TOOLS_COUNTER > 10:
            description = "Workshops large and small dot the city, filing the air with hissing steam, grinding gears, and hammering metal as new gadgets and machines are created.\n The spirit of innovation and progress seems to fill Water 7's residents."
            announce(description)
        elif REPAIR_TOOLS_COUNTER == 10:
            self.handleFireEvent()
            self.fireEventDone = True

    def handleFireEvent(self):
        description1 = (
            "Flames suddenly erupt from a corner workshop near the dry docks."
        )
        description2 = "The fire quickly spreads, trapping workers and threatening whole rooms of half-built ship components."
        description3 = "Time is of essence! You can either rush to evacuate the 5 workers still in peril, or deduce the emergency extinguishing system puzzle to halt the fire's advance. "
        description4 = (
            "Completing both objectives minimizes harm and earns the Mayor's favor."
        )

        announce(description1)
        announce(description2)
        announce(description3)
        announce(description4)

        choice = input("Choose 1 to: \n 1. Help evacuate workers and stop fire \n")

        if choice == "1":
            announce("You help all the workers escape the fire.")
            # Need some info for solving the riddle and setting off the fire.
            self.handleFireRiddle()

    def handleFireRiddle(self):
        riddleBattle = self.getRiddleAndAnswer()
        max_guess = self.RIDDLE_AMOUNT

        while max_guess > 0:
            print(riddleBattle[0])
            plural = ""
            if max_guess != 1:
                plural = "s"

            print(f"You have {max_guess} guesses left.")
            choice = input("What's your guess? ")

            if riddleBattle[1] in choice.lower():
                self.riddleBattleReward()
                announce(
                    "You are thanked by all the residents and Mayor awarded you with 9 repair tools because of your bravery."
                )
                max_guess = 0
            else:
                max_guess -= 1
                announce("Your guess is incorrect.")

    def riddleBattleReward(self):
        global REPAIR_TOOLS_COUNTER
        REPAIR_TOOLS_COUNTER += 9

    def getRiddleAndAnswer(self):
        riddleList = [
            (
                "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?",
                "echo",
            )
        ]
        return random.choice(riddleList)

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "harbor":
            config.the_player.next_loc = self.main_location.locations["harbor"]

        if verb == "drydock1":
            config.the_player.next_loc = self.main_location.locations["dryDock1"]

        if verb == "marketdistrict":
            config.the_player.next_loc = self.main_location.locations["marketDistrict"]

        if verb == "fountainofyouth":
            config.the_player.next_loc = self.main_location.locations["fountainOfYouth"]

        if verb == "lighthouse":
            config.the_player.next_loc = self.main_location.locations["lightHouse"]

        if verb == "iceburghmansion":
            config.the_player.next_loc = self.main_location.locations["iceburghMansion"]

        if verb == "blueprintarchives":
            config.the_player.next_loc = self.main_location.locations[
                "blueprintArchives"
            ]

        if verb == "workshops":
            config.the_player.next_loc = self.main_location.locations["workshops"]

        if verb == "map":
            Harbor.print_map(self)


class FountainOfYouth(location.SubLocation):
    def __init__(self, mainlocation):
        super().__init__(mainlocation)
        self.name = "fountainOfYouth"
        self.verbs["harbor"] = self
        self.verbs["dryDock1"] = self
        self.verbs["marketDistrict"] = self
        self.verbs["fountainOfYouth"] = self
        self.verbs["lightHouse"] = self
        self.verbs["iceburghMansion"] = self
        self.verbs["blueprintArchives"] = self
        self.verbs["workshops"] = self
        self.verbs["enter"] = self
        self.verbs["map"] = self

        self.FountainofYouthUsed = False
        self.RIDDLE_AMOUNT = 3

        self.event_chance = 50
        self.events.append(seagull.Seagull())
        self.events.append(drowned_pirates.DrownedPirates())
        self.events.append(man_eating_monkeys.ManEatingMonkeys())

    def enter(self):
        announce(
            "Secluded, shimmering waters imbued with otherworldly restorative properties both coveted yet feared if misused. You can enter the fountain."
        )

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "harbor":
            config.the_player.next_loc = self.main_location.locations["harbor"]

        if verb == "drydock1":
            config.the_player.next_loc = self.main_location.locations["dryDock1"]

        if verb == "marketdistrict":
            config.the_player.next_loc = self.main_location.locations["marketDistrict"]

        if verb == "fountainofyouth":
            config.the_player.next_loc = self.main_location.locations["fountainOfYouth"]

        if verb == "lighthouse":
            config.the_player.next_loc = self.main_location.locations["lightHouse"]

        if verb == "iceburghmansion":
            config.the_player.next_loc = self.main_location.locations["iceburghMansion"]

        if verb == "blueprintarchives":
            config.the_player.next_loc = self.main_location.locations[
                "blueprintArchives"
            ]

        if verb == "workshops":
            config.the_player.next_loc = self.main_location.locations["workshops"]

        if verb == "map":
            Harbor.print_map(self)

        if verb == "enter":
            self.handleFountainofYouth()

    def handleFountainofYouth(self):
        if not self.FountainofYouthUsed:
            announce("You are challenged by the guardian of the fountain.")
            choice = input("Do you wanna accept the challenge (yes/no): ")
            if "yes" in choice.lower():
                self.handleRiddleBattle()
            else:
                announce("You turn away.")
        else:
            announce("The fountain lays dormant.")

    def handleRiddleBattle(self):
        riddleBattle = self.getRiddleAndAnswer()
        max_guess = self.RIDDLE_AMOUNT
        self.FountainofYouthUsed = True

        while max_guess > 0:
            print(riddleBattle[0])
            plural = ""
            if max_guess != 1:
                plural = "s"

            print(f"You have {max_guess} guesses left.")
            choice = input("What's your guess? ")

            if riddleBattle[1] in choice.lower():
                self.riddleBattleReward()
                announce("Guardian is happy from your answer and gave 2 repair tools.")
                max_guess = 0
            else:
                max_guess -= 1
                announce("Your guess is incorrect.")

    def riddleBattleReward(self):
        global REPAIR_TOOLS_COUNTER
        REPAIR_TOOLS_COUNTER += 2

    def getRiddleAndAnswer(self):
        riddleList = [
            (
                "You measure my life in hours and I serve you by expiring. I’m quick when I’m thin and slow when I’m fat. The wind is my enemy.",
                "candle",
            )
        ]
        return random.choice(riddleList)
