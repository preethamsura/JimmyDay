""" Player class which represents a player playing snake. """

# Necessary imports
import pygame
from Pong import Pong

class Player():
    """ A class which allows the player to play the snake game
    that is passed in using arrow keys or wasd."""
    def __init__(self, screenProps):
        self.screenProps = screenProps
        self.game = Pong.Pong()

    """ Creates a game where a player can play snake. """
    def playGame(self):
        # Whether or not the player won
        winning = self.game.startGame()

        # Resetting the screen size.
        self.screenProps["screen"] = pygame.display.set_mode([self.screenProps["windowWidth"], self.screenProps["windowHeight"]])

        return winning