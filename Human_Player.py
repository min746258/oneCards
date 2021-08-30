from Enviroment import Game

sit = Game()

class Human_Play:
    def __init__(self):
        self.name = 'Human'
        self.hands_card = list()

    def action(self, sit, player):
        while True:
            top_card = sit.topCard()
