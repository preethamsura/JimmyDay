""" Player class which represents a player playing tag. """

# Necessary imports
import pygame
from Tag import Tag

class Player():
    """ A class which allows the player to play the tag game
    that is passed in using arrow keys or wasd."""
    def __init__(self, screenProps):
        self.game = Tag.Tag(screenProps)
        self.playGame()

    """ Creates a game where a player can play tag. """
    def playGame(self):
        # Start the game and run it till it is over. 
        self.game.startGame()

        running = True
        while running:
            # Handles events
            for i in pygame.event.get():
                self.keyPresses()
                # Event which occurs every 50 milliseconds
                if i.type == pygame.USEREVENT + 1:
                    value = self.game.updateGame()
                    if (value):
                        print(value)
                        return value > -1

                # Quitting out of the game
                elif i.type == pygame.QUIT:
                    running = False

    """ Handles pressed keys by the player. """
    def keyPresses(self):
        # Stores whether or not that key has been pressed
        keys=pygame.key.get_pressed()

        # Handling of directions
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            self.game.setDir(3)
        elif (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            self.game.setDir(7)
        elif (keys[pygame.K_UP] or keys[pygame.K_w]):
            self.game.setDir(1)
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            self.game.setDir(5)