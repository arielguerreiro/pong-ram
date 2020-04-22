import pickle
import numpy as np
from objects import Environment

def load_table(file):
	with open(file, 'rb') as pickle_in:
		Q = pickle.load(pickle_in)
	return Q

env = Environment()
Q = load_table('model.pickle')

NUMBER_OF_EPISODES = 5

for i in range(NUMBER_OF_EPISODES):
	done = False
	s = env.reset()
	while not done:
		action = np.argmax(Q[s])
		s2, reward, done, _ = env.step(action)
		env.render()
		s = s2

