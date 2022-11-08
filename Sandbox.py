"""
class Super:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def exMethod(self, var_):
        print(f'{self.name} is {self.age}')
        print(var_)


class Sub(Super):
    def __init__(self, name, age, height):
        self.height = height
        super().__init__(name, age)


def main():
    test = Sub("Ezra", 22, 195)
    test.exMethod("text")

if __name__ == "__main__":
    main()

# Sub is the general case, but can be overridden with special qualities using Super
# https://www.w3schools.com/python/python_inheritance.asp
"""

import tkinter as tk
from tkinter import messagebox
from tkinter import TOP, BOTH, LEFT, RIGHT, BOTTOM
from PIL import ImageTk, Image
from Game import Game


class App:
    """
    Responsible for creating frame for the game application which handles all major GUI responsibilities, such as...
    """

    def __init__(self, root):
        """Initialises application, """

        self.backgroundImg = ImageTk.PhotoImage(Image.open('images/Library.jpg'))

        self.roomImageFrame = tk.Frame(root, width=350, height=350, bg='GRAY10')  # Creates room image frame
        self.roomImageFrame.pack_propagate(0)  # Prevents resizing
        self.roomImageFrame.pack()             # ...

        self.roomImg = ImageTk.PhotoImage(Image.open('images/Storage Room.jpeg').resize((350, 300), Image.ANTIALIAS))
        self.roomImage = tk.Label(self.roomImageFrame, image=self.roomImg, bg="GRAY10")
        self.roomImage.pack(side=TOP)

        self.roomName = tk.Label(
            self.roomImageFrame, text="Storage room", bg="GRAY10", fg="WHITE", font=("Gothic MS", 20)
        )
        self.roomName.pack(side=TOP)


window = tk.Tk()                # Main application window created as base for additional widgets
window.title("title")        # Window title set, taking 'Game' class' title attribute as argument
window.geometry("700x350")      # Sets dimensions of window
window.resizable(False, False)  # Neither x nor y dimensions resizable

myApp = App(window)  # GUI frame created and attached to window
window.mainloop()    # Calls GUI mainloop
