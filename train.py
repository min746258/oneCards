from Enviroment import Game
from AI_Player import DQN_Player

P1 = DQN_Player()
P2 = DQN_Player()
P3 = DQN_Player()

P1_win = 0
P2_win = 0
P3_win = 0
draw = 0

max_learn = 20000

for i in range(max_learn):
    env = Game()

    for i in range(10000):
        player = 1
        pos = P1.policy(env)                # 행동 선택

        if env.done == 0:
            if env.reward == 0:
