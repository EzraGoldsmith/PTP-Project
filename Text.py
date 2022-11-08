from typing import List  # Allows for type hinting annotation


class Text:
    """
    Responsible for providing structure for any (narrative-centered) text that appears on UI, such as basic text boxes,
    interactive checks, and intro/outro texts (sub classes of this class.) Both static methods, 'prepareText' and
    'printText' are designed to prepare and print text within the UI while allowing the user a greater level of
    formatting control than through 'print()' function alone.
    """

    @staticmethod
    def prepareText(*lines: str, includeCheck=False) -> List[str]:
        """
        Takes in as many lines of text, *line: str, as the user inputs (a newline can be set manually by the user
        via the syntax "\n" at place of break), and returns a list which can be printed using the 'printText'
        method. The, includeCheck: bool, argument determines whether the check section is included when printing.
        """

        textReady = []
        for line in lines:
            textReady.extend(line.split("\n"))  # Separates sentence into designated sections and adds to return
            textReady.append("")                # Adds a blank line, separating from following sentence
        if includeCheck:
            textReady[-1] = " "                 # Acts as a key within the 'printText' module if check wanted
        return textReady

    @staticmethod
    def printText(*textboxes: List[str]):
        """Takes each text box prepared for printing using the 'textBox' method and prints them."""

        for textbox in textboxes:   # Allows many prepared texts to be printed simultaneously, without needing to
            for line in textbox:    # call the method multiple times.
                print(line)         # Prints text as outlined by user.
            if textbox[-1] == " ":  # Checks whether user included check section, continues if True.
                checked = False
                print("[Press the Enter key to continue.]")
                while not checked:
                    if input("> ").upper() == "":
                        checked = True
                    else:
                        print("[Invalid entry, please press the Enter key to continue.]")


class Narrative(Text):
    """
    Designed so that, upon being instanced in the 'Main' module, the intro is executed and game narrative made
    accessible. The user may input and display through the UI any given text (using the inherited 'prepareText' and
    'printText' methods from the super class 'Text') by calling the 'storyText' class method.
    """

    def __init__(self, *introLines: str, title="my game", exit="exit"):
        """
        Takes each 'introSection' and assigns them to the 'allIntroLines' class attribute for use within 'introText',
        which is then executed. Here the syntax "#" is used to denote when an enter check is to be included by the user.

        :param introLine: str
        """

        self.introLines = *(line for line in introLines),  # Tuple comprehension for necessary data type in line.88
        self.introText(title, exit)  # Displays the intro text in the UI, as instructed by the user

    def introText(self, title: str, exit: str):
        """
        Runs the 'allIntroLines' attribute through 'storyText' method, which then displays them in the UI as formatted
        by the user (additional borders can be included which automatically change size depending on how the user
        formats the introParagraph argument.)

        :param title: str
        :param exit: str
        :return:
        """

        introParagraph = self.prepareText(
            "Welcome to %s, a word-based adventure game, where your goal\n"
            "is to explore each room, uncover their secrets, reach the %s and escape." % (title, exit),
            "To navigate the area, enter 'GO' along with the direction you want to travel\n"
            "in the space below (e.g. 'GO EAST'.)",
            "If you ever get stuck, enter the action word 'MENU' to see all available\n"
            "actions, or 'HINT' for some extra help.",
            "Good luck!",
            includeCheck=True
        )

        borderBase = ""
        borderLength = max([len(line) for line in introParagraph])  # Finds maximum length out of each line
        for i in range(borderLength):
            borderBase += "="                                       # Increases border length to equal introParagraph
        border = self.prepareText(borderBase)                       # Prepares border for use within printText method

        self.printText(border, introParagraph, border)  # Displays introParagraph & borders in UI

        self.storyText(*self.introLines)  # Displays introduction narrative & tip in UI.
        print("[Use your available actions to search the area.]")

    def storyText(self, *storyLines: str):
        """
        Responsible for presenting all narrative text in the UI, with the option to include a player check (off by
        default.) Enter "#" as an argument after any line the user wishes to include an enter check.

        :param storyLines: str
        :return:
        """

        storySegments = []
        segment = []
        checkIncluded = False

        for line in storyLines:
            if line != "#":
                segment.append(line)                               # Adds line to story segment
                if storyLines.index(line) == len(storyLines) - 1:  # Checks if line is closing line from final segment
                    pass                    # If closing line, final segment completed and added to storySegments list
                else:
                    continue                # Otherwise, line added to current segment and next line checked
            else:
                checkIncluded = True        # Includes enter check when prepared for print
            storySegments.append(self.prepareText(*tuple(segment), includeCheck=checkIncluded))
            segment = []           # Variable reset for following segment, if needed
            checkIncluded = False  # Variable reset for following segment, if needed (assumes no enter check)

        self.printText(*tuple(storySegments))  # Changes 'storySegments' data type into tuple for use as argument, then
                                               # prints through 'printText' method.

    def outroText(self, *outroLines, winCheck=False):
        """
        :param winCheck:
        """

        if winCheck:                     # Under condition that game is won instead of quit via 'QUIT' action, bonus
            self.storyText(*outroLines)  # story text is presented in UI

        outroParagraph = self.prepareText(
            "Thank you for playing!",
            "If you'd like to play again, why not see if you can win in under X?"
        )
        self.printText(outroParagraph)
