import pygame
from objects import *

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH,HEIGHT))

bar_parameters = [(15,50,100,5,0),(WIDTH-15,50,100,5,0),
				  (WIDTH/2,0,2,WIDTH,1),(WIDTH/2,HEIGHT,2,WIDTH,1),
				  (0,HEIGHT/2,HEIGHT,2,0),(WIDTH,HEIGHT/2,HEIGHT,2,0)]

bars = []
for bar in bar_parameters:
	bars.append(Bar(bar[0],bar[1],bar[2],bar[3], orientation=bar[-1]))
control_bar = bars[0]

ball = Ball(WIDTH/2,HEIGHT/2,10,1) #x inicial; y inicial; raio; velocidade

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	screen.fill((255,100,100))

	for bar in bars:
		bar.draw(screen)
		ball.bounce(bar)
	ball.draw(screen)
	ball.move()
	control_bar.move()

	pygame.display.update()




