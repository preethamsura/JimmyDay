""" Main class which runs the machine learning snake
program or it allows the player to play snake. """

# Necessary imports
import pygame
from Snake import Snake
from Snake import Player

# Creates the snake game.
game = Snake.Snake()

# Creates rectangle for the player game button
player_text = game.font.render("Default", True, game.black, game.green)
player_text_rect = player_text.get_rect()
player_text_rect.center = (200, 60)
game.screen.blit(player_text, player_text_rect)
pygame.display.update()

""" Clears the display buttons"""
def clearButtons():
    # Updates player button to be white
    player_text = game.font.render("Default", True, game.white, game.white)
    game.screen.blit(player_text, player_text_rect)

""" Starts a game which the player can play using wasd or arrow keys. """
def playerGame():
    Player.Player(game)

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
            if (click[0] > 150 and click[1] > 45 and click[0] < 250 and click[1] < 80):
                clearButtons()
                playerGame()
                intro = False

            # Checks to see if the click position was on the Computer game button.
            elif(click[0] > 520 and click[1] > 45 and click[0] < 680 and click[1] < 80):
                clearButtons()
                computerGame()
                intro = False

        # This is ran if the the window is closed. It closes the window and terminates the program.
        elif event.type == pygame.QUIT:
            intro = False
            pygame.quit()