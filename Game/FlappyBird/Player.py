""" Player class which represents a player playing snake. """

# Necessary imports
import pygame
from FlappyBird import flappy

class Player():
    """ A class which allows the player to play the snake game
    that is passed in using arrow keys or wasd."""
    def __init__(self, screenProps):
        self.screenProps = screenProps
        self.winningScore = 10

    """ Creates a game where a player can play snake. """
    def playGame(self):
        self.game = flappy.Flappy(self.screenProps)

        self.movementInfo = self.game.showWelcomeAnimation()
        self.crashInfo = self.game.mainGame(self.movementInfo)
        score = self.game.showGameOverScreen(self.crashInfo)

        # Resetting the screen size.
        self.screenProps["screen"] = pygame.display.set_mode([self.screenProps["windowWidth"], self.screenProps["windowHeight"]])

        return score >= self.winningScore