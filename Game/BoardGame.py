""" Class which holds is going to represent the board game."""

import pygame

class BoardGame():

    """ Creates a new board and starts the game."""
    def __init__(self, screenProps):
        #Assigns useful values to passed in parameter
        self.screenProps = screenProps
        self.colors = screenProps["colors"]

        # Creates a new board with randomized game squares
        self.resetBoard()

        # Default starting positions
        self.playerPos = 1
        self.computerPos = 1

        # Start the game
        self.startGame()

    """ Will update the display to represent the current state of the board"""
    def updateDisplay(self):
        # do stuff which will update the display
        return False

    """ Creates a new board variable which has 50 spaces. Board will
    have randomized game squares every 2 to 5 squares. Item in board will be True
    if the square is a game square or the item will be empty (or false) if the 
    square is a default square type. """
    def resetBoard(self):
        # Create the board
        self.spaces, self.rows, self.cols = (50, 10, 5)
        self.board = [0] * self.spaces
        return False


    """ FIX ME"""
    def startGame(self):
        return False

    """ Returns a random number between 1 and 6 (inclusive). """
    def rollDice(self):
        return False