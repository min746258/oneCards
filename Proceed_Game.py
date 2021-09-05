from Environment import Game
from DQN_Player import *

# P1 = human
# P2 = ?
# P3 = AI
P3 = Agent()

startingCards_num = 5

env = Game()
env.resetGame()

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
        result = env.step(action)
        if result:
            # add = env.giveCards(result)
            P3_cards.append(add)
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
