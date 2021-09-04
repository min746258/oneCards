from Enviroment import Game
from Human_Player import Human_Play
from AI_Player import DQN_Player
from tqdm import tqdm

# P1 = human()
P1 = DQN_Player()
P2 = DQN_Player()
P3 = DQN_Player()

auto = True

games = 250
print('P1 player : {}'.format(P1.name))
print('P2 player : {}'.format(P2.name))
print('P3 player : {}'.format(P3.name))

startingCards_num = 5

P1_win = 0
P2_win = 0
P3_win = 0
draw = 0

env = Game()

for game in tqdm(range(games)):                     # game = episode
    env.resetGame()

    P1.cards = env.giveCards(startingCards_num)
    P2.cards = env.giveCards(startingCards_num)
    P3.cards = env.giveCards(startingCards_num)

    done = False
    winner = False

    for t in range(10000):
        turn, direction = env.state()
        if turn == 1:
            epsilon = P1.get_epsilon(game+1)
            action = P1.greed_search(epsilon, game, Q)
            result = env.play(action)
            if result:
                add = env.giveCards(result)
                P1.cards.append(add)
            if not P1.cards:
                P1_win += 1
                winner = 1
                done = True
        elif turn == 2:
            epsilon = P2.get_epsilon(game + 1)
            action = P2.greed_search(epsilon, game, Q)
            result = env.play(action)
            if result:
                add = env.giveCards(result)
                P2.cards.append(add)
            if not P2.cards:
                P2_win += 1
                winner = 2
                done = True
        elif turn == 3:
            epsilon = P3.get_epsilon(game + 1)
            action = P3.greed_search(epsilon, game, Q)
            result = env.play(action)
            if result:
                add = env.giveCards(result)
                P3.cards.append(add)
            if not P3.cards:
                P3_win += 1
                winner = 3
                done = True

        if done:
            if winner == 1:
                print('winner is P1({})'.format(P1.name))
            elif winner == 2:
                print('winner is P2({})'.format(P2.name))
            elif winner == 3:
                print('winner is P3({})'.format(P3.name))
            else:
                print('draw')
            break

print('P1 win : {} / P2 win : {} / P3 win : {} / draw : {}'.format(P1_win, P2_win, P3_win, draw))
