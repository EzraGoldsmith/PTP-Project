import tkinter as tk
from Rooms import Room
from Player import Player
import Text
import GUI


class Game:
    """
    The 'Game' class is responsible for running the game in its entirety, whereas all other classes only provide
    the framework for a text-based adventure game with attributes created and handles by the 'Player', 'Rooms', 'Text'
    and 'GUI' modules (for more information on these, please refer to their respective class documentation.)

    A primary, core gameplay loop is outlined within the 'play' class method, which assigns any required functionality
    to other methods for handling. Each of these methods may be directed to by 'runAction', which takes a user input
    through the 'prepareInput' method and assesses which of these should be carried out - all valid action word inputs
    are listed within the 'actions' attribute.
    'doGoAction', 'doMenuAction' and 'doInteractAction' methods when called handle these nested functionalities, the
    latter being its own self-contained gameplay loop.

    This class alongside all others is purposefully designed so that a user can create their own game upon its
    framework; an example, "The Mysterious Mansion", is included to display all of program's features in action.
    (Please refer to each class and their methods for further explanation on how to implement these features.)
    """

    def __init__(self, title="The Mysterious Mansion"):
        """
        Upon being initialised, creation of the area in which the game takes place is handled by the 'createRooms'
        method, while the player's starting room is assigned also. The Player class is then instanced, responsible for
        handling all of the players attributes, and the game's narrative is handled by each class within the Text
        module.
        """

        self.title = title

        self.createRooms()                 # Creates area layout and fills with rooms
        self.currentRoom = self.startRoom  # Sets start room for player

        self.player = Player()  # Player added

        # Following 'story' attribute initialises the game's narrative, assigning the introductory text for later
        # printing in UI.
        self.story = Text.Narrative(
            "You're caught in a violent storm,\nforced to find shelter in a nearby building.",
            "Upon entering, its front doors slam shut behind you.",
            "You fall deep asleep while waiting out the storm...\n",
            "#",
            "Midnight.",
            "You awaken, dim candlelight\nnow illuminating the room.",
            title=self.title, exit=self.exitRoom.description
        )

        self.actions = ['GO', 'INSPECT', 'INVENTORY', 'HINT', 'QUIT']  # Base list of valid action words

    def createGUI(self):
        """
        Creates the end screen window once the main gameplay loop has terminated.
        """

        window = tk.Tk()
        window.title(self.title)
        window.geometry('350x350')
        window.resizable(False, False)

        call = GUI.App(window)
        window.mainloop()

    def createRooms(self):
        """
        Method allows for different room configurations to be created, as the user desires. Requires that the
        'startRoom' and 'exitRoom' attributes are included otherwise program could not run. Once all rooms have been
        created, the user may add interconnecting doors and room items as seen fit - the existing configuration may
        be used as a template, demonstrating the application of all available features.
        (For more on these features, please refer to the Rooms module documentation.)
        """

        # WARNING: Only the parameters of this 'startRoom' object should be changed (see method documentation.)
        self.startRoom = Room(
            'images/Lobby.jpeg',
            "Lobby",
            wordDescription="A grandiose room whose walls have been left barren of decor - light dances through\n"
                            "the dust kicked up by your entry.",
            writtenHint="You search around, only to happen across the odd pieces of broken glass and splinters."
        )

        self.roomC = Room(
            'images/Cellar.jpg',
            "Cellar",
            wordDescription="Down a spiral staircase, you're greeted by alcoholic fumes and empty bottles. A sole\n"
                            "glass, knocked over, has spilt recently..."
        )
        self.roomK = Room(
            'images/Kitchen.jpg',
            "Kitchen",
            wordDescription="Piles of rusting cutlery and mouldy stains render any surface untouchable."
        )
        self.roomDR = Room(
            'images/Dining Room.jpg',
            "Dining Room",
            wordDescription="Three crystal chandeliers, all lit, reveal a long room with a table at its centre,\n"
                            "set and ready prepared for guests.",
            writtenHint="At the end of the table you spot some cutlery that appears recently used.\n"
                        "A lone jacket hangs on the chair behind..."
        )
        self.roomLi = Room(
            'images/Library.jpg',
            "Library",
            wordDescription="Flickering tongues of flame burst from a fireplace. You see a door\n"
                            " barricaded by books, torn and tarnished."
        )
        self.roomSR = Room(
            'images/Storage Room.jpeg',
            "Storage Room",
            wordDescription="Your hands are barely visible in front of your face. The room is barely big\n"
                            "enough to stand in.",
            storeroom=True
        )
        self.roomA = Room(
            'images/Attic.jpg',
            "Attic",
            wordDescription="Rats race into the eaves as you summit the stairs. Dust sheets are laid over an\n"
                            "array of paintings, furniture and broken items.",
            writtenHint="Floorboards and overhead beams are laden with cobwebs. All, that is, bar one tile..."
        )
        self.roomD = Room(
            'images/Dungeon.jpg',
            "Dungeon",
            wordDescription="As if planned, the ladder hatch locks behind you. The stench of sewerage\n"
                            "nearly brings you to vomit.",
            writtenHint="There remains upon the far wall a collection of well-serviced cell keys.\n"
                        "Could one of them be of use?"
        )
        self.roomDC = Room(
            'images/Dungeon Cell.jpg',
            "Dungeon Cell",
            wordDescription="Anything that once existed in this cell has either been consumed by the rats or time.",
            writtenHint="Fading, you find inscribed onto the brick wall: O', the smell of my masters cooking... So\n"
                        "crisp and clear from the attic... - What could it mean?"
        )

        # WARNING: Only the parameters of this 'exitRoom' object should be changed (see method documentation.)
        self.exitRoom = Room('images/Exit', "Exit")

        # Once all rooms have been created, add features as done below:
        self.startRoom.createDoor("east", self.roomDR)
        self.startRoom.createDoor("west", self.roomLi)
        self.startRoom.createDoor("south", self.exitRoom, True, self.roomK)
        self.startRoom.createDoor("downstairs", self.roomC, True, self.roomC)
        self.startRoom.addItems("Broken key")
        self.roomC.createDoor("upstairs", self.startRoom)
        self.roomK.createDoor("south", self.roomDR)
        self.roomK.createDoor("upstairs", self.roomA)
        self.roomDR.createDoor("north", self.roomK, True)
        self.roomDR.createDoor("west", self.startRoom)
        self.roomLi.createDoor("north", self.roomSR, True, self.roomDR)
        self.roomLi.createDoor("upstairs", self.roomA)
        self.roomLi.createDoor("east", self.startRoom)
        self.roomSR.createDoor("south", self.roomLi)
        self.roomSR.createDoor("ladder", self.roomD)
        self.roomD.createDoor("ladder", self.roomSR, True)
        self.roomD.createDoor("east", self.roomDC, True, self.roomD)
        self.roomDC.createDoor("west", self.roomD)
        self.roomDC.createDoor("up", self.roomC)
        self.roomA.createDoor("downstairs", self.roomLi)
        self.roomA.createDoor("hatch", self.roomK, True, self.roomC)

    def play(self):
        """
        Handles the core gameplay loop: while not finished, the loop will request inputs from the player and process
        them through the 'runAction' method, which then assigns further handling of these actions to their
        respective methods (e.g. 'MENU' hands off to 'doMenuAction'.) Once game finished state has been set to 'True',
        the outro text is displayed in the UI and closing GUI window is opened.
        """

        finished = False  # Determines whether below gameplay loop should repeat or not
        gameWon = False   # Determines whether player won or quit game

        # Core gameplay loop:
        while not finished:
            finished = self.runAction(self.prepareInput())  # Input requested from player and processed by 'runAction'

            if self.currentRoom == self.exitRoom:  # If exit room reached, both the 'finished' and 'gameWon' variables
                finished = True                    # are set to True, ending the gameplay loop and displaying outro
                gameWon = True                     # text in UI.

        # Outro text - these string arguments may be changed as the user sees fit (see Text module documentation for
        # help on how to input arguments.)
        self.story.outroText(
            "\nThe sun rises, and you successfully escaped the building.",
            "#",
            "As the morning breeze cools your face, the world now feeling more\n"
            "open than ever, you take one final glimpse over your shoulder and head\n"
            "for home.",
            winCheck=gameWon
        )
        self.createGUI()

    @staticmethod
    def prepareInput():
        """
        This method receives player keyboard inputs and prepares them for use within 'runAction'.

        :return: tuple
        """
        actionInput1 = None
        actionInput2 = None
        inputLine = input("> ")  # Input received from player
        if inputLine != "":      # Checks if input is empty, returning 'None' if so
            allWords = inputLine.split()            # Input split at blank-space and assigned to 'allWords', where only
            actionInput1 = allWords[0].upper()      # first two elements from this list are then returned.
            if len(allWords) > 1:
                actionInput2 = allWords[1].upper()
            else:
                actionInput2 = None

        return actionInput1, actionInput2  # Processed inputs returned

    def runAction(self, action):
        """
        Handles prior processing of inputs received by 'prepareInput' within 'play' method, then assigning latter
        processing as necessary. Returns 'wantToQuit' boolean variable once action processed, informing 'play' whether
        game's end has been reached or not.
        (For more information on how each of the below methods act, please refer to their respective class
        documentation.)

        :param action:
        """

        actionWord, direction = action
        wantToQuit = False  # Determines whether main gameplay loop should terminate

        if actionWord == "GO":
            self.doGoAction(direction)  # Hands off to 'doGoAction' class method to be processed further

        elif actionWord == "INTERACT":
            self.doInteractAction()  # Hands off to interact gameplay loop

        elif actionWord == "INSPECT":
            self.currentRoom.getInfo()  # Calls information on current room through 'getInfo' method (see Room Class)

        elif actionWord == "INVENTORY":   # Calls status of player's inventory through 'checkInventory' method
            self.player.checkInventory()  # (see Player Class)

        elif actionWord == "HINT":
            self.currentRoom.hint(self.player)  # Calls all available hints through 'hint' method (see Room Class)

        elif actionWord == "MENU":
            self.doMenuAction()  # Hands off to 'doMenuAction' class method to be processed further

        elif actionWord == "QUIT":  # Manually quits game
            wantToQuit = True

        else:  # Informs player that invalid input received and of all valid action words
            print("[You have not entered a valid action word. Enter 'MENU' to see all available actions.]")

        return wantToQuit  # Returns boolean expression; informs core gameplay loop whether to terminate or not

    def doGoAction(self, direction: str):
        """
        Moves player from 'currentRoom' environment to 'nextRoom', checking first if doorway being accessed is locked
        or exists through 'checkExit' method from Rooms class. If any change occurs, player is updated through UI.

        :param direction: str
        """

        unlocked = True
        exit = self.currentRoom.checkExit(direction, self.player)
        if exit == unlocked:
            self.currentRoom = self.currentRoom.doors[direction]  # Updates current room to the given directions room
            print("You have entered the %s." % self.currentRoom.description)  # Confirms change of room in user UI

    def doMenuAction(self):
        """
        Informing player of available actions. If no interactions are available, 'INTERACT' not displayed in actions
        list.
        """

        print("[You may enter the following action words:]")
        if len(self.currentRoom.items) != 0 or self.currentRoom.roomNo in Room.storageRooms:
            self.actions.insert(1, 'INTERACT')
            print(self.actions)
            self.actions.remove('INTERACT')
        else:
            print(self.actions)

    def doInteractAction(self):
        """
        Responsible for handling all player interactions, primarily the interaction gameplay loop within this method.
        If the player inputs 'INTERACT" at a valid point of the game, this method runs and allows the player various
        different interactions: access of room storage boxes, in which they can check their storage, store and retrieve
        items, take items from rooms or 'PASS' to continue otherwise.
        """

        interactions = ['PASS']  # Base interaction options - 'PASS' is always a valid interaction

        if self.currentRoom.roomNo in Room.storageRooms:  # Checks if current room is listed as a storage room
            print("This room contains a storage box. [Enter 'OPEN' to access.]\n")
            interactions.insert(0, 'OPEN')  # Allows player to access storage
        if len(self.currentRoom.items) != 0:  # Checks if room contains any items
            interactions.insert(0, 'TAKE')  # Allows player to pick up items
        if len(interactions) == 1:
            print("There is nothing to interact with.")
            return None

        finished = False  # Determines whether gameplay loop should terminate

        # Interaction gameplay loop:
        while not finished:
            print("[Your available interactions are:]")  # Informs player of available valid actions
            print(interactions)
            actionWord, index = self.prepareInput()  # Processes user inputs
            if actionWord not in interactions:
                print("[Please enter a valid interaction word.]\n")
                continue

            if actionWord == "TAKE":  # Handles taking of items from rooms
                self.player.collectItem(self.currentRoom.items[0], self.currentRoom)

            elif actionWord == "OPEN":  # Opens storage box, then updating available interactions
                print("Storage opened.\n")
                interactions = ['CHECK', 'RETRIEVE', 'STORE', 'CLOSE']
                continue

            # Following three interactions are only available once a storage box has been opened
            elif actionWord == "CHECK":     # Informs player of storage status
                self.player.checkStorage()
                continue

            elif actionWord == "RETRIEVE":  # Enables player to retrieve stored items
                self.player.retrieveItem(self.currentRoom)
                continue

            elif actionWord == "STORE":  # Enables player to store held items
                self.player.storeItem(self.currentRoom)
                continue

            elif actionWord == "CLOSE":  # Closes storage box, ending interaction gameplay loop
                print("Storage closed.")

            elif actionWord == "PASS":  # Ends interaction gameplay loop
                pass

            finished = True  # Tells 'while' loop to terminate


def main():
    """Instantiates the game and begins play"""

    game = Game()
    game.play()


if __name__ == "__main__":
    main()
