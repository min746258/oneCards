from Enviroment import Game
from Human_Player import Human_Play
from AI_Player import AI_Play

#P1 = human()
P1 = AI_Play()
P2 = AI_Play()
P3 = AI_Play()

auto = True

games = 250
print('P1 player : {}'.format(P1.name))
print('P2 player : {}'.format(P2.name))
print('P3 player : {}'.format(P3.name))

P1_win = 0
P2_win = 0
P3_win = 0
draw = 0

if auto:
    for j in range(games):
        game = Game()
        game.startGame()
        P1.hands_card = game.giveCards(5)
        P2.hands_card = game.giveCards(5)
        P3.hands_card = game.giveCards(5)
        for i in range(10000):
            #reward, done =
            if done == True:
                if reward == 1:
                    print('winner is P1({})'.format(P1.name))
                elif reward == 2:
                    print('winner is P2({})'.format(P2.name))
                elif reward == 3:
                    print('winner is P3({})'.format(P3.name))
                else:
                    print('draw')
                break
    answer = input("More Game? (Y/N)")
else:
    while True:
        game = Game()
        game.print = True
        for i in range(10000):
            #reward, done =
            if done == True:
                if reward == 1:
                    print('winner is P1({})'.format(P1.name))
                elif reward == 2:
                    print('winner is P2({})'.format(P2.name))
                elif reward == 3:
                    print('winner is P3({})'.format(P3.name))
                else:
                    print('draw')
                break
print('P1 win : {} / P2 win : {} / P3 win : {} / draw : {}'
      .format(P1_win, P2_win, P3_win, draw))