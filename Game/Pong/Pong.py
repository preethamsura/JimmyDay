#PONG pygame

import random
import pygame, sys
from pygame.locals import *

class Pong():
    def __init__(self):
        #colors
        self.WHITE = (255,255,255)
        self.RED = (255,0,0)
        self.GREEN = (0,255,0)
        self.BLACK = (0,0,0)

        #globals
        self.WIDTH = 600
        self.HEIGHT = 400       
        self.BALL_RADIUS = 20
        self.PAD_WIDTH = 8
        self.PAD_HEIGHT = 80
        self.HALF_PAD_WIDTH = self.PAD_WIDTH // 2
        self.HALF_PAD_HEIGHT = self.PAD_HEIGHT // 2
        self.ball_pos = [0,0]
        self.ball_vel = [0,0]
        self.paddle1_vel = 0
        self.paddle2_vel = 0
        self.l_score = 0
        self.r_score = 0
        self.font = pygame.font.Font('freesansbold.ttf', 25)

        #canvas declaration
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT + 40), 0, 32)
        pygame.display.set_caption('JimmyDay')

        self.paddle1_pos = [self.HALF_PAD_WIDTH - 1, self.HEIGHT//2]
        self.paddle2_pos = [self.WIDTH +1 - self.HALF_PAD_WIDTH, self.HEIGHT//2]
        self.l_score = 0
        self.r_score = 0

        if random.randrange(0,2) == 0:
            self.ball_init(True)
        else:
            self.ball_init(False)
        
        self.fps = pygame.time.Clock()

    """ Plays the game until one side scores. """
    def startGame(self):
        #game loop
        while True:

            self.draw(self.window)

            # Display score needed to win
            self.displayWin()

            for event in pygame.event.get():

                if event.type == KEYDOWN:
                    self.keydown(event)
                elif event.type == KEYUP:
                    self.keyup(event)
                elif event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    
            pygame.display.update()
            self.fps.tick(60)

            self.computerGame()

            if (self.l_score or self.r_score):
                return self.r_score

    """ helper function that spawns a ball, returns a position vector and a velocity vector
    if right is True, spawn to the right, else spawn to the left """
    def ball_init(self, right):
        self.ball_pos = [self.WIDTH//2, self.HEIGHT//2]
        horz = random.randrange(4,7)
        vert = random.randrange(3,5)
        
        if right == False:
            horz = - horz
            
        self.ball_vel = [horz,-vert]

    """draw function of canvas """
    def draw(self, canvas):

        canvas.fill(self.BLACK)
        pygame.draw.line(canvas, self.WHITE, [self.WIDTH // 2, 0],[self.WIDTH // 2, self.HEIGHT], 1)
        pygame.draw.line(canvas, self.WHITE, [self.PAD_WIDTH, 0],[self.PAD_WIDTH, self.HEIGHT], 1)
        pygame.draw.line(canvas, self.WHITE, [self.WIDTH - self.PAD_WIDTH, 0],[self.WIDTH - self.PAD_WIDTH, self.HEIGHT], 1)
        pygame.draw.circle(canvas, self.WHITE, [self.WIDTH//2, self.HEIGHT//2], 70, 1)

        # update paddle's vertical position, keep paddle on the screen
        if self.paddle1_pos[1] > self.HALF_PAD_HEIGHT and self.paddle1_pos[1] < self.HEIGHT - self.HALF_PAD_HEIGHT:
            self.paddle1_pos[1] += self.paddle1_vel
        elif self.paddle1_pos[1] == self.HALF_PAD_HEIGHT and self.paddle1_vel > 0:
            self.paddle1_pos[1] += self.paddle1_vel
        elif self.paddle1_pos[1] == self.HEIGHT - self.HALF_PAD_HEIGHT and self.paddle1_vel < 0:
            self.paddle1_pos[1] += self.paddle1_vel
        
        if self.paddle2_pos[1] > self.HALF_PAD_HEIGHT and self.paddle2_pos[1] < self.HEIGHT - self.HALF_PAD_HEIGHT:
            self.paddle2_pos[1] += self.paddle2_vel
        elif self.paddle2_pos[1] == self.HALF_PAD_HEIGHT and self.paddle2_vel > 0:
            self.paddle2_pos[1] += self.paddle2_vel
        elif self.paddle2_pos[1] == self.HEIGHT - self.HALF_PAD_HEIGHT and self.paddle2_vel < 0:
            self.paddle2_pos[1] += self.paddle2_vel

        #update ball
        self.ball_pos[0] += int(self.ball_vel[0])
        self.ball_pos[1] += int(self.ball_vel[1])

        #draw paddles and ball
        pygame.draw.circle(canvas, self.RED, self.ball_pos, 20, 0)
        pygame.draw.polygon(canvas, self.GREEN, [[self.paddle1_pos[0] - self.HALF_PAD_WIDTH, self.paddle1_pos[1] - self.HALF_PAD_HEIGHT], [self.paddle1_pos[0] - self.HALF_PAD_WIDTH, self.paddle1_pos[1] + self.HALF_PAD_HEIGHT], 
            [self.paddle1_pos[0] + self.HALF_PAD_WIDTH, self.paddle1_pos[1] + self.HALF_PAD_HEIGHT], [self.paddle1_pos[0] + self.HALF_PAD_WIDTH, self.paddle1_pos[1] - self.HALF_PAD_HEIGHT]], 0)
        pygame.draw.polygon(canvas, self.GREEN, [[self.paddle2_pos[0] - self.HALF_PAD_WIDTH, self.paddle2_pos[1] - self.HALF_PAD_HEIGHT], [self.paddle2_pos[0] - self.HALF_PAD_WIDTH, self.paddle2_pos[1] + self.HALF_PAD_HEIGHT], 
            [self.paddle2_pos[0] + self.HALF_PAD_WIDTH, self.paddle2_pos[1] + self.HALF_PAD_HEIGHT], [self.paddle2_pos[0] + self.HALF_PAD_WIDTH, self.paddle2_pos[1] - self.HALF_PAD_HEIGHT]], 0)

        #ball collision check on top and bottom walls
        if int(self.ball_pos[1]) <= self.BALL_RADIUS:
            self.ball_vel[1] = - self.ball_vel[1]
        if int(self.ball_pos[1]) >= self.HEIGHT + 1 - self.BALL_RADIUS:
            self.ball_vel[1] = -self.ball_vel[1]
        
        #ball collison check on gutters or paddles
        if int(self.ball_pos[0]) <= self.BALL_RADIUS + self.PAD_WIDTH and int(self.ball_pos[1]) in range(self.paddle1_pos[1] - self.HALF_PAD_HEIGHT, self.paddle1_pos[1] + self.HALF_PAD_HEIGHT, 1):
            self.ball_vel[0] = -self.ball_vel[0]
            self.ball_vel[0] *= 1.1
            self.ball_vel[1] *= 1.1

        elif int(self.ball_pos[0]) <= self.BALL_RADIUS + self.PAD_WIDTH:
            self.r_score += 1
            self.ball_init(True)
            
        if int(self.ball_pos[0]) >= self.WIDTH + 1 - self.BALL_RADIUS - self.PAD_WIDTH and int(self.ball_pos[1]) in range(self.paddle2_pos[1] - self.HALF_PAD_HEIGHT, self.paddle2_pos[1] + self.HALF_PAD_HEIGHT, 1):
            self.ball_vel[0] = -self.ball_vel[0]
            self.ball_vel[0] *= 1.1
            self.ball_vel[1] *= 1.1
        elif int(self.ball_pos[0]) >= self.WIDTH + 1 - self.BALL_RADIUS - self.PAD_WIDTH:
            self.l_score += 1
            self.ball_init(False)
        
        
    """ keydown handler """
    def keydown(self, event):    
        if event.key == K_UP:
            self.paddle2_vel = -8
        elif event.key == K_DOWN:
            self.paddle2_vel = 8

    """keyup handler """
    def keyup(self, event):    
        if event.key in (K_UP, K_DOWN):
            self.paddle2_vel = 0

    """ Moves the computer paddle based on the direction the ball is in."""
    def computerGame(self):
        if (self.ball_pos[1] > self.paddle1_pos[1]):
            self.paddle1_vel = 8
        elif (self.ball_pos[1] < self.paddle1_pos[1]):
            self.paddle1_vel = -8
        else:
            self.paddle1_vel = 0

    def displayWin(self):
        pygame.draw.rect(self.window, self.WHITE, (0, self.HEIGHT + 50, 
                self.WIDTH, 25), 100)

        score_button = self.font.render("Win by scoring once you dumbass", True, self.BLACK, self.WHITE)
        score_button_rect = score_button.get_rect()
        score_button_rect.center = (self.WIDTH // 2, self.HEIGHT + 25)
        self.window.blit(score_button, score_button_rect)
            