import pygame
import numpy

class Bar:
	def __init__(self, x, y, lenght = 20, width = 2, velocity = 2, orientation = 1):
		self.x = int(x)
		self.y = int(y)
		self.lenght = lenght
		self.width = width
		self.velocity = velocity
		self.orientation = orientation # 1 para horizontal, 0 para vertical

	def draw(self, screen, color = (255,255,255)):
		pygame.draw.rect(screen, color, [self.x-self.width/2, self.y-self.lenght/2, self.width, self.lenght])

	def move(self):
		lookup_table = {pygame.K_s : lambda x: x + self.velocity, # movimentamos a barra verticalmente
						pygame.K_w : lambda x: x - self.velocity} # conforme a tabela indica

		pressed = pygame.key.get_pressed()

		for k in lookup_table.keys(): # verificamos se a tecla foi apertada
			if pressed[k]:
				self.y = lookup_table[k](self.y)


class Ball:
	def __init__(self, x, y, radius, velocity):
		self.x = int(x)
		self.y = int(y)
		self.radius = radius
		self.velocity = [velocity, velocity]

	def move(self):
		self.x += self.velocity[0]
		self.y += self.velocity[1]

	def draw(self,screen,color = (255,255,255)):
		pygame.draw.circle(screen, color, [self.x, self.y], self.radius)

	def bounce(self, wall):
		lookup_table = {0:[-1,1],
						1:[1,-1]}
		if abs(self.x - wall.x) <= wall.width/2 and abs(self.y - wall.y) <= wall.lenght/2:
			self.velocity[0] *= lookup_table[wall.orientation][0]
			self.velocity[1] *= lookup_table[wall.orientation][1]