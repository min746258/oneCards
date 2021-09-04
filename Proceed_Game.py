from Enviroment import Game
from DDQN_Player import *

# P1 = human
# P2 = ?
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
        print('현재 카드 : {}'.format(P1.cards))
        able = env.getAction(P1.cards)
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
            P1.cards.append(add)
        if not P1.cards:
            P1_win += 1
            winner = 1
            done = True
    elif turn == 2:
        pass
    elif turn == 3:
        action =
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
