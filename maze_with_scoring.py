#############################
# By: Chase Poland          #
# Date: 3/22/18             #
#############################


# Imports
import pygame
import intersects
from walls import *
import random
import time
# Initialize game engine
pygame.init()


# Window
WIDTH = 800
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)
TITLE = "Collect The Coins! "
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60
    


# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

BIGPAPA = pygame.image.load('Chase.png')


# Make a player
player1 =  [200, 150, 20, 20]
vel1 = [0, 0]
player1_speed = 5
score1 = 0

#Sounds
pygame.mixer.music.load("sounds/snow.ogg")

# Make coins
coin1 = [300, 510, 20, 20]
coin2 = [400, 200, 20, 20]
coin3 = [130, 130, 20, 20]
coin4 = [130, 260, 20, 20]

def splash_screen():
    font = pygame.font.Font(None, 48)
    text = font.render("Welcome To The Maze! Press Spacebar to Play!", 1, BLACK)
    text1 = font.render("Collect the Coins!!!", 1, BLACK)
    screen.blit(BIGPAPA, [0, 0])
    screen.blit(text, [0, 100])
    screen.blit(text1, [100, 150])

def restart_screen():
    screen.fill(BLACK)
    for w in walls:
        pygame.draw.rect(screen, BLACK, w)
    font = pygame.font.Font(None, 48)
    text = font.render("Press R to play again!", 1, BLACK)
    screen.blit(text, [0, 100])

def setup():
    global player1, vel1, player1_speed, score1, coins, time_remaining, ticks
    player1 = [10, 10, 20, 20]
    vel1 = [0,0]
    player1_speed = 5
    score1 = 0
    win = False
    coins = [coin1, coin2, coin3, coin4]
    time_remaining = 10
    ticks = 0

    
def game_play():
        pygame.draw.rect(screen, WHITE, player1)
        
        for w in walls:
            pygame.draw.rect(screen, BLUE, w)

        for c in coins:
            pygame.draw.rect(screen, rand_color, c)
        
        font = pygame.font.Font(None, 24)
        text = font.render(str(score1), 1, WHITE)
        time_text = font.render(str(time_remaining), 1, WHITE)
        screen.blit(text, [1, 255])
        screen.blit(time_text, [400, 300])
    
def end_game():
    screen.fill(BLACK)
    for w in walls:
        pygame.draw.rect(screen, BLACK, w)
    font = pygame.font.Font(None, 48)
    text = font.render("Press 'R' to restart the game!", 1, WHITE)
    s_text = font.render("Your score was :  " + str(score1), 1, WHITE)
    screen.blit(text, [230, 150])
    screen.blit(s_text, [230, 100])

# Game loop
setup()
win = False
done = False
play = False
restart = False

while not done:
    # Event processing (React to key presses, mouse clicks, etc.)
    ''' for now, we'll just check to see if the X is clicked '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                playing = True
                pygame.mixer.music.play(-1)

            elif event.key == pygame.K_r:
                playing = False
                win = False
                setup()

    pressed = pygame.key.get_pressed()

    up = pressed[pygame.K_UP]
    down = pressed[pygame.K_DOWN]
    left = pressed[pygame.K_LEFT]
    right = pressed[pygame.K_RIGHT]
    space = pressed[pygame.K_SPACE]
    

    if left:
        vel1[0] = -player1_speed
    elif right:
        vel1[0] = player1_speed
    else:
        vel1[0] = 0

    if play == True:
        ticks += 1

        if ticks % refresh_rate == 0:
            time_remaining -= 1

        if time_remaining == 0:
            play = False
            restart = True

    if space:
        play = True
        
    if up:
        vel1[1] = -player1_speed
    elif down:
        vel1[1] = player1_speed
    else:
        vel1[1] = 0
        
            
    rand_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    # Game logic (Check for collisions, update points, etc.)
    ''' move the player in horizontal direction '''
    player1[0] += vel1[0]

    ''' resolve collisions horizontally '''
    for w in walls:
        if intersects.rect_rect(player1, w):        
            if vel1[0] > 0:
                player1[0] = w[0] - player1[2]
            elif vel1[0] < 0:
                player1[0] = w[0] + w[2]

    ''' move the player in vertical direction '''
    player1[1] += vel1[1]
    
    ''' resolve collisions vertically '''
    for w in walls:
        if intersects.rect_rect(player1, w):                    
            if vel1[1] > 0:
                player1[1] = w[1] - player1[3]
            if vel1[1]< 0:
                player1[1] = w[1] + w[3]


    ''' here is where you should resolve player collisions with screen edges '''




    ''' get the coins '''
    hit_list = []

    for c in coins:
        if intersects.rect_rect(player1, c):
            hit_list.append(c)
     
    hit_list = [c for c in coins if intersects.rect_rect(player1, c)]
    
    for hit in hit_list:
        coins.remove(hit)
        score1 += 1
        print("sound!")
        
    if len(coins) == 0:
        win = True

    screen.fill(BLACK)


    if restart == True:
        restart_screen()

    if play == False:
        splash_screen()

    if play == True:
        game_play()

    if win == True:
        end_game()
        
    # Drawing Functions Executed (Describe the picture. It isn't actually drawn yet.)

    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
