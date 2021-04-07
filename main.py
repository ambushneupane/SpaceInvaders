import pygame
import math
import random
from pygame import mixer

pygame.init()

width = 900
height = 600

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
FPS = 40
clock = pygame.time.Clock()

# Background
background = pygame.image.load("bgnight.png")

#Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1) #-1 plays in loop
# Player
playerIMG = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0


# Enemies
enemyIMG = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_of_enemy = 6
for i in range(num_of_enemy):
    enemyIMG.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(100, 150))


    enemyX_change.append(6)
    enemyY_change.append(20)

#Bullet
bulletIMG = pygame.image.load('bullet.png')
bulletX = playerX
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 40)
textX = 10
textY = 10

#Game over Text
game_over_font=pygame.font.Font('freesansbold.ttf',64)

def game_over_Text():
    over_text= game_over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text,(250,250))

#Functions
def show_score(x, y):
    score = font.render("SCORE:-" + str(score_value), True, (255, 255, 255))
    screen.blit(score,(x,y))


def player(x, y):
    screen.blit(playerIMG, (x, y))


def enemy(x, y, i):
    screen.blit(enemyIMG[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletIMG, (x + 16,
                            y + 10))  # x+16 to fire the bullet from center and y+10 to show bullet was fired from the top of the  player


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))

    if distance < 27:

        return True
    else:
        return False


# Game Loop
running = True
while running:
    clock.tick(FPS)
    screen.fill((0, 0, 0))  # RGB
    screen.blit(background, (0, 0))

    #Checking if the program is closed or not.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Checking if any key is pressed or not.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -8
            if event.key == pygame.K_RIGHT:
                playerX_change = 8
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound=mixer.Sound('laser.wav')
                    bullet_Sound.play()

                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    #player moment
    playerX += playerX_change
    if playerX >= width - 64:
        playerX = width - 64
    elif playerX <= 0:
        playerX = 0

    # enemy Moment
    for i in range(num_of_enemy):
        #Game OVER
        if enemyY[i] > 400:
            for j in range(num_of_enemy):
                enemyY[j]=2000 #setting Y=2000 so that we don't see them in the screen
            game_over_Text()
            break
        enemyX[i] += enemyX_change[i]

        if enemyX[i] >= width - 64:
            enemyX_change[i] = -10
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] <= 0:
            enemyX_change[i] = 10
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)

        if collision:
            explosion_Sound= mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)
    # bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()
