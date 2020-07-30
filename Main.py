""" Main class which runs the machine learning snake
program or it allows the player to play snake. """

# Necessary imports
import pygame
from Snake import Snake
from Snake import Player

# Define the screen which will be used by every game class
screen = ""
font = ""
player_text_rect = ""

# All the colors which can be used in any class
colors = {
    "white": [255, 255, 255],
    "black": [0, 0, 0],
    "green": [46, 135, 58]
}

# Properties of the screen and the actual screen.
screenProperties = {
    screen: "",
    font: "",
    
}

# Runs the application 
def __main__():
    # Creates the screen with default parameters
    createScreen()
    

# Creates the default screen
def createScreen():
    global font, screen, player_text_rect

    # Create the pygame screen with caption "Happy Birthday Jimmy"
    pygame.init()
    pygame.display.set_caption('Happy Birthday Jimmy')

    # Setting up the window
    windowWidth = 800
    windowHeight = 800
    screen = pygame.display.set_mode([windowWidth, windowHeight])
    screen.fill(colors["white"])

    # Creates rectangle for the play Game Button
    font = pygame.font.Font('freesansbold.ttf', 80)
    player_text = font.render("PLAY", True, colors["black"], colors["white"])
    player_text_rect = player_text.get_rect()
    player_text_rect.center = (400, 400)
    screen.blit(player_text, player_text_rect)
    pygame.display.update()

""" Clears the display buttons"""
def clearButtons():
    # Updates player button to be white
    player_text = font.render("Default", True, colors["white"], colors["white"])
    screen.blit(player_text, player_text_rect)

""" Starts a game which the player can play using wasd or arrow keys. """
def playerGame():
    Player.Player(game)

__main__()

""" Runs the intro sequence until the player clicks the button to
play a player version of the game. The variable intro will be set to False when
the simulation starts. """
intro = True
while intro:
    pygame.display.update()
    events = pygame.event.get()
    for event in events:
        # Event for a mouseclick.
        if event.type == pygame.MOUSEBUTTONUP:
            click = pygame.mouse.get_pos()

            # Checks to see if the click position was on the Player game button.
            if (click[0] > 300 and click[1] > 350 and click[0] < 500 and click[1] < 450):
                clearButtons()
                #playerGame()
                #intro = False

        # This is ran if the the window is closed. It closes the window and terminates the program.
        elif event.type == pygame.QUIT:
            intro = False
            pygame.quit()