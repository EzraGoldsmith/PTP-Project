import tkinter as tk
from tkinter import TOP, RIGHT, BOTTOM
from PIL import ImageTk, Image


class App:
    """
    This application class handles all functionality concerning the game GUI, notably its instantiation, formatting,
    attributes and features. Its 'prepareImg' and 'updateImg' methods handle the process of updating the displayed
    images (through the 'refresh' method).
    This class need be instanced only once by the user within the Game class '__init__' method, displaying then the
    cover image and allowing the player access to the 'CONTINUE' button - this begins executing the main game
    in the player's IDE.
    """

    def __init__(self, root):
        """
        Initialises application, taking Tkinter window as 'root' argument, on which any frames are packed.
        'imgFrame' attribute is the frame responsible for displaying any images as directed by the user (notably
        those linked with each room from the Game class).

        As commented below, various frame formatting options should be changed as the user desires, to best fit your
        game's vision.

        :param root: Tkinter Tk() Class
        """

        self.imgFrame = tk.Frame(root, width=350, height=350, bg='GRAY10')  # Creates room image frame
        self.imgFrame.pack_propagate(0)                                     # Prevents resizing
        self.imgFrame.pack(side=RIGHT)                                      # Frame packed into window, on right side

        # Once frame created, Tkinter label packed with 'coverImg' image to display when GUI is instanced.
        self.coverImg = ImageTk.PhotoImage(Image.open('images/Exterior.jpeg').resize((350, 300), Image.ANTIALIAS))
        self.currentRoomImg = tk.Label(self.imgFrame, image=self.coverImg, bg="GRAY10")
        self.currentRoomImg.pack(side=TOP)

        self.contButton = tk.Button(
            self.imgFrame,
            text='The end(?)',
            font=("Gothic MS", 20),
            command=root.destroy,
            width=12,
            height=4,
            fg='GRAY10',
            activeforeground='RED',
            relief='sunken'
        )
        self.contButton.pack(side=BOTTOM)

        # Following frame and widgets ultimately scrapped due to time limitations, but would would serve to display
        # any relevant Narrative or error-message text. If implemented, window dimensions required to be 800x350.

        # self.roomName = tk.Label(     # Tkinter label responsible for displaying the current room's name (i.e.
        #     self.imgFrame,            # 'description' argument with instancing the Room class.)
        #     text="",
        #     bg="GRAY10",              # Formatted such that white text distinguishable upon gray background.
        #     fg="WHITE",               # ('bg', 'gf' and 'font' parameters editable - see '__init__' documentation.)
        #     font=("Gothic MS", 20)
        # )
        # self.roomName.pack(side=TOP)  # Packs label onto image frame

        # self.printFrame = tk.Frame(root, width=450, height=350, bg='GRAY10')
        # self.printFrame.pack_propagate(0)
        # self.printFrame.pack(side=LEFT)

        # self.display = tk.Label(
        #     self.printFrame,
        #     text="",
        #     fg='WHITE',
        #     font=("Gothic MS", 12),
        #     height=25,
        #     width=50,
        #     bg='GRAY20'
        # )
        # self.display.pack(padx=20, pady=20)

    @staticmethod
    def prepareImg(image: str):
        """
        Each image must fit the dimensions of the image frame as part of the overall application, and so
        needs to be resized and prepared for configuring under 'updateImg' method.

        :param image: str
        """
        inputImg = Image.open(image)                # Inputted image opened in usable format
        preparedImg = ImageTk.PhotoImage(inputImg)  # Image prepared for use within Tkinter 'configure' Frame method
        return preparedImg                          # Item returned for use within 'updateImg' class method

    def updateImg(self, game: object):
        """
        As the main gameplay loop refreshes, i.e. through the Game class' 'play' method, this would update
        the current room's image within the GUI. Alongside other class methods, such as 'updateText' method,
        which were never designed nor implemented, would act within 'refresh' method.

        :param game: object
        """

        img = self.prepareImg(game.currentRoom.roomImg)  # Prepares image for updating through 'prepareImg' method
        self.currentRoomImg.configure(image=img)         # Configures new image for current room, displaying in GUI

    def refresh(self, game: object):
        """
        Responsible for refreshing GUI with relevant media, including the current room's associated image and any
        text. Would also update drop-box items with those from Game's 'self.actions' or 'interactions' lists,
        executing the selected option.

        :param game: object
        """

        self.updateImg(game)     # Updates GUI image
        # self.updateText(game)  # Would update GUI displayed text within 'printFrame' Tkinter frame

def main():
    window = tk.Tk()                # Main application window created as base for additional widgets
    window.title("title")           # Window title set
    window.geometry("350x350")      # Dimensions of window set
    window.resizable(False, False)  # Neither x nor y dimensions resizable

    myApp = App(window)  # GUI frame created and attached to window
    window.mainloop()    # Calls GUI mainloop


if __name__ == "__main__":
    main()