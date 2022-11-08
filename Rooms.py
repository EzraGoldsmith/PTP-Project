class Room:
    """
    This class allows for a room to be instanced with its own unique items, descriptions, features and
    accessibility to other rooms. It has no connections to begin with, these being added via the 'createDoor' class
    method, which is done within the 'Game' class.

    Upon being instantiated, object is given the 'description', 'wordDescription' and 'writtenHint' attributes,
    the latter two being optional if the user wishes to provide more narrative-centered detail for the room or
    a hint on how to interact with it (any additional text should be included at the users discretion.)

    The 'storeRoom' option determines whether the player can store items in this room, and must be considered
    when avoiding soft-locks. The global attributes 'roomNo' and 'storageRooms' allow for unique room numbers to be
    assigned when an object is instanced and a record of all storage rooms to be kept, while 'allDirections' stores
    all direction options added by the user - these are used when catching typo errors.
    """

    roomNo = 1
    storageRooms = []
    allDirections = []

    def __init__(self, roomImage: str, description: str, wordDescription="", writtenHint="", storeroom=False):
        """
        Initialises the class, creating a room.

        :param description:
        :param wordDescription:
        :param writtenHint:
        :param storeroom:
        """

        self.doors = {}  # Contains (direction, room) dictionary pairs for each door and its corresponding room
        self.locks = {}  # Tracks which doors are locked, from the side of current room to the one connected
        self.keys = {}   # Tracks the required keys for the above locks
        self.items = []  # List of all items obtainable from a room

        self.roomImg = roomImage
        self.description = description
        self.wordDescription = wordDescription
        self.writtenHint = writtenHint

        self.roomNo = Room.roomNo
        Room.roomNo += 1
        if storeroom:
            Room.storageRooms.append(self.roomNo)  # If desired, adds room to list of all storage rooms

    def addItems(self, *allItems: str):
        """
        Used to add as many items to a rooms 'item' attribute as desired. (Should be called upon alongside 'createDoor'
        method to assign all required attributes efficiently.)

        :param allItems: str
        """

        self.items.extend([item for item in allItems])

    def getInfo(self):
        """
        Used to retrieve room details, 'wordDescription' text and number of doorways, when called upon.
        """

        if self.wordDescription != "":
            print(self.wordDescription)
            print("")

        if len(self.items) != 0:
            print("A faint glimmer can be spotted across the room...\n")

        allDoors = self.doors.keys()  # Creates list object whose elements are each of the rooms door directions
        if len(allDoors) == 1:
            print("Just 1 door is found upon its walls.\n")
        else:
            print("%s doors line its walls.\n" % len(allDoors))
        print("[Your available directions are:]")
        print(list(allDoors))

    def createDoor(self, direction: str, connectedRoom: object, locked=False, keyRoom=None):
        """
        Creates a door which connects the current room to the provided 'connectedRoom', with the option for this
        doorway to be locked (only in assigned direction, as access from side of connected room can be assigned without
        a lock, if desired by user.) If locked, the user may also assign a corresponding key room, 'keyRoom', where the
        key for this door is found.

        :param direction:
        :param connectedRoom:
        :param locked:
        :param keyRoom:
        """

        if direction.upper() not in Room.allDirections:   # Checks whether this direction option has already been logged
            Room.allDirections.append(direction.upper())  # If not logged, it is added to allDirections

        direction = direction.upper()
        self.doors[direction] = connectedRoom

        if locked:
            self.locks[direction] = connectedRoom  # (direction, connectedRoom) pairing is added to 'locks' attribute
            self.keys[direction] = connectedRoom.description + " key"  # Creates key for lock and adds to 'keys'
            if keyRoom is not None:
                keyRoom.items.append(self.keys[direction])  # If desired, adds the key to a specified room, 'keyRoom'

    def unlockDoor(self, direction: str, player: object) -> bool:
        """
        For use within the 'checkExit' class method.

        Checks whether the player has the key to a given doorway, removing the lock if so and returning the connected
        room's corresponding object, otherwise informing them that they currently do not possess the required key and
        returns False boolean algebraic object.
        Note that when a door in unlocked, this only removes the lock from the current side of the door, as to allow
        1-sided locks.

        :param direction: str
        :param player: object
        """

        if self.keys[direction] in player.inventory:
            del self.locks[direction]     # Lock is removed so that player can access room and key no longer needed
            player.inventory.remove(self.keys[direction])
            player.inventory.append(self.keys[direction] + " (used)")
            # String corresponding to door key is extended with the string ' (used)' for better player quality-of-life.
            # This also corrects for possible UI errors when player calls 'HINT' action, as now the original key string
            # is no longer in the players inventory list.
            print("The way has been unlocked.")
            return True
        else:
            print("The way to the %s is locked." % self.doors[direction].description)
            print("The correct key for this passage is not in your inventory.")
            return False

    def checkExit(self, direction: str, player: object):
        """
        Checks if the corresponding door for a given direction exists or is locked, the returned value depending upon
        these conditions. If the given direction does not connect to an instanced room, then None is returned for use
        within the 'Main' class.
        A check is made initially for any typos by comparing the inputted direction against those listed in
        'allDirections'. If caught, an error message is printed in the UI.

        :param direction: str
        :param player: object
        """

        if direction in Room.allDirections:
            if direction in self.locks:                    # checks if door is locked, any following checks carried
                return self.unlockDoor(direction, player)  # out by 'unlockDoor' method if so
            elif direction in self.doors:
                return True
            else:                                          # If door does not exist, error message shown in UI
                print("No such doorway exists! Try inspecting the room.")
        else:  # If direction not listed under 'allDirections', clause reached and error message shown in UI
            print("[Direction not registered. Please check for typos or try another.]")

    def hint(self, player):
        """
        Responsible for providing the player with any hints when called upon.
        """

        if self.writtenHint != "":   # Checks if written hint included by user
            print(self.writtenHint + "\n")

        if len(self.items) != 0:     # Checks if any items remain in the current room, informing user or result in UI
            print("You have not obtained every item in this room. [Enter 'INTERACT'.]")
        else:
            print("No more items remain in this room.")

        allPlayerInventory = set(player.inventory)  # Copy of player inventory as a set
        allPlayerStorage = set(player.storageBox)
        allKeys = set()                         # Base empty set variable
        for k in list(self.keys):               # Iterates over all dictionary keys from 'keys' attribute
            allKeys.add(self.keys[k])           # Value corresponding to dictionary key 'k' added to 'allKeys' set

        if len(player.inventory) != 0:
            if allPlayerInventory & allKeys != set():  # Determines whether intersection of sets is empty
                print("\nA useful object weighs on your pocket. \n"
                      "Perhaps it's of use here? [Check your inventory.]")
            if allPlayerStorage & allKeys != set():
                print("\nYou recall having found a suitable key before. \n"
                      "[Find and check a storage box.]")
