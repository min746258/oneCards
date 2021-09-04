from collections import deque
import numpy as np

# 플레이어 3명, 카드 5장으로 시작함

class Game:
    def __init__(self):
        self.card_list = [          #Diamond, Spade, Clover, Heart, Joker
            ['D', 'A'], ['D', '2'], ['D', '3'], ['D', '4'], ['D', '5'],
            ['D', '6'], ['D', '7'], ['D', '8'], ['D', '9'], ['D', '10'],
            ['D', 'J'], ['D', 'Q'], ['D', 'K'],
            ['S', 'A'], ['S', '2'], ['S', '3'], ['S', '4'], ['S', '5'],
            ['S', '6'], ['S', '7'], ['S', '8'], ['S', '9'], ['S', '10'],
            ['S', 'J'], ['S', 'Q'], ['S', 'K'],
            ['C', 'A'], ['C', '2'], ['C', '3'], ['C', '4'], ['C', '5'],
            ['C', '6'], ['C', '7'], ['C', '8'], ['C', '9'], ['C', '10'],
            ['C', 'J'], ['C', 'Q'], ['C', 'K'],
            ['H', 'A'], ['H', '2'], ['H', '3'], ['H', '4'], ['H', '5'],
            ['H', '6'], ['H', '7'], ['H', '8'], ['H', '9'], ['H', '10'],
            ['H', 'J'], ['H', 'Q'], ['H', 'K'],
            ['J', 'SC'], ['J', 'HD']]
        self.cards = deque()
        self.attack = 0
        self.top_card = ''
        self.turn = 1
        self.direction = 1
        self.state_size = len(self.state)
        self.actions = list()
        self.action_size = len(self.actions)
        self.reward = 0
        self.rewards = list()
        self.done = False
        self.state = [self.turn, self.top_card, self.attack, self.done]

    def resetGame(self):            # 게임 리셋
        self.cards = deque(self.card_list)
        np.random.shuffle(self.card_list)
        self.top_card = self.card_list.pop()
        self.deck_cards = deque(self.card_list)

    def giveCards(self, n):         # 카드 지급
        if not self.cards:
            return False
        np.random.shuffle(self.cards)
        cards = list()
        for i in range(n):
            cards.append(self.card_list.pop())
        return cards

    def find_turn(self):
        return self.turn % 3, self.direction

    def action_able(self, my_cards):  # 가능한 행동 파악
        able = list()
        for i in range(len(my_cards)):
            if my_cards[i][0] == self.top_card[0] or my_cards[i][1] == self.top_card[1] or my_cards[i][0] == 'J':
                able.append(my_cards[i])
        if able:
            return able
        else:
            return False

    def step(self, action):         # 행동 반영
        if action:
            self.cards.append(self.top_card)
            self.top_card = action
            return False
        else:
            if self.attack:
                return self.attack
            else:
                return 1

