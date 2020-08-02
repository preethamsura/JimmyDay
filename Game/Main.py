""" Main class which instantiates pygame and creates the basic screen. 
Will leave this class and move to other files as soon as the game is started. 
Game starts when player clicks the 'Play' Button. """

# Necessary imports
import pygame
import BoardGame

# Instantiate play button for the main screen.
play_button_rect = ""

# All the default colors which can be used in any class
colors = {
    "white": [255, 255, 255],
    "black": [0, 0, 0],
    "green": [46, 135, 58],
    "bright blue": [0, 255, 255],
    "light red" : [255, 102, 102],
    "dark blue" : [0, 51, 102],
    "gold" : [255, 188, 0],
}  

fonts = {
    "playButtonFont": "",
    "boardFont": ""
}

# Properties of the screen and the actual screen.
screenProperties = {
    "screen": "", # Screen which is going to be used
    "font": "", # Default font
    "windowWidth": "", # Screen width
    "windowHeight": "", # Screen height
    "colors": colors, 
    "fonts": fonts
}

# Runs the application 
def __main__():
    # Creates the screen with default parameters and a play button.
    createScreen()

    # Keeps the screen going until someone clicks the play button. 
    introduction()

    Board = BoardGame.BoardGame(screenProperties)
    

# Creates the default screen
def createScreen():
    global play_button_rect

    # Create the pygame screen with caption "Happy Birthday Jimmy"
    pygame.init()
    pygame.display.set_caption('Happy Birthday Jimmy')

    # Setting up the window
    screenProperties["windowWidth"] = 1200
    screenProperties["windowHeight"] = 800
    screenProperties["screen"] = pygame.display.set_mode([screenProperties["windowWidth"], screenProperties["windowHeight"]])
    screenProperties["screen"].fill(colors["white"])

    # Creates rectangle for the play Game Button
    fonts["playButtonFont"] = pygame.font.Font('freesansbold.ttf', 80)
    play_text = fonts["playButtonFont"].render("PLAY", True, colors["black"], colors["white"])
    play_button_rect = play_text.get_rect()
    play_button_rect.center = (600, 400)
    screenProperties["screen"].blit(play_text, play_button_rect)
    pygame.display.update()

""" Clears the display buttons"""
def clearButtons():
    # Updates player button to be white
    play_text = fonts["playButtonFont"].render("Default", True, colors["white"], colors["white"])
    screenProperties["screen"].blit(play_text, play_button_rect)

""" Runs the intro sequence until the player clicks the button to
play a player version of the game. The variable intro will be set to False when
the simulation starts. """
def introduction():
    # Variable which keeps track of whether or not the intro should still be running.
    intro = True

    # Loops until the play button is clicked.
    while intro:
        pygame.display.update()
        events = pygame.event.get()
        for event in events:
            # Event for a mouseclick.
            if event.type == pygame.MOUSEBUTTONUP:
                click = pygame.mouse.get_pos()

                # Checks to see if the click position was on the Player game button.
                if (click[0] > 500 and click[1] > 350 and click[0] < 700 and click[1] < 450):
                    clearButtons()
                    intro = False

            # This is ran if the the window is closed. It closes the window and terminates the program.
            elif event.type == pygame.QUIT:
                intro = False
                pygame.quit()

# Starts the game.
__main__()