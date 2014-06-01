# Planet Defender Game
# By Dathan Ault-McCoy
# Game Idea By Finn Davis Owsley 
# Python Build
# Version 1.6

import sys, time, random, pygame

class ObjectClass(pygame.sprite.Sprite):
	def __init__(self, imageFile, location, speed):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(imageFile)
		self.rect = self.image.get_rect()
		self.speed = speed
		self.rect.centerx, self.rect.centery = location
	def move(self):
		self.rect = self.rect.move(self.speed)

class ShipClass(ObjectClass):
	def __init__(self, imageFile):
		ObjectClass.__init__(self, imageFile, [75, 50], [0, 0])

class WeaponClass(ObjectClass):
	def __init__(self, imageFile, shooter, speed, damage):
		ObjectClass.__init__(self, imageFile, [shooter.rect.centerx, shooter.rect.centery], speed)
		self.damage = damage

class EnemyClass(ObjectClass):
	def __init__(self, imageFile, location, speed, health, points):
		ObjectClass.__init__(self, imageFile, location, speed)
		self.health = health
		self.points = points
	def damage(self, damage):
		self.health = self.health - damage

class UpgradeClass(pygame.sprite.Sprite):
	def __init__(self, text, color, location, speed, type):
		pygame.sprite.Sprite.__init__(self)
		self.surf = pygame.font.Font(None, 100).render(text, 1, color)
		self.rect = self.surf.get_rect()
		self.speed = speed
		self.rect.centerx, self.rect.centery = location
		self.type = type
	def move(self):
		self.rect = self.rect.move(self.speed)


# pygame initialization
pygame.init()                                   
clock = pygame.time.Clock()
screen = pygame.display.set_mode([1000, 700])
background = pygame.Surface(screen.get_size())
pygame.key.set_repeat(1, 25)
# makes the ship and weapons
weaponDamage = 1
shipSpeed = 12
friendlyShip = ShipClass('data/shipImage.bmp')
weaponGroup = pygame.sprite.Group()
# makes the enemies
enemyCounter = 0
enemyGroup = pygame.sprite.Group()
enemyRange = 300
# phase 1 enemies
def enemyGenerator(enemyRange):
	enemyType = random.randint(1, 3)
       	if enemyType < 3:
       		enemyStats = ['data/enemyImage1.bmp', 1, [-15, 0], 10]
       	elif enemyType == 3:
       		enemyStats = ['data/enemyImage1.bmp', 2, [-10, 0], 15]
       	enemyGroup.add(EnemyClass(enemyStats[0], [screen.get_width() + 600, screen.get_height() / 2 + random.randint(-enemyRange, enemyRange)], enemyStats[2], enemyStats[1], enemyStats[3]))
	enemyCounter = 0
enemyGenerator(enemyRange)
# makes the power ups
upgradeGroup = pygame.sprite.Group()
upgradeCounter = 0
def upgradeGenerator(enemyRange):
	powerupType = random.randint(1, 3)
       	if powerupType == 1:
       		upgradeStats = ['S', (100, 50, 255), 'shipspeed']
       	elif powerupType == 2:
       		upgradeStats = ['W', (100, 80, 5), 'weapondamage']
       	elif powerupType == 3:
       		upgradeStats = ['L', (255, 50, 50), 'livesup']
       	upgradeGroup.add(UpgradeClass(upgradeStats[0], upgradeStats[1], [screen.get_width() + 3000 + random.randint(1000, 3000), screen.get_height() / 2 + random.randint(-enemyRange, enemyRange)], [-12, 0], upgradeStats[2]))
upgradeGenerator(enemyRange)
# sets game phase variables
gameStart = False
gameOver = False
# start menu
gameTitleFont = pygame.font.Font(None, 150)
gameInstructionsFont = pygame.font.Font(None, 50)
gameStartFont = pygame.font.Font(None, 75)
gameTitleSurf = gameTitleFont.render('Planet Defender', 1, (255, 255, 255))
gameInstructionsSurf = [gameInstructionsFont.render('UP ARROW: move up', 1, (255, 255, 255)), gameInstructionsFont.render('DOWN ARROW: move down', 1, (255, 255, 255)), gameInstructionsFont.render('SPACE: fire weapons', 1, (255, 255, 255)), gameInstructionsFont.render('P KEY: pause/unpause', 1, (255, 255, 255))]
gameStartSurf = gameStartFont.render('PRESS ENTER TO START', 1, (255, 255, 255))
gameIcon = pygame.image.load('data/enemyImage1.bmp') 
# completed game screen
congratulationsFont = pygame.font.Font(None, 100)
finalScoreFont = pygame.font.Font(None, 75)
highscoreFont = pygame.font.Font(None, 60)
highscoreSurf = highscoreFont.render('NEW HIGHSCORE', 1, (255, 255, 255))
highscoreScoreFont = pygame.font.Font(None, 65)
# lost game screen
gameOverFont = pygame.font.Font(None, 175)
gameOverSurf = gameOverFont.render('GAME OVER', 1, (255, 255, 255))
# sets the game variables
lives = 7
score = 0
# sets other variables
repCounter = 0
paused = False
# font initialization
pygame.font.init()

while True:
	# regulates the FPS
	clock.tick(30)
	# empties the screen
	screen.fill([0, 0, 0])
	# runs the lives counter
	livesFont = pygame.font.Font(None, 75)
	livesSurf = livesFont.render(str(lives), 1, [255, 255, 255])
	# opens the highscore file
	highscore = open('data/highscore.txt', 'r+')
	# gets events
	if gameStart and not gameOver:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				# moves the ship down
				if event.key == pygame.K_DOWN and friendlyShip.rect.top + 75 < screen.get_height():
					friendlyShip.speed[1] = shipSpeed
					friendlyShip.move()
				# moves the ship up
				elif event.key == pygame.K_UP and friendlyShip.rect.top > 0:
					friendlyShip.speed[1] = -shipSpeed
					friendlyShip.move()
				# fires the weapon
				elif event.key == pygame.K_SPACE:
					repCounter += 1
					if repCounter > 6:
						weaponGroup.add(WeaponClass('data/weaponImage1.bmp', friendlyShip, [30, 0], 1))
						repCounter = 0
			if event.type == pygame.KEYUP:
				# pauses the game
				if event.key == pygame.K_p:
					paused = True
					while paused:
						for event in pygame.event.get():
							if event.type == pygame.QUIT:
								sys.exit()
							if event.type == pygame.KEYUP:
								if event.key == pygame.K_p:
									paused = False
		# makes more enemies
		if enemyCounter > 70:
			enemyGenerator(enemyRange)
			enemyCounter = 0
		else:
			enemyCounter += 1
		# makes more upgrades
		if upgradeCounter > 250:
			upgradeGenerator(enemyRange)
			upgradeCounter = 0
		else:
			enemyCounter += 1
		for enemy in pygame.sprite.spritecollide(friendlyShip, enemyGroup, False):
			# deals damage to you if an enemy hits your ship
			lives -= 1
			enemy.kill()
		for upgrade in pygame.sprite.spritecollide(friendlyShip, upgradeGroup, False):
			# gives you upgrades
			if upgrade.type == 'shipspeed':
				shipSpeed += 2
			if upgrade.type == 'weapondamage':
				weaponDamage += 1
			if upgrade.type ==  'livesup':
				lives += 1
			upgrade.kill()
		for weapon in weaponGroup:
			# deals damage to the enemies
			for enemy in pygame.sprite.spritecollide(weapon, enemyGroup, False):
				enemy.damage(weaponDamage)
				weapon.kill()
			# destroys the weapon if off screen
			if weapon.rect.left > screen.get_width():
				weapon.kill()
			# moves the weapon
			weapon.move()
			# draws the weapon
			screen.blit(weapon.image, weapon.rect)
		for enemy in enemyGroup:
			if enemy.health > 0:
				# moves the enemy
				enemy.move()
				# draws the enemy
				screen.blit(enemy.image, enemy.rect)
			else:
				# kills the enemy
				enemy.kill()
				# gives you points
				score += enemy.points
			if enemy.rect.left + 50 < 0:
				# deals you damage
				lives -= 1
				enemy.kill()
		for upgrade in upgradeGroup:
			# moves the upgrade
			upgrade.move()
			# kills the upgrade if off screen
			if upgrade.rect.left + 150 < 0:
				upgrade.kill()
			# draws the uprade
			screen.blit(upgrade.surf, upgrade.rect)
		# ends the game
		if lives < 1:
			gameOver = True
			enemyGroup.empty()
			weaponGroup.empty()
			upgradeGroup.empty()
			enemyGenerator(enemyRange)
			upgradeGenerator(enemyRange)
			weaponDamage = 1
			shipSpeed = 11
		# draws the ship
		screen.blit(friendlyShip.image, friendlyShip.rect)
		# draws the lives counter
		screen.blit(livesSurf, [10, 10])
	# start menu
	if not gameStart and not gameOver:
		# resets lives
		lives = 5
		# gets the events
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				# starts the game
				if event.key == pygame.K_RETURN:
					gameStart = True
			# quits the game
			if event.type == pygame.QUIT:
				sys.exit()
		# draws the icon
		screen.blit(gameIcon, [screen.get_width() / 2 - gameIcon.get_width() / 2, screen.get_height() / 2 - 200])
		# draws the title
		screen.blit(gameTitleSurf, [screen.get_width() / 2 - gameTitleSurf.get_width() / 2, screen.get_height() - 450])
		# draws the start instructions
		screen.blit(gameStartSurf, [screen.get_width() / 2 - gameStartSurf.get_width() / 2, screen.get_height() - 350])
		# resets the counter variable
		listPos = 0
		# draws the game instructions
		for surf in gameInstructionsSurf:
			listPos += 1
			screen.blit(surf, [screen.get_width() / 2 - surf.get_width() / 2, screen.get_height() - 300 + 40 * listPos])
		# displays everything
	# finish message
	if gameStart and gameOver:
		# gets events
		for event in pygame.event.get():
			# quits the game
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				# restarts the game
				if event.key == pygame.K_RETURN:
					gameStart = False
					gameOver = False
					score = 0
					time.sleep(0.3)
		# calculates your score
	       	finalScoreSurf = finalScoreFont.render('Your final score was ' + str(score), 1, (255, 255, 255))
	       	# displays the game over message
	       	screen.blit(gameOverSurf, [screen.get_width() / 2 - gameOverSurf.get_width() / 2, screen.get_height() / 2 - 135])
	       	# displays your score
	       	screen.blit(finalScoreSurf, [screen.get_width() / 2 - finalScoreSurf.get_width() / 2, screen.get_height() /2 + 50])
	       	# checks for highscore
		highscore.seek(0)
	       	if score >= int(highscore.read()):
	       		# displays new highscore message
	       		screen.blit(highscoreSurf, [screen.get_width() / 2 - highscoreSurf.get_width() / 2, screen.get_height() / 2 + 170])
	       		# changes the highscore
	       		highscore.seek(0)
	       		highscore.truncate()
	       		highscore.write(str(score))
		# displays highscore
		highscore.seek(0)
		highscoreScoreSurf = highscoreScoreFont.render('Highscore: ' + str(highscore.read()), 1, (255, 255, 255)) 
		screen.blit(highscoreScoreSurf, [screen.get_width() / 2 - highscoreScoreSurf.get_width() /2, screen.get_height() / 2 + 110])
	pygame.display.flip()
	highscore.close()


