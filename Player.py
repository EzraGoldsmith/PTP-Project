class Player:
    """
    This class serves to handle any aspects of player's interaction with the game elements. Upon being initialised,
    the player is assigned inventory and storage attributes, these both being empty lists to track and items found and
    where they are stored.
    The 'collectItem' method handles collection of item from rooms, while 'checkInventory' and 'checkStorage' inform
    the player what condition their inventory or storage is in, respectively.
    'storeItem' and 'retrieveItem' act as storing and retrieving gameplay loops, resp., if necessary conditions are met
    for their application.
    """

    def __init__(self):
        """
        Initialises the class, setting the player's inventory and storage as empty lists for later use.
        """

        self.inventory = []
        self.storageBox = []

    def collectItem(self, item: str, room: object):
        """
        Handles the collect of items from rooms by the player. The first argument, 'item', goes through 2 checks before
        being added to the player's inventory: existence within 'room', and availability of space since the player
        can carry at most 3 items at one time.

        :param item: str
        :param room: Room object
        """
        if item in room.items:
            if len(self.inventory) >= 3:
                print("Inventory full.")
            else:
                room.items.remove(item)      # Item is removed from room via 'pop()' method and moved
                self.inventory.append(item)  # to player inventory.
                print("Collected %s." % item)
        else:
            print("Item not in room.")

    def storeItem(self, room):
        """
        Handles the storage of items from player's inventory to a room's storage box. Acts further as a nested
        gameplay loop: requests player keyboard input, checks whether input is valid, then either carries out
        command or returns an error message until an input is valid. To avoid an infinite loop, 'PASS' command is
        included so that the loop can be terminated at any input opportunity.

        :param room:
        """

        # First two conditional statements check whether action can be carried out by user, i.e. if there are items to
        # store or a storage box within the current room. None returned for either option so that following code is
        # never reached, returning to interaction gameplay loop.

        if len(self.inventory) == 0:                # Checks whether inventory attribute is empty
            print("You carry nothing to store.\n")  # Informs player of error
            return None
        if room.roomNo not in room.storageRooms:    # Checks whether room is listed under storageRooms global attribute
            print("Room has no storage box.\n")     # informs player of error
            return None

        finished = False
        print("[Enter the index of the item you wish to store, or 'PASS'.]")  # Informs player of valid inputs
        print("[e.g. For %s, enter '1'.]\n" % self.inventory[0])              # Provides example of valid input

        # Storing gameplay loop:
        while not finished:
            self.checkInventory()           # Informs player of inventory status through UI
            interactionInput = input("> ")  # Receives player keyboard input

            if interactionInput.isnumeric():
                itemNo = int(interactionInput)
                if itemNo in range(1, len(self.inventory) + 1):
                    item = self.inventory.pop(itemNo - 1)  # As with 'collectItem' procedure, item is removed
                    self.storageBox.append(item)           # from inventory and appended to storageBox list.
                    print("%s stored.\n" % item)
                else:
                    print("Item index out of range. [Enter another or 'PASS'.]\n")
                    continue

            elif interactionInput == "PASS":  # Terminates gameplay loop
                pass

            else:
                print("[Please enter a valid item index, or 'PASS'.]\n")  # Valid input not entered, so loop repeats
                continue

            finished = True  # If reached, loop terminates

    def retrieveItem(self, room):
        """
        Method has inverse use of 'storeItem', being of identical structure but with reverse effect by moving items
        from storage to player's inventory. The size limit of this is also accounted for, so that no more than 3 items
        can be held by the player at one time.

        :param room:
        """

        # First three conditional statements check if action is valid, by assessing existence of retrievable items,
        # whether room has a storage box, or if inventory is full and cannot hold more items. If any are True under
        # current conditions, retrieval gameplay loop never reached and returns to interaction gameplay loop.

        if len(self.storageBox) == 0:                        # Checks if storage empty
            print("You have nothing stored to retrieve.\n")  # Informs player of error in UI
            return None
        if room.roomNo not in room.storageRooms:  # Checks if room contains storage box
            print("Room has no storage box.\n")   # Informs player of error
            return None
        if len(self.inventory) >= 3:                                                 # Checks if inventory full
            print("Inventory is full. Deposit some items in a nearby storage box.")  # Informs player of error
            print("[Items with no further use are labelled '(used)'.]\n")
            return None

        finished = False
        print("[Enter the index of the item you wish to retrieve, or 'PASS'.]")
        print("[e.g. For %s, enter '1'.]\n" % self.storageBox[0])

        # Retrieval gameplay loop:
        while not finished:
            self.checkStorage()             # Informs player of storage status through UI
            interactionInput = input("> ")  # Receives player keyboard input

            if interactionInput.isnumeric():
                itemNo = int(interactionInput)
                if itemNo in range(1, len(self.storageBox) + 1):  # Checks if index is valid
                    item = self.storageBox.pop(itemNo - 1)
                    self.inventory.append(item)
                    print("You retrieved %s.\n" % item)
                else:
                    print("Item index out of range. [Enter another, or 'PASS'.]\n")
                    continue

            elif interactionInput == "PASS":  # Terminates gameplay loop
                pass

            else:
                print("[Please enter a valid item index, or 'PASS'.]\n")
                continue

            finished = True  # If reached, retrieval gameplay loop terminates

    def checkInventory(self):
        """
        Informs the player of what items are currently stored in their inventory, if any, by returning relevant
        information in UI.
        """

        if len(self.inventory) == 0:           # Checks if inventory is empty
            print("Your inventory is empty.")  # Informs player through UI
        else:
            print("You are holding the following items:")  # If not empty, prints list of stored items
            print(self.inventory)

    def checkStorage(self):
        """
        Informs the player of what items are currently stored in their storage, if any, by returning relevant
        information in UI.
        """

        if len(self.storageBox) == 0:          # Checks if storage is empty
            print("Your storage is empty.\n")  # Informs player through UI
        else:
            print("You have the following items stored:")  # If not empty, prints list of stored items
            print(self.storageBox)
