""" Class which is going to represent the board game."""

import pygame
from random import randint

class BoardGame():

    """ Creates a new board and starts the game."""
    def __init__(self, screenProps):
        #Assigns useful values to passed in parameter
        self.screenProps = screenProps
        self.colors = screenProps["colors"]

        # Define dimensions for board and creates a new board 
        # with randomized game squares
        self.spaces, self.rows, self.cols = (50, 10, 5)
        self.resetBoard()

        # Default starting positions and starting scores. 
        self.playerPos = 0
        self.computerPos = 0
        self.computerScore = 0
        self.playerScore = 0

        # Start the game
        #self.playGame()

    """ Will update the display to represent the current state of the board which
    includes where the game squares are located and locations of both players."""
    def updateDisplay(self):
        # do stuff which will update the display
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
        if (self.checkGameSpace(self.computerPos)):


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