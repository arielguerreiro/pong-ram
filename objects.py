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

	def move(self, mode='human', move=None): #mode = (human, machine, enemy); move = (0,1,2)
		lookup_table = {pygame.K_s : lambda x: x + self.velocity,
						1 : lambda x: x + self.velocity, # movimentamos a barra verticalmente
						pygame.K_w : lambda x: x - self.velocity,
						2 : lambda x: - + self.velocity} # conforme a tabela indica

		pressed = pygame.key.get_pressed()

		if mode == 'human':
			for k in lookup_table.keys(): # verificamos se a tecla foi apertada
				if pressed[k]:
					self.y = lookup_table[k](self.y)

		elif mode == 'machine':
			if move != 0:
				self.y = lookup_table[move](self.y)



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

class Environment:
	def __init__(self, HEIGHT=600, WIDTH=800, bar_velocity=2, ball_velocity=1):
		bar_parameters = [(15,50,100,5,bar_velocity,0),(WIDTH-15,50,100,5,bar_velocity,0),
				  (WIDTH/2,0,2,WIDTH,0,1),(WIDTH/2,HEIGHT,2,WIDTH,0,1),
				  (0,HEIGHT/2,HEIGHT,2,0,0),(WIDTH,HEIGHT/2,HEIGHT,2,0,0)]

		self.bars = []
		for bar in bar_parameters:
			bars.append(Bar(bar[0],bar[1],bar[2],bar[3],bar[4],orientation=bar[-1]))
		self.control_bar = bars[0]
		self.other_bar = bars[1]

		self.ball = Ball(WIDTH/2,HEIGHT/2,10,ball_velocity) #x inicial; y inicial; raio; velocidade
		self.score = [0,0]
		self.done = False

	def reset(self):
		return ([self.control_bar.x, self.control_bar.y, self.ball.x, self.ball.y, self.ball.velocity], 0, self.done, '_')

	def step(self,action):
		self.control_bar.move(mode='machine',move=action)
		self.other_bar.move() # adicionar o movimento da outra barra
		self.ball.move()
		for bar in self.bars:
			self.ball.bounce(bar)
		# adicionar score e condição de finalização
		return ([self.control_bar.x, self.control_bar.y, self.ball.x, self.ball.y, self.ball.velocity], reward, self.done, '_')

