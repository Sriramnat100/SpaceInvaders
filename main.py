# Sriram Natarajan
# Period 3
# AP Computer Science Principles
# 1. Initialize game window and objects (player, aliens, bullets)
# 2. Set up game loop
# 3. Check player input for movement and shooting
# 4. Move aliens, player, and bullets
# 5. Check for collisions between objects
# 6. Update scores and lives
# 7. Repeat loop until player loses or defeats all aliens
# 8. Display game over message or victory screen.


import pygame
from pygame.locals import *
from pygame.sprite import *
from pygame import mixer
import random

# from gameObj import Spaceship
from globalVars import *
from gameObj import *

#set the frame rate of the game.
clock = pygame.time.Clock()
pygame.mixer.pre_init(44100, -16, 2, 512)
#initialize pygame and the mixer module.
mixer.init()
pygame.init()

fps = 60;
countdown = 0
lastCount = pygame.time.get_ticks()
gameOver = 0;
#variable used to track the time interval between big spaceship appearances.
bigShipTime = pygame.time.get_ticks()

def changeGameOver(status):
	#allows the game over status to be changed.
	gameOver = status

prevInvaderShot = pygame.time.get_ticks()

screenWidth = getWidthHeight()[0]
screenHeight = getWidthHeight()[1]

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Space Invaders')

#fonts used
font30 = pygame.font.SysFont('Constantia', 30)
font40 = pygame.font.SysFont('Constantia', 40)

#sound effects needed
explosionSound = pygame.mixer.Sound("sounds/explosion.wav")
explosionSound.set_volume(0.4)

explosionSound2 = pygame.mixer.Sound("sounds/explosion2.wav")
explosionSound2.set_volume(0.2)

laserSound = pygame.mixer.Sound("sounds/laser.wav")
laserSound.set_volume(0.05)

def drawBg():
	# load image and scale it to the screen width & height
	bgImage = pygame.image.load("images/newbackround.jpeg")
	bgImage = pygame.transform.scale(bgImage, (screenWidth, screenHeight))

	screen.blit(bgImage, (0, 0))

#renders and displays text on the screen.
def createText(tx, font,color, x, y):
	img = font.render(tx, True, color)
	screen.blit(img, (x, y))

# Sprite groups
spaceshipGrp = pygame.sprite.Group()
laserGrp = pygame.sprite.Group()
invaderLaserGrp = pygame.sprite.Group()
invaderGrp = pygame.sprite.Group()
explosionGrp = pygame.sprite.Group()
bigShipGrp = pygame.sprite.Group()

# init player
spaceship = Spaceship(int(screenWidth / 2), screenHeight - 100, 3, screenWidth, screenHeight, laserGrp, screen, invaderGrp, explosionGrp, explosionSound, laserSound, bigShipGrp)

#create multiple instances of the invader objects and add them to the invaderGrp sprite group.
for x in range(5):
	for y in range(5):
		invader = Invaders(100 + y * 100, 100 + x * 70)
		invaderGrp.add(invader)

spaceshipGrp.add(spaceship)

run = True

while run:
	clock.tick(fps)

	drawBg()

#checking if the countdown variable is equal to 0
	if countdown == 0:
		curTime = pygame.time.get_ticks()
		if curTime - prevInvaderShot > 1000 and len(invaderGrp) > 0:
			shootingInvader = random.choice(invaderGrp.sprites())
			invaderLaser = InvaderLaser(shootingInvader.rect.center[0], shootingInvader.rect.center[1], screenHeight, spaceshipGrp, explosionGrp, explosionSound2)
			invaderLaserGrp.add(invaderLaser)
			prevInvaderShot = curTime

		genSpaceShip = random.randint(1, 100)
		# genSpaceShip = 4
		# if len(bigShipGrp) == 0 and genSpaceShip == 4 and bigShipTime - curTime > 100:
		if len(bigShipGrp) == 0 and genSpaceShip == 2:
			bigShip = BigSpaceship(screenWidth - 20, 600)
			bigShipGrp.add(bigShip)
			bigShipTime = pygame.time.get_ticks()

		if len(invaderGrp) == 0:
			gameOver = 1

		if gameOver == 0:
			gameOver = spaceship.update()
			laserGrp.update()
			invaderGrp.update()
			invaderLaserGrp.update()
			bigShipGrp.update()
		else:
			if gameOver == -1:
				createText('GAME OVER!!!', font40, (255, 255, 255), int(screenWidth / 2 - 110), int(screenHeight / 2 + 50))
			if gameOver == 1:
				createText('YOU WIN!!!', font40, (255, 255, 255), int(screenWidth / 2 - 90), int(screenHeight / 2 + 50))
	
	#used to track the time interval between invader shots.
	if countdown > 0:
		createText('Get Ready!!!', font40, (255, 255, 255), int(screenWidth / 2 - 110), int(screenHeight / 2 + 50))
		createText(str(countdown), font30, (255, 255, 255), int(screenWidth / 2 - 10), int(screenHeight / 2 + 100))
		countTimer = pygame.time.get_ticks()
	#lastcount variable is used to track the time of the last invader shot.
		if countTimer - lastCount > 1000:
			countdown -= 1
			lastCount = countTimer

	explosionGrp.update()

	spaceshipGrp.draw(screen)
	laserGrp.draw(screen)
	invaderGrp.draw(screen)
	invaderLaserGrp.draw(screen)
	explosionGrp.draw(screen)
	bigShipGrp.draw(screen)

#runs continuously until the run variable is set to False.
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()
