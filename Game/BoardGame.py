""" Class which is going to represent the board game."""

import pygame
from random import randint

class BoardGame():

    """ Creates a new board and starts the game."""
    def __init__(self, screenProps):
        # Assigns useful values to passed in parameter
        self.screenProps = screenProps
        self.screen = screenProps["screen"]
        self.colors = screenProps["colors"]
        self.fonts = screenProps["fonts"]
        self.fonts["boardFont"] = pygame.font.Font('freesansbold.ttf', 35)
        self.boardSquareLength = 100

        # Assigns scores which players receive for certain events. 
        self.winMiniGameScore = 3
        self.reachEndFirstScore = 9

        # Define dimensions for board and creates a new board 
        # with randomized game squares
        self.spaces, self.rows, self.cols = (50, 10, 5)
        self.resetBoard()

        # Default starting positions and starting scores. 
        self.playerPos = 0
        self.computerPos = 0
        self.computerScore = 0
        self.playerScore = 0

        # Displays the initial starting state of the game. 
        self.updateDisplay()

        # Start the game
        self.playGame()

    """ Will update the display to represent the current state of the board which
    includes where the game squares are located and locations of both players."""
    def updateDisplay(self):
        # Wipe the screen of whatever was there beforehand.
        self.screen.fill(self.colors["white"])

        self.displayBoard()
        self.displayPieces()
        self.displayScores()

        pygame.display.update()

        # Variable which keeps track of whether or not the intro should still be running.
        intro = True

        # Loops until the play button is clicked.
        while intro:
            events = pygame.event.get()
            for event in events:
                # Event for a mouseclick.
                if event.type == pygame.MOUSEBUTTONUP:
                    click = pygame.mouse.get_pos()

                # This is ran if the the window is closed. It closes the window and terminates the program.
                elif event.type == pygame.QUIT:
                    intro = False
                    pygame.quit()

        return False

    """ Displays the board (top down). Special game squares will be indicated by a number of a different color from
    the rest of the board numbers (which will be of the same background color as the board)."""
    def displayBoard(self):
        for i in range(len(self.board)):
            # Indices for that board square. 
            xval = i % 10 * self.boardSquareLength + 100
            yval = i // 10 * self.boardSquareLength + 300

            # For all the squares in the board, display the number which represents that square. 
            # Colors the number of the square a different color if that square is a game square. 
            if (self.board[i]):
                numberText = self.fonts["boardFont"].render(str(i + 1), True, self.colors["black"], self.colors["green"])
            else:
                numberText = self.fonts["boardFont"].render(str(i + 1), True, self.colors["black"], self.colors["white"])
            numberTextRect = numberText.get_rect()
            numberTextRect.center = (xval, yval)
            self.screen.blit(numberText, numberTextRect)

            # Draw a rectangle around the squares on the board. 
            pygame.draw.rect(self.screen, self.colors["black"], (xval - 20, yval - 20, self.boardSquareLength, self.boardSquareLength), 5)


    """ FIX ME"""
    def displayPieces(self):
        return False

    """ FIX ME"""
    def displayScores(self):
        return False

    """ Creates a new board variable which has 50 spaces. Board will
    have randomized game squares every 2 to 5 squares. Item in board will be True
    if the square is a game square or the item will be empty (or false) if the 
    square is a default square type. """
    def resetBoard(self):
        # Create the board
        self.board = [0] * self.spaces

        # Randomly insert game squares every 2 to 5 points.
        i = randint(1, 4)
        while (i < self.spaces - 1):
            self.board[i] = 1
            randomNum = randint(2, 5)
            i += randomNum


    """ Starts a game where the player plays against the computer."""
    def playGame(self):
        # Keeps the game running until game over. 
        while (True):
            # Makes a player move.
            self.makePlayerMove()
            # Stops making moves if the player reached the end. 
            if (self.checkGameEnd()):
                break

            # Makes a computer move. 
            self.makeComputerMove()
            # Stops making moves if the computer reached the end. 
            if (self.checkGameEnd()):
                break

    """ FIX ME"""
    def makePlayerMove(self):
        return False
        
    """ FIX ME"""
    def makeComputerMove(self):
        # Adds to computer square.
        self.computerPos += self.rollDice()

        # Checks to see if the computer should play a "minigame." 
        # Computer has a 50-50 chance of winning the minigame. 
        if (self.checkGameSpace(self.computerPos)):
            self.playComputerGame()

    """ Randomly decides whether or not the computer 'won' a minigame
    that it played and adds to the computer score. """
    def playComputerGame(self):
        self.computerScore += randint(0, 1) * self.winMiniGameScore

    """ Returns whether or not the space that was landed on is a game square."""
    def checkGameSpace(self, position):
        return position < 49 and self.board[position]

    """ Returns a random number between 1 and 6 (inclusive). """
    def rollDice(self):
        return randint(1, 6)

    """ Returns true if there is a winner (either computer or player). """
    def checkGameEnd(self):
        return self.playerPos >= 49 or self.computerPos >= 49

    """ Returns true if it was the player won the game. Returns false if the
    computer won the game or there was a tie. """
    def didPlayerWin(self):
        return self.playerScore > self.computerScore