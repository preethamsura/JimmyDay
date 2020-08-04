""" Game where AI chases player around a square board until a timer runs out.
The player wins if they can survive until the timer runs out and they lose otherwise."""

import pygame

class Tag():

    def __init__(self, screenProps):
        # Setting the default variables.
        self.screen = screenProps["screen"]
        self.colors = screenProps["colors"]

        # Default colors + images
        self.white = self.colors["white"]
        self.black = self.colors["black"]
        self.darkblue = self.colors["dark blue"]
        self.gold = self.colors["gold"]

        # Resetting the screen.
        self.screen.fill(self.colors["white"])

        # Parameters for the size of the players
        self.diameter = 30
        self.radius = 15

        #Map borders
        self.topBorder = 100
        self.bottomBorder = 700
        self.rightBorder = 1100
        self.leftBorder = 100

        pygame.draw.rect(self.screen, self.black, (self.leftBorder - self.radius, self.topBorder - self.radius, 
            self.rightBorder - self.leftBorder + self.radius * 2, self.bottomBorder - self.topBorder + self.radius * 2), 5)

        # Default player and computer starting locations
        self.playerLocation = [100, 100]
        self.computerLocation = [1100, 700]
        self.speed = 20

        # Max time that the game should run without the player getting caught. 
        self.maxTime = 30

        # All directions that the player and computer can move in + what value those directions map to.
        self.directions = {
            1: [0, -1], #north
            2: [.5, -.5], #northeast
            3: [1, 0], #east
            4: [.5, .5], #southeast
            5: [0, 1], #south
            6: [-.5, .5], #southwest
            7: [-1, 0], #west
            8: [-.5, -.5] #northwest
        }

        # Default player starting direction.
        self.playerDir = 4

        # Draw initial locations of player
        self.drawPlayers()

        pygame.display.update()

    """ Draws the players at their current locations."""
    def drawPlayers(self):
        pygame.draw.circle(self.screen, self.darkblue, (self.playerLocation[0], self.playerLocation[1]), self.radius)
        pygame.draw.circle(self.screen, self.gold, (self.computerLocation[0], self.computerLocation[1]), self.radius)

    """ Returns direction that computer should move in 
    based on the location of the computer and player. """
    def computerDirection(self):
        #Get difference in x and y values of the two players
        xDif = self.playerLocation[0] - self.computerLocation[0]
        yDif = self.playerLocation[1] - self.computerLocation[1]

        #Determine direction of player
        xDir = self.getDirection(xDif)
        yDir = self.getDirection(yDif)

        #Returns direction values based on xDif and yDif
        if (abs(xDir) == abs(yDir)):
            return [xDir * 1/2, yDir * 1/2]
        else:
            return [xDir, yDir]

    """ Setter for the direction of the player."""
    def setPlayerDirection(self, dir):
        playerDir = dir

    """ Sets the direction that the player is currently moving in. """
    def setDir(self, direction):
        playerDir = direction

    """ Returns directional movement instructions based 
    on difference values. """
    def getDirection(self, difference):
        if (difference > 0):
            return 1
        elif (difference == 0):
            return 0
        else:
            return -1

    """ Returns true if the game is supposed to be over and
    returns false if the game is supposed to keep running."""
    def checkGameEnd(self, time):
        if xDif <= diameter or yDif <= diameter or time == maxTime:
            return true
        else:
            return false

    """ Returns true if player won and returns false is computer won. """
    def getWinner(self, time):
        return time == self.maxTime

    """ Moves both players certain number of pixels in their current given direction. 
    Players cannot move in the given if they are already at the edge of the map. """
    def updateGame(self):
        # Get the directions and locations of the player and computer. 
        computerDir = self.computerDirection()
        xPlayer = self.playerLocation[0] + self.playerDir[0] * self.speed
        yPlayer = self.playerLocation[1] + self.playerDir[1] * self.speed
        xcomp = self.computerLocation[0] + self.computerDir[0] * self.speed
        ycomp = self.computerLocation[1] + self.computerDir[1] * self.speed
        
        # Move the player in the x direction if they will be in bounds after the move. 
        if (xPlayer >= self.leftBorder and xPlayer <= self.rightBorder):
            self.playerLocation[0] = xPlayer
            
        # Move the player in the y direction if they will be in bounds after the move. 
        if (yPlayer >= self.bottomBorder and yPlayer <= self.topBorder):
            self.playerLocation[1] = yPlayer
            
        # Move the computer in the x direction if they will be in bounds after the move. 
        if (xcomp >= self.leftBorder and xcomp <= self.rightBorder):
            self.computerLocation[0] = xcomp
            
        # Move the computer in the y direction if they will be in bounds after the move. 
        if (ycomp >= self.bottomBorder and ycomp >= self.topBorder):
            self.computerLocation[1] = ycomp