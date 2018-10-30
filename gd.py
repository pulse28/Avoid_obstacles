import pygame
import time
import random
import ast

pygame.init()

crash_sound = pygame.mixer.Sound("crashsound.wav")
pygame.mixer.music.load("bgmusic.wav")

display_width = 800
display_height = 600
with open('best.txt', 'r') as f:
	best = ast.literal_eval(f.read())

black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
bright_green = (0,150,0)
bright_red = (150,0,0)
block_color = (35, 57, 113)
pause = False

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Dodge Blocks!')
clock = pygame.time.Clock()

carImg = pygame.image.load('racecar.png') #image of car

pygame.display.set_icon(carImg)

def things_dodged(count):
	font = pygame.font.SysFont("comicsansms", 25)
	text = font.render("Dodged : "+str(count), True, black)
	gameDisplay.blit(text,(0,0))

def best_display(count):
	font = pygame.font.SysFont("comicsansms", 25)
	text = font.render("Best : "+str(count), True, black)
	gameDisplay.blit(text,(0,20))

def things(thingx, thingy, thingw, thingh, color):
	pygame.draw.rect(gameDisplay, block_color, [thingx, thingy, thingw, thingh])

def car(x,y) :
	gameDisplay.blit(carImg, (x,y))

def text_objects(text, font):
	textSurface = font.render(text, True, black)
	return textSurface, textSurface.get_rect()

def crash():

	pygame.mixer.music.stop()
	pygame.mixer.Sound.play(crash_sound)

	largeText = pygame.font.SysFont('comicsansms',115)
	TextSurf, TextRect = text_objects("You Crashed!", largeText)
	TextRect.center = ((display_width/2),(display_height/2))
	gameDisplay.blit(TextSurf, TextRect)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit_game()

		button("Play Again", 150, 450, 100, 50, green, bright_green, game_loop)
		button("Quit", 550, 450, 100, 50, red, bright_red, quit_game)

		pygame.display.update()
		clock.tick(100)

def button(msg, x, y, w, h, ic, ac, action=None):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()

	if mouse[0] > x and mouse[0] < x+w and mouse[1] > y and mouse[1] < y+h:
		pygame.draw.rect(gameDisplay, ac, (x,y,w,h))
		if click[0] == 1 and action != None:
			#GO
			action()

	else:
		pygame.draw.rect(gameDisplay, ic, (x,y,w,h))

	smallText = pygame.font.SysFont("comicsansms", 20)
	textSurf, textRect = text_objects(msg, smallText)
	textRect.center = ((x+(w/2)),(y+(h/2)))
	gameDisplay.blit(textSurf, textRect)

def unpause():
	global pause
	pygame.mixer.music.unpause()
	pause = False

def paused():
	pygame.mixer.music.pause()
	global pause
	pause = True

	largeText = pygame.font.SysFont('comicsansms',115)
	TextSurf, TextRect = text_objects("Paused", largeText)
	TextRect.center = ((display_width/2),(display_height/2))
	gameDisplay.blit(TextSurf, TextRect)

	while pause:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit_game()

		button("Continue", 150, 450, 100, 50, green, bright_green, unpause)
		button("Quit", 550, 450, 100, 50, red, bright_red, quit_game)

		pygame.display.update()
		clock.tick(15)

def game_intro():
	pygame.mixer.music.play(-1)
	intro = True
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit_game()

		gameDisplay.fill(white)
		largeText = pygame.font.SysFont('comicsansms',115)
		TextSurf, TextRect = text_objects("Dodge Blocks!", largeText)
		TextRect.center = ((display_width/2),(display_height/2))
		gameDisplay.blit(TextSurf, TextRect)

		#button(msg, x, y, w, h, ic, ac)

		button("Go!", 150, 450, 100, 50, green, bright_green, game_loop)
		button("Quit", 550, 450, 100, 50, red, bright_red, quit_game)

		pygame.display.update()
		clock.tick(15)

def quit_game():
	with open('best.txt', 'w') as f:
		f.write(str(best))
	pygame.quit()
	quit()

def game_loop():

	pygame.mixer.music.stop()
	pygame.mixer.music.play(-1)
	global pause
	global best
	x = (display_width * 0.5 - 64)
	y = (display_height * 0.7)

	x_change = 0

	thing_startx = random.randrange(200,display_width-200)
	print(thing_startx)
	thing_starty = -600
	thing_speed = 4
	thing_width = 100
	thing_height = 100
	car_speed = 5

	dodged = 0;

	gameExit = False

	while not gameExit:

		for event in pygame.event.get() :
			if event.type == pygame.QUIT:
				with open('best.txt', 'w') as f:
					f.write(str(best)) 
				quit_game()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					x_change = 0 - car_speed
				elif event.key == pygame.K_RIGHT:
					x_change = car_speed
				elif event.key == pygame.K_p:
					paused()

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					x_change = 0

		x += x_change

		gameDisplay.fill(white)

		things(thing_startx, thing_starty, thing_width, thing_height, black)
		thing_starty += thing_speed

		car(x,y)
		best_display(best)
		things_dodged(dodged)

		if x < -25 or x > display_width-100: 
			x_change = 0

		if thing_starty > display_height:
			thing_starty = 0 - thing_height
			thing_startx = random.randrange(max(int(x-200), 0),min(int(x+200),display_width))
			dodged += 1
			if best < dodged:
				best = dodged
			thing_speed += 0.2
			car_speed += 0.2

		if y+5 < thing_starty+thing_height and y+128 > thing_starty:
			if x+30 >= thing_startx and x+30 <= thing_startx+thing_width or x+97 > thing_startx and x+97 < thing_startx+thing_width:
				crash()


		pygame.display.update()
		clock.tick(100)

game_intro()
game_loop()
quit_game()
