import numpy as np
from objects import Environment
import pickle

a = 0.05 #learning rate
e = 1 #epsilon
gamma = 0.9  #fator de desconto
decay = 0.999999 #decaímento do epsilon
N_EPISODES = 800
times = []
Q = {}

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
        if s not in Q.keys(): Q[s] = [0,0,0]
        if s2 not in Q.keys(): Q[s2] = [0,0,0]        	

        Q[s][action] = Q[s][action] + a*(r + gamma*np.max(Q[s2]) - Q[s][action])
        
        s = s2
        t += 1
        e *= decay
    
    times.append(t)
    print(f'o episodio {i_episode} durou {t} steps, recompensa {total_reward:.2f}, o score terminou como {env.score[0]}x{env.score[1]}, epsilon: {e:.2f}, tamanho da tabela: {len(Q)}')
    
with open('model.pickle','wb') as pickle_out:
	pickle.dump(Q, pickle_out)

