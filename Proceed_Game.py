from Environment import Game
from DQN_Player import *

# P1 = human
# P2 = ?
# P3 = AI

startingCards_num = 5

env = Game()
env.resetGame()

P3 = Agent(env.state_size, env.action_size)

P1_cards = env.giveCards(startingCards_num)
P2_cards = env.giveCards(startingCards_num)
P3_cards = env.giveCards(startingCards_num)
done = False
winner = False

for t in range(300):
    turn, direction = env.state()
    action = False

    if turn == 1:
        print('현재 카드 : {}'.format(P1_cards))
        able = env.getAction(P1_cards)
        if able:
            print('가능한 카드 : {}'.format(able))
            action = able[int(input('행동을 선택해주세요(배열 인덱스 입력) : '))]
        else:
            print('낼 수 있는 카드가 없으므로', end='')
        result = env.play(action)
        if result:
            add = env.giveCards(result)
            print('카드 {}장을 가져옵니다'.format(len(add)))
            print('가져갈 카드 : {}'.format(add))
            P1_cards.append(add)
        if not P1_cards:
            winner = 1
            done = True
    elif turn == 2:
        pass
    elif turn == 3:
        state = env.action_able(P3_cards)
        action = P3.get_action(state)
        able = list()
        if action:
            if action == 0:
                for i in range(len(P3_cards)):
                    if P3_cards[i][0] == env.top_card[0]:
                        able.append(P3_cards[i])
            elif action == 1:
                for i in range(len(P3_cards)):
                    if P3_cards[i][1] == env.top_card[1]:
                        able.append(P3_cards[i])
            elif action == 2:
                for i in range(len(P3_cards)):
                    if P3_cards[i][1] == 'J':
                        able.append(P3_cards[i])
                env.turn += env.direction * 2
            elif action == 3:
                for i in range(len(P3_cards)):
                    if P3_cards[i][1] == 'Q':
                        able.append(P3_cards[i])
                env.direction *= -1
            elif action == 4:
                for i in range(len(P3_cards)):
                    if P3_cards[i][1] == 'K':
                        able.append(P3_cards[i])
                env.turn += 3
            elif action == 5:
                for i in range(len(P3_cards)):
                    if P3_cards[i][1] == '3':
                        able.append(P3_cards[i])
                env.attack = 0
            elif action == 6:
                for i in range(len(P3_cards)):
                    if P3_cards[i][1] == '2':
                        able.append(P3_cards[i])
                env.attack += 2
            elif action == 7:
                for i in range(len(P3_cards)):
                    if P3_cards[i][1] == 'A':
                        able.append(P3_cards[i])
                env.attack += 3
            elif action == 8:
                for i in range(len(P3_cards)):
                    if P3_cards[i][0] == 'J':
                        able.append(P3_cards[i])
                env.attack += 5
            final_action = random.sample(able)
            env.step(final_action)
        else:
            if env.attack:
                P3_cards += env.giveCards(env.attack)
                env.attack = 0
            else:
                P3_cards.append(env.giveCards(1)[0])
        if not P3.cards:
            winner = 3
            done = True


    if done:
        if winner == 1:
            print('winner is P1')
        elif winner == 2:
            print('winner is P2')
        elif winner == 3:
            print('winner is P3')
        else:
            print('draw')
        break

    env.turn += env.direction
