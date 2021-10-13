import DQN_Player
import random
from Environment import Game

def get_card():
    data = input().split()
    return data

# P1 : AI
# P2 : Human
# P0 : Human


print('starting game!\nP1 is AI Player.')

startingCards_num = 5

env = Game()


P1 = DQN_Player.Agent(env.state_size, env.action_size)

print('please take 5 cards each')
P1_cards = [get_card() for _ in range(startingCards_num)]
done = False
winner = False

env.top_card = get_card()

for t in range(300):
    turn, direction = env.find_turn()
    action = False
    if turn == 1:               # AI turn
        print("P{} turn".format(turn))
        print(env.top_card)
        state = env.action_able(P1_cards, env.top_card)
        while True:
            if state == [0 for i in range(len(state))]:
                action = 999
                break
            action = P1.get_action(state)
            if state[action] > 0:
                break
        able = list()
        if action != 999:
            print(action)
            if action == 0:
                for i in range(len(P1_cards)):
                    if P1_cards[i][0] == env.top_card[0]:
                        able.append(P1_cards[i])
            elif action == 1:
                for i in range(len(P1_cards)):
                    if P1_cards[i][1] == env.top_card[1]:
                        able.append(P1_cards[i])
            elif action == 2:
                for i in range(len(P1_cards)):
                    if P1_cards[i][1] == 'J':
                        able.append(P1_cards[i])
                env.turn += env.direction * 2
            elif action == 3:
                for i in range(len(P1_cards)):
                    if P1_cards[i][1] == 'Q':
                        able.append(P1_cards[i])
                env.direction *= -1
            elif action == 4:
                for i in range(len(P1_cards)):
                    if P1_cards[i][1] == 'K':
                        able.append(P1_cards[i])
                env.turn += 3
            elif action == 5:
                for i in range(len(P1_cards)):
                    if P1_cards[i][1] == '3':
                        able.append(P1_cards[i])
                env.attack = 0
            elif action == 6:
                for i in range(len(P1_cards)):
                    if P1_cards[i][1] == '2':
                        able.append(P1_cards[i])
                env.attack += 2
            elif action == 7:
                for i in range(len(P1_cards)):
                    if P1_cards[i][1] == 'A':
                        able.append(P1_cards[i])
                env.attack += 3
            elif action == 8:
                for i in range(len(P1_cards)):
                    if P1_cards[i][0] == 'J':
                        able.append(P1_cards[i])
                env.attack += 5
            final_action = random.sample(able, len(able))
            print(final_action)
            env.top_card = final_action[0]
        else:
            if env.attack:
                P1_cards.extend([get_card() for _ in range(env.attack)])
                env.attack = 0
            else:
                P1_cards.append(get_card())
        if not P1_cards:
            break
    else:
        print("P{} turn".format(turn))
        action = get_card()
        print(env.top_card)
        if action == '0':
            print('passing')
            pass
        else:
            print('not passing')
            env.top_card = action

    env.turn += env.direction

print('game ended!!!')



