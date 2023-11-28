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


class Harbor(location.SubLocation):
    def __init__(self, mainlocation):
        super().__init__(mainlocation)
        self.name = "harbor"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["west"] = self
        self.description_printed = True

    def enter(self):
        if self.description_printed:
            announce(
                "As your ship nears the island, you spot the white stone lighthouse perched atop rocky cliffs that jut sharply from the sea."
            )
            announce(
                "Its beacon helps guide your malfunctioning ship towards the busy harbor."
            )
            announce(
                "Huge mechanical cranes operated by teams of overall-clad workers rise from the piers, loading and unloading cargo from ships docked in the bustling port."
            )
        announce("Together, you dock the ship and set out to repair it on the island.")
        self.description_printed = False

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "north":
            announce(
                "You cannot return to your ship unless the malfunctioning of the ship is not fixed."
            )

        if verb == "south":
            config.the_player.next_loc = self.main_location.locations["dryDock1"]

        if verb == "west":
            config.the_player.next_loc = self.main_location.locations["lightHouse"]


class DryDock1(location.SubLocation):
    def __init__(self, mainlocation):
        super().__init__(mainlocation)
        self.name = "dryDock1"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["west"] = self
        self.verbs["east"] = self
        self.description_printed = True

    def enter(self):
        description = "After working to bring your damaged ship to the central Dry Docks with Foreman Kaku's approval, he criticizes your old and malfunctioning mechanical systems.\n"
        description += "He gestures to the warehouses of salvaged ship parts and challenges your crew to build replacement systems from scratch using your own innovation and limited resources.\n"
        description += "You are tasked with combining bits of broken ships - timber supports, metal plates, barrels, gears, coal engines, ropes and pulleys - to construct new steering, power, and navigation mechanisms for your unresponsive vessel.\n"
        description += "You'll have to calculatedly measure, lift, fasten and position the parts together into functioning apparatuses.\n"
        description += "Kaku's favor depends on whether the new systems operate efficiently when installed."

        if self.description_printed:
            announce(
                "Making your way down the cluttered docks past fish markets and noisy taverns, you enter the city."
            )
            announce(
                "The buildings seem to sprout directly from the waterways crisscrossing the island, connected by elaborate bridges and locks."
            )
            announce(
                "The structures combine brick, metal, and timber in engineering feats you've never seen before."
            )
            announce(
                "At the heart of the harbor lies the impressive Dry Dock 1, ringed by scaffolds and sheds."
            )
            announce(
                "The air rings with the cacophony of sawing, hammering and welding as burly men repair ships of all sizes under the watch of foreman Kaku."
            )
        announce(
            "Kaku's approval is needed for you to access the tools and materials to fix your own ship."
        )
        announce(description)

        self.description_printed = False

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "north":
            config.the_player.next_loc = self.main_location.locations["harbor"]

        if verb == "south":
            config.the_player.next_loc = self.main_location.locations["marketDistrict"]

        if verb == "west":
            config.the_player.next_loc = self.main_location.locations["iceburghMansion"]

        if verb == "east":
            config.the_player.next_loc = self.main_location.locations[
                "blueprintArchives"
            ]


class MarketDistrict(location.SubLocation):
    def __init__(self, mainlocation):
        super().__init__(mainlocation)
        self.name = "marketDistrict"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.description_printed = True

    def enter(self):
        if self.description_printed:
            announce(
                "Pushing your way through the crowded streets, you emerge into the bustling marketplace at the heart of the city."
            )
            announce(
                "Vendors call out to passersby, selling fresh fish, steamed buns, intricately crafted gears and gadgets."
            )
            announce("The aroma of cooked meat mixes with the tang of salt air.")
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
            "You overhear a group whispering about secret warehouses full of rescued shipwrecks - and the treasures within. One table plays a rowdy gambling game using dice and tiny wooden ships."
        )
        self.description_printed = False

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "north":
            config.the_player.next_loc = self.main_location.locations["dryDock1"]

        if verb == "south":
            config.the_player.next_loc = self.main_location.locations["fountainOfYouth"]

        if verb == "east":
            config.the_player.next_loc = self.main_location.locations["workshops"]


class LightHouse(location.SubLocation):
    def __init__(self, mainlocation):
        super().__init__(mainlocation)
        self.name = "lightHouse"
        self.verbs["east"] = self
        self.verbs["enter"] = self

        self.description_printed = True
        self.lightHouseUsed = False
        self.RIDDLE_AMOUNT = 3

    def enter(self):
        if self.description_printed:
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

        self.description_printed = False

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "east":
            config.the_player.next_loc = self.main_location.locations["harbor"]

        if verb == "enter":
            self.handleLightHouse()

    def handleLightHouse(self):
        if not self.lightHouseUsed:
            announce(
                "Inside at the old keeper's desk lays a worn logbook with a poem. You can solve this poem"
            )
            choice = input(
                "Deciphering this will give you repair tools. Do you wanna solve the poem?"
            )
            if "yes" in choice.lower():
                self.handlePoemRiddle()
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

            print(f"You have {max_guess} left.")
            choice = input("What's your guess?")

            if poemRiddle[1] in choice.lower():
                self.poemRiddleReward()
                announce("")


class IceburghMansion(location.SubLocation):
    def __init__(self, mainlocation):
        super().__init__(mainlocation)
        self.name = "iceburghMansion"
        self.verbs["east"] = self
        self.description_printed = True

    def enter(self):
        pass

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "east":
            config.the_player.next_loc = self.main_location.locations["dryDock1"]


class BluePrintArchives(location.SubLocation):
    def __init__(self, mainlocation):
        super().__init__(mainlocation)
        self.name = "blueprintArchive"
        self.verbs["west"] = self
        self.description_printed = True

    def enter(self):
        pass

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "west":
            config.the_player.next_loc = self.main_location.locations["marketDistrict"]


class WorkShops(location.SubLocation):
    def __init__(self, mainlocation):
        super().__init__(mainlocation)
        self.name = "workshops"
        self.verbs["west"] = self
        self.description_printed = True

    def enter(self):
        pass

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "west":
            config.the_player.next_loc = self.main_location.locations["fountainOfYouth"]


class FountainOfYouth(location.SubLocation):
    def __init__(self, mainlocation):
        super().__init__(mainlocation)
        self.name = "fountainOfYouth"
        self.verbs["north"] = self
        self.description_printed = True

    def enter(self):
        pass

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "north":
            config.the_player.next_loc = self.main_location.locations["marketDistrict"]
