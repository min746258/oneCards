from Enviroment import Game

game = Game()

class Human_Play:
    def __init__(self):
        self.name = 'Human'
        self.hands_card = list()

    def action(self, game, player):
        while True:
            top_card = game.topCard()
