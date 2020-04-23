import numpy as np

class Bar:
	def __init__(self, x, y, lenght = 20, width = 2, velocity = 2, orientation = 1):
		self.x = int(x)
		self.y = int(y)
		self.lenght = lenght
		self.width = width
		self.velocity = velocity
		self.orientation = orientation # 1 para horizontal, 0 para vertical


	def move(self, mode='human', move=None, ball = None): #mode = (human, machine, enemy); move = (0,1,2)
		lookup_table = {
						1 : lambda x: x + self.velocity, # movimentamos a barra verticalmente
						2 : lambda x: x - self.velocity} # conforme a tabela indica

		# modos de movimento: o mode 'human' serve para o controle manual,
		# 'machine' diz respeito ao environment e o 'enemy' serve para controlar
		# a barra inimiga

		if mode == 'machine':
			if move != 0:
				self.y = lookup_table[move](self.y)
			if self.y > 600-self.lenght//2:
				self.y = 600 - self.lenght//2
			if self.y < 0+self.lenght//2:
				self.y = self.lenght//2

		elif mode == 'enemy':
			if self.y != ball.y and np.random.random() < .6 and ball.x >= 400: vec = ((ball.y - self.y)/abs(ball.y - self.y))
			else: vec = 0
			self.y += self.velocity*vec


class Ball:
	def __init__(self, x, y, radius):
		self.x = int(x)
		self.y = int(y)
		self.radius = radius
		rr = [(0.75,1.5),(-1,1),(1.5,0.75),(1,0.5)]
		r = np.random.choice(range(len(rr)))
		self.velocity = [rr[r][0],rr[r][1]]

	def move(self):
		self.x = self.x + self.velocity[0]
		self.y = self.y + self.velocity[1]

	def bounce(self, wall):
		lookup_table = {0:[-1,1],
						1:[1,-1]}
		if abs(self.x - wall.x) <= wall.width/2 and abs(self.y - wall.y) <= wall.lenght/2:
			self.velocity[0] *= lookup_table[wall.orientation][0]
			self.velocity[1] *= lookup_table[wall.orientation][1]

class Environment:
	def __init__(self, HEIGHT=600, WIDTH=800, bar_velocity=3, max_steps = 1000000):

		bar_parameters = [(15,50,100,5,bar_velocity,0),(WIDTH-15,50,100,5,5,0),
				  (WIDTH/2,0,2,WIDTH,0,1),(WIDTH/2,HEIGHT,2,WIDTH,0,1),
				  (0,HEIGHT/2,HEIGHT,2,0,0),(WIDTH,HEIGHT/2,HEIGHT,2,0,0)]

		self.HEIGHT = HEIGHT
		self.WIDTH = WIDTH
		self.max_steps = max_steps
		self.rendered = False

		self.bars = []
		for bar in bar_parameters:
			self.bars.append(Bar(bar[0],bar[1],bar[2],bar[3],bar[4],orientation=bar[-1]))
		self.control_bar = self.bars[0]
		self.other_bar = self.bars[1]

		self.ball = Ball(WIDTH/2,HEIGHT/2,10) #x inicial; y inicial; raio

	def reset(self):
		
		self.ball.x, self.ball.y = self.WIDTH/2, self.HEIGHT/2
		self.steps = 0
		self.control_bar.x, self.control_bar.y = 15,50
		self.other_bar.x, self.other_bar.y = self.WIDTH - 15,50
		rr = [(0.75,1.5),(-1,1),(1.5,0.75),(1,0.5)]
		r = np.random.choice(range(len(rr)))
		self.ball.velocity = [rr[r][0],rr[r][1]]
		self.done = False
		self.score = [0,0]
		return ((self.control_bar.y - self.ball.y))

	def step(self,action):

		reward = 0
		self.steps += 1
		self.control_bar.move(mode='machine',move=action)
		self.other_bar.move(mode='enemy',ball=self.ball)
		self.ball.move()

		for bar in self.bars:
			self.ball.bounce(bar)

		if self.ball.x <= 4:

			self.ball.x, self.ball.y = self.WIDTH/2, self.HEIGHT/2
			self.control_bar.x, self.control_bar.y = 15,50
			self.other_bar.x, self.other_bar.y = self.WIDTH - 15,50

			self.score[1] += 1
			reward = -500
			if self.score[-1] >= 5: self.done = True; reward -= 5000

		elif self.ball.x >= self.WIDTH - 4:

			self.ball.x, self.ball.y = self.WIDTH/2, self.HEIGHT/2
			self.control_bar.x, self.control_bar.y = 15,50
			self.other_bar.x, self.other_bar.y = self.WIDTH - 15,50

			self.score[0] += 1
			reward = +500
			if self.score[0] >= 5: self.done = True; reward += 5000

		if self.control_bar.y > self.HEIGHT or self.control_bar.y < 0 or self.steps >= self.max_steps:
			reward = -1000
			self.done = True
		return (int(self.control_bar.y - self.ball.y),1 + reward,self.done,'_')
a = 0.01 #learning rate
e = 1 #epsilon
gamma = 0.9  #fator de desconto
decay = 0.999999 #decaímento do epsilon
N_EPISODES = 500
times = []
Q = {} # keys: estados; values: valor atribuido à cada ação

env = Environment()
for i_episode in range(N_EPISODES):
    
    s = env.reset()
    done = False
    t = 0
    total_reward = 0
    
    while not done:
        #politica
        if np.random.random() < e:
            action = np.random.choice([0,1,2])
        else:
            action = np.argmax(Q[s])
        #A ação é tomada e os valores novos são coletados
        s2, r, done, info = env.step(action)
        total_reward += r
        #O novo estado é salvo numa nova variavel
        #equação de Bellman
        if s not in Q.keys(): Q[s] = [0,0,0] # para cada estado ainda não descoberto, iniciamos seu valor como nulo
        if s2 not in Q.keys(): Q[s2] = [0,0,0]        	

        Q[s][action] = Q[s][action] + a*(r + gamma*np.max(Q[s2]) - Q[s][action])
        
        s = s2
        t += 1
        e *= decay
    
    times.append(t)
    print(f'o episodio {i_episode} durou {t} steps, recompensa {total_reward:.2f}, o score terminou como {env.score[0]}x{env.score[1]}, epsilon: {e:.2f}, tamanho da tabela: {len(Q)}')
    