""" Game where AI chases player around a square board until a timer runs out.
The player wins if they can survive until the timer runs out and they lose otherwise."""

import pygame

class Tag():

    def __init__(self, screenProps):
        # Setting the default variables.
        self.screen = screenProps["screen"]
        self.colors = screenProps["colors"]
        self.font = pygame.font.Font('freesansbold.ttf', 20)

        # Default colors + images
        self.white = self.colors["white"]
        self.black = self.colors["black"]
        self.darkblue = self.colors["dark blue"]
        self.gold = self.colors["gold"]

        # Parameters for the size of the players
        self.diameter = 30
        self.radius = 15

        #Map borders
        self.topBorder = 100
        self.bottomBorder = 700
        self.rightBorder = 1100
        self.leftBorder = 100
        self.drawBorders()

        # Default player and computer starting locations
        self.playerLocation = [300, 300]
        self.computerLocation = [900, 500]
        self.speed = 40

        # Max time that the game should run without the player getting caught. 
        self.maxTime = 30.0
        self.time = 0.0

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
        self.playerDir = self.directions[4]

        # Draw initial locations of player
        self.drawPlayers()

        pygame.display.update()

    """ Refreshes the screen and draws a new border."""
    def drawBorders(self):
        self.screen.fill(self.colors["white"])
        pygame.draw.rect(self.screen, self.black, (self.leftBorder - self.radius, self.topBorder - self.radius, 
            self.rightBorder - self.leftBorder + self.radius * 2, self.bottomBorder - self.topBorder + self.radius * 2), 5)

    """ Draws the players at their current locations."""
    def drawPlayers(self):
        pygame.draw.circle(self.screen, self.darkblue, (int(self.playerLocation[0]), int(self.playerLocation[1])), self.radius)
        pygame.draw.circle(self.screen, self.gold, (int(self.computerLocation[0]), int(self.computerLocation[1])), self.radius)

    """ Display the current time lasted. """ 
    def displayTime(self):
        # Create box for how long the player has lasted
        self.time_text = self.font.render('Time: ' +
            str(int(self.time)), True, self.black, self.white)
        self.time_text_rect = self.time_text.get_rect()
        self.time_text_rect.center = (600, 25)

        # Create box for the amount of time the player needs to last for. 
        self.max_text = self.font.render('Minimum time needed: 30', True, self.black, self.white)
        self.max_text_rect = self.max_text.get_rect()
        self.max_text_rect.center = (690, 50)

        # Display them on the screen
        self.screen.blit(self.time_text, self.time_text_rect)
        self.screen.blit(self.max_text, self.max_text_rect)

    """ Returns direction that computer should move in 
    based on the location of the computer and player. """
    def computerDirection(self):
        #Get difference in x and y values of the two players
        self.xDif = self.playerLocation[0] - self.computerLocation[0]
        self.yDif = self.playerLocation[1] - self.computerLocation[1]
        self.magXDif = abs(self.xDif)
        self.magYDif = abs(self.yDif)

        #Determine direction of player
        xDir = self.getDirection(self.xDif)
        yDir = self.getDirection(self.yDif)

        #Returns direction values based on xDif and yDif
        if (abs(xDir) == abs(yDir)):
            return [xDir * 1/2, yDir * 1/2]
        else:
            return [xDir, yDir]

    """ Sets the direction that the player is currently moving in. """
    def setDir(self, dir):
        self.playerDir = self.directions[dir]

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
    def checkGameEnd(self):
        return (self.magXDif <= self.diameter and self.magYDif <= self.diameter) or self.time >= self.maxTime

    """ Returns true if player won and returns false is computer won. """
    def getWinner(self):
        return self.time >= self.maxTime

    """ Moves both players certain number of pixels in their current given direction. 
    Players cannot move in the given if they are already at the edge of the map. """
    def updateGame(self):
        # Updates the time to represent the new state. 
        self.time += .2

        # Get the directions and locations of the player and computer. 
        computerDir = self.computerDirection()
        xPlayer = self.playerLocation[0] + self.playerDir[0] * self.speed
        yPlayer = self.playerLocation[1] + self.playerDir[1] * self.speed
        xcomp = self.computerLocation[0] + computerDir[0] * self.speed * 1.25
        ycomp = self.computerLocation[1] + computerDir[1] * self.speed * 1.25
        
        # Move the player in the x direction if they will be in bounds after the move. 
        if (xPlayer >= self.leftBorder and xPlayer <= self.rightBorder):
            self.playerLocation[0] = xPlayer
            
        # Move the player in the y direction if they will be in bounds after the move. 
        if (yPlayer <= self.bottomBorder and yPlayer >= self.topBorder):
            self.playerLocation[1] = yPlayer
            
        # Move the computer in the x direction if they will be in bounds after the move. 
        if (xcomp >= self.leftBorder and xcomp <= self.rightBorder):
            self.computerLocation[0] = xcomp
            
        # Move the computer in the y direction if they will be in bounds after the move. 
        if (ycomp <= self.bottomBorder and ycomp >= self.topBorder):
            self.computerLocation[1] = ycomp

        # Draw the new location of players. 
        self.drawBorders()
        self.drawPlayers()
        self.displayTime()

        # Checks whether or not the game is over and returns who won. 
        if (self.checkGameEnd()):
            self.endGame()
            return self.getWinner() or -1

        # Update the display with the new location. 
        pygame.display.update()

    """ Starts the actual tag game."""
    def startGame(self, speed = 200):
        # Start Timer
        pygame.time.set_timer(pygame.USEREVENT + 1, speed)

    """ Disables the timer. """
    def endGame(self):
        # End Timer
        pygame.time.set_timer(pygame.USEREVENT + 1, 0)
