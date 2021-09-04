from Enviroment import Game
from Human_Player import Human_Play
from AI_Player import DQN_Player

# P1 = human()
P1 = DQN_Player()
P2 = DQN_Player()
P3 = DQN_Player()

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

# P1은 무조건 Human, P3은 무조건 AI
env.resetGame()
P1.cards = env.giveCards(startingCards_num)
P2.cards = env.giveCards(startingCards_num)
P3.cards = env.giveCards(startingCards_num)
done = False
winner = False

for t in range(10000):
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
        # epsilon = P3.get_epsilon(game + 1)
        # action = P3.greed_search(epsilon, game, Q)
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
