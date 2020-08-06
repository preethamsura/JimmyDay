from itertools import cycle
import random
import sys

import pygame
from pygame.locals import *

try:
    xrange
except NameError:
    xrange = range


class Flappy():
    def __init__(self, screenProps):
        self.FPS = 30
        self.SCREENWIDTH  = 288
        self.SCREENHEIGHT = 512
        self.PIPEGAPSIZE  = 100 # gap between upper and lower part of pipe
        self.BASEY        = self.SCREENHEIGHT * 0.79
        # image, sound and hitmask  dicts
        self.IMAGES, self.SOUNDS, self.HITMASKS = {}, {}, {}

        # list of all possible players (tuple of 3 positions of flap)
        self.PLAYERS_LIST = (
            # yellow bird
            (
                'FlappyBird/assets/sprites/yellowbird-upflap.png',
                'FlappyBird/assets/sprites/yellowbird-midflap.png',
                'FlappyBird/assets/sprites/yellowbird-downflap.png',
            ),
        )

        # list of backgrounds
        self.BACKGROUNDS_LIST = (
            'FlappyBird/assets/sprites/background-day.png',
        )

        # list of pipes
        self.PIPES_LIST = (
            'FlappyBird/assets/sprites/pipe-green.png',
        )

        self.FPSCLOCK = pygame.time.Clock()
        self.SCREEN = pygame.display.set_mode([self.SCREENWIDTH, self.SCREENHEIGHT + 50])
        self.colors = screenProps["colors"]
        self.fonts = screenProps["fonts"]

        # numbers sprites for score display
        self.IMAGES['numbers'] = (
            pygame.image.load('FlappyBird/assets/sprites/0.png').convert_alpha(),
            pygame.image.load('FlappyBird/assets/sprites/1.png').convert_alpha(),
            pygame.image.load('FlappyBird/assets/sprites/2.png').convert_alpha(),
            pygame.image.load('FlappyBird/assets/sprites/3.png').convert_alpha(),
            pygame.image.load('FlappyBird/assets/sprites/4.png').convert_alpha(),
            pygame.image.load('FlappyBird/assets/sprites/5.png').convert_alpha(),
            pygame.image.load('FlappyBird/assets/sprites/6.png').convert_alpha(),
            pygame.image.load('FlappyBird/assets/sprites/7.png').convert_alpha(),
            pygame.image.load('FlappyBird/assets/sprites/8.png').convert_alpha(),
            pygame.image.load('FlappyBird/assets/sprites/9.png').convert_alpha()
        )

        # game over sprite
        self.IMAGES['gameover'] = pygame.image.load('FlappyBird/assets/sprites/gameover.png').convert_alpha()
        # message sprite for welcome screen
        self.IMAGES['message'] = pygame.image.load('FlappyBird/assets/sprites/message.png').convert_alpha()
        # base (ground) sprite
        self.IMAGES['base'] = pygame.image.load('FlappyBird/assets/sprites/base.png').convert_alpha()

        # select background sprites
        self.IMAGES['background'] = pygame.image.load(self.BACKGROUNDS_LIST[0]).convert()

        # select player sprite
        self.IMAGES['player'] = (
            pygame.image.load(self.PLAYERS_LIST[0][0]).convert_alpha(),
            pygame.image.load(self.PLAYERS_LIST[0][1]).convert_alpha(),
            pygame.image.load(self.PLAYERS_LIST[0][2]).convert_alpha(),
        )

        # select random pipe sprites
        self.IMAGES['pipe'] = (
            pygame.transform.flip(
                pygame.image.load(self.PIPES_LIST[0]).convert_alpha(), False, True),
            pygame.image.load(self.PIPES_LIST[0]).convert_alpha(),
        )

        # hismask for pipes
        self.HITMASKS['pipe'] = (
            self.getHitmask(self.IMAGES['pipe'][0]),
            self.getHitmask(self.IMAGES['pipe'][1]),
        )

        # hitmask for player
        self.HITMASKS['player'] = (
            self.getHitmask(self.IMAGES['player'][0]),
            self.getHitmask(self.IMAGES['player'][1]),
            self.getHitmask(self.IMAGES['player'][2]),
        )

    def showWelcomeAnimation(self):
        """Shows welcome screen animation of flappy bird"""
        # index of player to blit on screen
        playerIndex = 0
        playerIndexGen = cycle([0, 1, 2, 1])
        # iterator used to change playerIndex after every 5th iteration
        loopIter = 0

        playerx = int(self.SCREENWIDTH * 0.2)
        playery = int((self.SCREENHEIGHT - self.IMAGES['player'][0].get_height()) / 2)

        messagex = int((self.SCREENWIDTH - self.IMAGES['message'].get_width()) / 2)
        messagey = int(self.SCREENHEIGHT * 0.12)

        basex = 0
        # amount by which base can maximum shift to left
        baseShift = self.IMAGES['base'].get_width() - self.IMAGES['background'].get_width()

        # player shm for up-down motion on welcome screen
        playerShmVals = {'val': 0, 'dir': 1}

        # return values for mainGame
        return {
            'playery': playery + playerShmVals['val'],
            'basex': basex,
            'playerIndexGen': playerIndexGen,
        }


    def mainGame(self, movementInfo):
        score = playerIndex = loopIter = 0
        playerIndexGen = movementInfo['playerIndexGen']
        playerx, playery = int(self.SCREENWIDTH * 0.2), movementInfo['playery']

        basex = movementInfo['basex']
        baseShift = self.IMAGES['base'].get_width() - self.IMAGES['background'].get_width()

        # get 2 new pipes to add to upperPipes lowerPipes list
        newPipe1 = self.getRandomPipe()
        newPipe2 = self.getRandomPipe()

        # list of upper pipes
        upperPipes = [
            {'x': self.SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
            {'x': self.SCREENWIDTH + 200 + (self.SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
        ]

        # list of lowerpipe
        lowerPipes = [
            {'x': self.SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
            {'x': self.SCREENWIDTH + 200 + (self.SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
        ]

        pipeVelX = -4

        # player velocity, max velocity, downward accleration, accleration on flap
        playerVelY    =  -9   # player's velocity along Y, default same as playerFlapped
        playerMaxVelY =  10   # max vel along Y, max descend speed
        playerMinVelY =  -8   # min vel along Y, max ascend speed
        playerAccY    =   1   # players downward accleration
        playerRot     =  45   # player's rotation
        playerVelRot  =   3   # angular speed
        playerRotThr  =  20   # rotation threshold
        playerFlapAcc =  -9   # players speed on flapping
        playerFlapped = False # True when player flaps


        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    if playery > -2 * self.IMAGES['player'][0].get_height():
                        playerVelY = playerFlapAcc
                        playerFlapped = True

            # check for crash here
            crashTest = self.checkCrash({'x': playerx, 'y': playery, 'index': playerIndex},
                                upperPipes, lowerPipes)
            if crashTest[0]:
                return {
                    'y': playery,
                    'groundCrash': crashTest[1],
                    'basex': basex,
                    'upperPipes': upperPipes,
                    'lowerPipes': lowerPipes,
                    'score': score,
                    'playerVelY': playerVelY,
                    'playerRot': playerRot
                }

            # check for score
            playerMidPos = playerx + self.IMAGES['player'][0].get_width() / 2
            for pipe in upperPipes:
                pipeMidPos = pipe['x'] + self.IMAGES['pipe'][0].get_width() / 2
                if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                    score += 1

            # playerIndex basex change
            if (loopIter + 1) % 3 == 0:
                playerIndex = next(playerIndexGen)
            loopIter = (loopIter + 1) % 30
            basex = -((-basex + 100) % baseShift)

            # rotate the player
            if playerRot > -90:
                playerRot -= playerVelRot

            # player's movement
            if playerVelY < playerMaxVelY and not playerFlapped:
                playerVelY += playerAccY
            if playerFlapped:
                playerFlapped = False

                # more rotation to cover the threshold (calculated in visible rotation)
                playerRot = 45

            playerHeight = self.IMAGES['player'][playerIndex].get_height()
            playery += min(playerVelY, self.BASEY - playery - playerHeight)

            # move pipes to left
            for uPipe, lPipe in zip(upperPipes, lowerPipes):
                uPipe['x'] += pipeVelX
                lPipe['x'] += pipeVelX

            # add new pipe when first pipe is about to touch left of screen
            if len(upperPipes) > 0 and 0 < upperPipes[0]['x'] < 5:
                newPipe = self.getRandomPipe()
                upperPipes.append(newPipe[0])
                lowerPipes.append(newPipe[1])

            # remove first pipe if its out of the screen
            if len(upperPipes) > 0 and upperPipes[0]['x'] < -self.IMAGES['pipe'][0].get_width():
                upperPipes.pop(0)
                lowerPipes.pop(0)

            # draw sprites
            self.SCREEN.blit(self.IMAGES['background'], (0,0))

            for uPipe, lPipe in zip(upperPipes, lowerPipes):
                self.SCREEN.blit(self.IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
                self.SCREEN.blit(self.IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

            self.SCREEN.blit(self.IMAGES['base'], (basex, self.BASEY))
            # print score so player overlaps the score
            self.showScore(score)

            # Player rotation has a threshold
            visibleRot = playerRotThr
            if playerRot <= playerRotThr:
                visibleRot = playerRot
            
            playerSurface = pygame.transform.rotate(self.IMAGES['player'][playerIndex], visibleRot)
            self.SCREEN.blit(playerSurface, (playerx, playery))

            self.showNeededScore()

            pygame.display.update()
            self.FPSCLOCK.tick(self.FPS)

    """ Display the score that is needed to get points."""
    def showNeededScore(self):
        pygame.draw.rect(self.SCREEN, self.colors["white"], (0, self.SCREENHEIGHT, 
                self.SCREENWIDTH, self.SCREENHEIGHT + 50), 100)

        score_button = self.fonts["turnFont"].render("Score needed is 5", True, self.colors["black"], self.colors["white"])
        score_button_rect = score_button.get_rect()
        score_button_rect.center = (self.SCREENWIDTH // 2, self.SCREENHEIGHT + 25)
        self.SCREEN.blit(score_button, score_button_rect)

    def showGameOverScreen(self, crashInfo):
        """crashes the player down ans shows gameover image"""
        score = crashInfo['score']
        playerx = self.SCREENWIDTH * 0.2
        playery = crashInfo['y']
        playerHeight = self.IMAGES['player'][0].get_height()
        playerVelY = crashInfo['playerVelY']
        playerAccY = 2
        playerRot = crashInfo['playerRot']
        playerVelRot = 7

        basex = crashInfo['basex']

        upperPipes, lowerPipes = crashInfo['upperPipes'], crashInfo['lowerPipes']

        while playery + playerHeight < self.BASEY - 1:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    if playery + playerHeight >= self.BASEY - 1:
                        return

            # player y shift
            if playery + playerHeight < self.BASEY - 1:
                playery += min(playerVelY, self.BASEY - playery - playerHeight)

            # player velocity change
            if playerVelY < 15:
                playerVelY += playerAccY

            # rotate only when it's a pipe crash
            if not crashInfo['groundCrash']:
                if playerRot > -90:
                    playerRot -= playerVelRot

            # draw sprites
            self.SCREEN.blit(self.IMAGES['background'], (0,0))

            for uPipe, lPipe in zip(upperPipes, lowerPipes):
                self.SCREEN.blit(self.IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
                self.SCREEN.blit(self.IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

            self.SCREEN.blit(self.IMAGES['base'], (basex, self.BASEY))
            self.showScore(score)

            playerSurface = pygame.transform.rotate(self.IMAGES['player'][1], playerRot)
            self.SCREEN.blit(playerSurface, (playerx,playery))
            self.SCREEN.blit(self.IMAGES['gameover'], (50, 180))

            self.showNeededScore()

            self.FPSCLOCK.tick(self.FPS)
            pygame.display.update()
        return score


    def playerShm(self, playerShm):
        """oscillates the value of playerShm['val'] between 8 and -8"""
        if abs(playerShm['val']) == 8:
            playerShm['dir'] *= -1

        if playerShm['dir'] == 1:
            playerShm['val'] += 1
        else:
            playerShm['val'] -= 1


    def getRandomPipe(self):
        """returns a randomly generated pipe"""
        # y of gap between upper and lower pipe
        gapY = random.randrange(0, int(self.BASEY * 0.6 - self.PIPEGAPSIZE))
        gapY += int(self.BASEY * 0.2)
        pipeHeight = self.IMAGES['pipe'][0].get_height()
        pipeX = self.SCREENWIDTH + 10

        return [
            {'x': pipeX, 'y': gapY - pipeHeight},  # upper pipe
            {'x': pipeX, 'y': gapY + self.PIPEGAPSIZE}, # lower pipe
        ]


    def showScore(self, score):
        """displays score in center of screen"""
        scoreDigits = [int(x) for x in list(str(score))]
        totalWidth = 0 # total width of all numbers to be printed

        for digit in scoreDigits:
            totalWidth += self.IMAGES['numbers'][digit].get_width()

        Xoffset = (self.SCREENWIDTH - totalWidth) / 2

        for digit in scoreDigits:
            self.SCREEN.blit(self.IMAGES['numbers'][digit], (Xoffset, self.SCREENHEIGHT * 0.1))
            Xoffset += self.IMAGES['numbers'][digit].get_width()


    def checkCrash(self, player, upperPipes, lowerPipes):
        """returns True if player collders with base or pipes."""
        pi = player['index']
        player['w'] = self.IMAGES['player'][0].get_width()
        player['h'] = self.IMAGES['player'][0].get_height()

        # if player crashes into ground
        if player['y'] + player['h'] >= self.BASEY - 1:
            return [True, True]
        else:

            playerRect = pygame.Rect(player['x'], player['y'],
                        player['w'], player['h'])
            pipeW = self.IMAGES['pipe'][0].get_width()
            pipeH = self.IMAGES['pipe'][0].get_height()

            for uPipe, lPipe in zip(upperPipes, lowerPipes):
                # upper and lower pipe rects
                uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], pipeW, pipeH)
                lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], pipeW, pipeH)

                # player and upper/lower pipe hitmasks
                pHitMask = self.HITMASKS['player'][pi]
                uHitmask = self.HITMASKS['pipe'][0]
                lHitmask = self.HITMASKS['pipe'][1]

                # if bird collided with upipe or lpipe
                uCollide = self.pixelCollision(playerRect, uPipeRect, pHitMask, uHitmask)
                lCollide = self.pixelCollision(playerRect, lPipeRect, pHitMask, lHitmask)

                if uCollide or lCollide:
                    return [True, False]

        return [False, False]

    def pixelCollision(self, rect1, rect2, hitmask1, hitmask2):
        """Checks if two objects collide and not just their rects"""
        rect = rect1.clip(rect2)

        if rect.width == 0 or rect.height == 0:
            return False

        x1, y1 = rect.x - rect1.x, rect.y - rect1.y
        x2, y2 = rect.x - rect2.x, rect.y - rect2.y

        for x in xrange(rect.width):
            for y in xrange(rect.height):
                if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
                    return True
        return False

    def getHitmask(self, image):
        """returns a hitmask using an image's alpha."""
        mask = []
        for x in xrange(image.get_width()):
            mask.append([])
            for y in xrange(image.get_height()):
                mask[x].append(bool(image.get_at((x,y))[3]))
        return mask