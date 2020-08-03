""" Class which is going to represent the board game."""

import pygame
from random import randint
from Snake import Player as SnakePlayer

class BoardGame():

    """ Creates a new board and starts the game."""
    def __init__(self, screenProps):
        # Assigns useful values to passed in parameter
        self.screenProps = screenProps
        self.screen = screenProps["screen"]
        self.colors = screenProps["colors"]
        self.fonts = screenProps["fonts"]
        self.fonts["turnFont"] = pygame.font.Font('freesansbold.ttf', 25)
        self.fonts["boardFont"] = pygame.font.Font('freesansbold.ttf', 35)
        self.fonts["scoreFont"] = pygame.font.Font('freesansbold.ttf', 45)
        self.fonts["diceFont"] = pygame.font.Font('freesansbold.ttf', 55)
        self.fonts["endGame"] = pygame.font.Font('freesansbold.ttf', 15)
        self.boardSquareLength = 100

        # Assigns the different games that can be played and their names to an integer from 0-3
        self.games = [["Snake", SnakePlayer], ["Snake", SnakePlayer], ["Snake", SnakePlayer], ["Snake", SnakePlayer]]

        # Assigns scores which players receive for certain events. 
        self.winMiniGameScore = 3
        self.reachEndFirstScore = 7

        # Define dimensions for board and creates a new board 
        # with randomized game squares
        self.spaces, self.rows, self.cols = (50, 10, 5)
        self.resetBoard()

        # Default starting positions and starting scores. 
        self.playerPos = 0
        self.computerPos = 0
        self.computerScore = 0
        self.playerScore = 0
        self.playerRadius = 15
        self.lastPlayerRoll = 0
        self.lastComputerRoll = 0

        # Displays the initial starting state of the game. 
        self.updateDisplay()

        # Start the game
        self.playGame()

    """ Will update the display to represent the current state of the board which
    includes where the game squares are located and locations of both players."""
    def updateDisplay(self):
        # Wipe the screen of whatever was there beforehand.
        self.screen.fill(self.colors["light red"])

        # Display different parts of the screen which represent the whole board game.
        self.displayBoard()
        self.displayPieces()
        self.displayScores()
        self.displayPreviousTurns()
        self.displayDiceButton()

        # Update the display with the display changes. 
        pygame.display.update()

    """ Displays the board (top down). Special game squares will be indicated by a number of a different color from
    the rest of the board numbers (which will be of the same background color as the board)."""
    def displayBoard(self):
        for i in range(len(self.board)):
            # Indices for that board square. 
            xval = i % 10 * self.boardSquareLength + 100
            yval = i // 10 * self.boardSquareLength + 300

            # For all the squares in the board, display the number which represents that square. 
            # Colors the number of the square a different color if that square is a game square. 
            if (self.board[i]):
                numberText = self.fonts["boardFont"].render(str(i + 1), 
                    True, self.colors["black"], self.colors["white"])
            else:
                numberText = self.fonts["boardFont"].render(str(i + 1), 
                    True, self.colors["black"], self.colors["light red"])
            numberTextRect = numberText.get_rect()
            numberTextRect.center = (xval, yval)
            self.screen.blit(numberText, numberTextRect)

            # Draw a rectangle around the squares on the board. 
            pygame.draw.rect(self.screen, self.colors["black"], (xval - 20, yval - 20, 
                self.boardSquareLength, self.boardSquareLength), 5)

    """ Displays the information of what the rolls were on the previous turns. """
    def displayPreviousTurns(self):
        # Display information for what player did on the last turn.
        playerString = "The player moved " + str(self.lastPlayerRoll)
        player_text = self.fonts["boardFont"].render(playerString, True, self.colors["black"], self.colors["light red"])
        player_rect = player_text.get_rect()
        player_rect.center = (200, 175)
        self.screen.blit(player_text, player_rect)

        # Display information for the computer's last turn. 
        computerString = "The computer moved " + str(self.lastComputerRoll)
        computer_text = self.fonts["boardFont"].render(computerString, True, self.colors["black"], self.colors["light red"])
        computer_rect = computer_text.get_rect()
        computer_rect.center = (230, 225)
        self.screen.blit(computer_text, computer_rect)

    """ Display the location of the player and the computer player. """
    def displayPieces(self):
        # Display the player piece. 
        playerX = self.playerPos % 10 * self.boardSquareLength + 110
        playerY = self.playerPos // 10 * self.boardSquareLength + 350
        pygame.draw.circle(self.screen, self.colors["dark blue"], (playerX, playerY), self.playerRadius)

        # Display the computer piece. 
        computerX = self.computerPos % 10 * self.boardSquareLength + 160
        computerY = self.computerPos // 10 * self.boardSquareLength + 350
        pygame.draw.circle(self.screen, self.colors["gold"], (computerX, computerY), self.playerRadius)

    """ Display the score for both the player and the computer."""
    def displayScores(self):
        # Display the player score.
        player_text = self.fonts["scoreFont"].render("Player: " + str(self.playerScore), True, self.colors["black"], self.colors["light red"])
        player_rect = player_text.get_rect()
        player_rect.center = (875, 100)
        self.screen.blit(player_text, player_rect)

        # Display the computer score. 
        computer_text = self.fonts["scoreFont"].render("Computer " + str(self.computerScore), True, self.colors["black"], self.colors["light red"])
        computer_rect = computer_text.get_rect()
        computer_rect.center = (900, 150)
        self.screen.blit(computer_text, computer_rect)

    """ Displays the button the player should click on to roll the dice and make their turn."""
    def displayDiceButton(self):
        # Display the text for the button. 
        dice_text = self.fonts["diceFont"].render("Roll the Dice", True, self.colors["black"], self.colors["light red"])
        dice_button_rect = dice_text.get_rect()
        dice_button_rect.center = (200, 100)
        self.screen.blit(dice_text, dice_button_rect)

        # Display the rectangle which goes around the text. 
        pygame.draw.rect(self.screen, self.colors["black"], (15, 65, 390, 60), 5)

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
            randomNum = randint(1, 4)
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

            # Update the display to represent the new game state. 
            self.updateDisplay()

        # Adds score to whichever player reached the end of the board first. 
        self.reachEndFirst()

        # Updates the display with the final results. 
        self.updateDisplay()
        
        # Prints the winner. 
        self.endGame()

    """ Make the players move and starts a mini game if the player lands on a mini game square."""
    def makePlayerMove(self):
        # Wait till player continues the game. 
        clickCoords = [[15, 65], [390, 125]]
        self.waitTillClick(clickCoords)

        # Make the players move. 
        self.lastPlayerRoll = randint(1, 6)
        self.playerPos += self.lastPlayerRoll

        # Plays a mini game if the player is on a game square. 
        if (self.checkGameSpace(self.playerPos)):
            self.updateDisplay()
            self.playMiniGame()

    """ Starts the mini game and returns True if the player won the mini game that they are playing.""" 
    def playMiniGame(self):
        # Choose which mini game to play.
        gameSelection = randint(0, 3)
        gameName = self.games[gameSelection][0]
        gamePlayer = self.games[gameSelection][1]

        # Wait till the player clicks "Play" to start the mini game. 
        self.displayPlayButton("Snake")
        playCoords = [[450, 10],[750, 60]]
        self.waitTillClick(playCoords)

        # Create and start the game. 
        game = gamePlayer.Player(self.screenProps)
        winner = game.playGame()
        return False

    """ Displays the play mini game button which will open up the mini game."""
    def displayPlayButton(self, gameName):
        play_button = self.fonts["diceFont"].render("Play " + gameName, True, self.colors["black"], self.colors["light red"])
        play_button_rect = play_button.get_rect()
        play_button_rect.center = (600, 40)
        self.screen.blit(play_button, play_button_rect)
        pygame.display.update()

    """ Wait till someone clicks in the passed in region (which is represented by coords)."""
    def waitTillClick(self, coords):
        # Variable which keeps track of whether or not the intro should still be running.
        waiting = True

        # Loops until the play button is clicked.
        while waiting:
            events = pygame.event.get()
            for event in events:
                # Event for a mouseclick.
                if event.type == pygame.MOUSEBUTTONUP:
                    click = pygame.mouse.get_pos()
                    print(click)

                    # Checks to see if player clicked the "roll the dice button".
                    if (click[0] > coords[0][0] and click[1] > coords[0][1] and click[0] < coords[1][0] and click[1] < coords[1][1]):
                        waiting = False

                # This is ran if the the window is closed. It closes the window and terminates the program.
                elif event.type == pygame.QUIT:
                    waiting = False
                    pygame.quit()
        
    """ FIX ME"""
    def makeComputerMove(self):
        # Adds to computer square.
        self.lastComputerRoll = self.rollDice()
        self.computerPos += self.lastComputerRoll

        # Checks to see if the computer should play a "minigame." 
        # Computer has a 50-50 chance of winning the minigame. 
        if (self.checkGameSpace(self.computerPos)):
            self.playComputerGame()

    """ Randomly decides whether or not the computer 'won' a minigame
    that it played and adds to the computer score. """
    def playComputerGame(self):
        self.computerScore += randint(0, 1) * self.winMiniGameScore

    """ Returns whether or not the space that was landed on is a game square."""
    def checkGameSpace(self, position):
        return position < 49 and self.board[position]

    """ Returns a random number between 1 and 6 (inclusive). """
    def rollDice(self):
        return randint(1, 6)

    """ Need to print winner at the top of the screen. """
    def endGame(self):
        # Default result is a tie.
        result = "There was a Tie"

        if (self.playerScore > self.computerScore):
            # Prints at top that player won. 
            result = "You Won!"

            # Prize Text
            self.prize = "Steam Code: DTBCT-MTRKI-BPGXR"
            end_text = self.fonts["endGame"].render(self.prize, True, self.colors["black"], self.colors["light red"])
            end_rect = end_text.get_rect()
            end_rect.center = (600, 80)
            self.screen.blit(end_text, end_rect)
            
        elif (self.playerScore < self.computerScore):
            # Prints that computer won and that the player should try again.
            result = "Computer Won"

        # Prints the winner at the top of the screen.
        end_text = self.fonts["diceFont"].render(result, True, self.colors["black"], self.colors["light red"])
        end_rect = end_text.get_rect()
        end_rect.center = (600, 40)
        self.screen.blit(end_text, end_rect)

        pygame.display.update()
        
        # Waits until the player closes out of the window to end the game. 
        waiting = True

        # Loops until the play button is clicked.
        while waiting:
            events = pygame.event.get()
            for event in events:
                # This is ran if the the window is closed. It closes the window and terminates the program.
                if event.type == pygame.QUIT:
                    waiting = False
                    pygame.quit()


    """ Returns true if someone reached the end (either computer or player). """
    def checkGameEnd(self):
        return self.playerPos >= 49 or self.computerPos >= 49

    """ Returns true if it was the player won the game. Returns false if the
    computer won the game or there was a tie. """
    def didPlayerWin(self):
        return self.playerScore > self.computerScore
    
    """ Adds score to which ever player reached the end of the board first.
    Resets the position to 49 so that the final position of the displayed piece
    is on the last square. """
    def reachEndFirst(self):
        if (self.playerPos >= 49):
            self.playerScore += self.reachEndFirstScore
            self.playerPos = 49
        else:
            self.computerScore += self.reachEndFirstScore
            self.computerPos = 49