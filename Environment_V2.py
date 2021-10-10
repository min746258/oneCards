from collections import deque
import numpy as np

# 플레이어 3명, 카드 5장으로 시작함
# 문양은 스페이드, 하트 등을 의미함
# 모양은 J,Q,K 등을 의미함

class Game:
    def __init__(self):
        self.card_list = [          #Diamond, Spade, Clover, Heart, Joker=0
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
            ['0', 'B'], ['0', 'C']]
        self.cards = deque()
        # self.special_card = ['J', 'Q', 'K', '2', 'A', 'J']
        self.attack = 0
        self.top_card = ''
        self.shape = '0'             # D, S, C, H, 0(조커/Default)
        self.turn = 1000
        self.direction = 1
        # self.state = [0 for _ in range(8)]
        self.state_size = len(self.state)
        self.actions = self.state
        self.action_size = len(self.actions)
        self.reward = 0
        self.rewards = list()
        self.done = False

    def resetGame(self):            # 게임 리셋
        self.attack = 0
        self.turn = 1000
        self.direction = 1
        self.cards = deque(self.card_list)
        np.random.shuffle(self.card_list)
        self.top_card = self.cards.pop()

    def giveCards(self, n):         # 카드 지급 // 구현오 작업
        if not self.cards:
            return False
        elif len(self.cards) < n:
            return False
        np.random.shuffle(self.cards)
        give = list()
        for i in range(n):
            give.append(self.cards.pop())
        return give

    def find_turn(self):            # 플레이어 순서, 방향 파악
        return self.turn % 3, self.direction

    def action_able(self, my_cards):  # 가능한 행동 파악(낼 수 있는 카드 개수 의미함)
        able = [0 for _ in range(8)]            # [일반카드, J(특수), Q(특수), K(특수), 3(방어), 2(공격), A(공격), 조커(공격)]
        if self.attack > 0:
            for i in range(len(my_cards)):
                if self.shape == '0':
                    if my_cards[i][0] == '0':
                        able[7] += 1
                    elif my_cards[i][1] == '3':
                        able[4] += 1
                elif self.top_card[1] == '2':
                    if my_cards[i][1] == '2':
                        able[5] += 1
                    elif my_cards[i][1] == 'A' and my_cards[i][0] == self.shape:
                        able[6] += 1
                    elif my_cards[i][0] == '0':
                        able[7] += 1
                    elif my_cards[i][1] == '3' and my_cards[i][0] == self.shape:
                        able[4] += 1
                elif self.top_card[1] == 'A':
                    if my_cards[i][1] == 'A':
                        able[6] += 1
                    elif my_cards[i][0] == '0':
                        able[7] += 1
                    elif my_cards[i][1] == '3' and my_cards[i][0] == self.shape:
                        able[4] += 1
        else:
            for i in range(len(my_cards)):
                if my_cards[i][0] == '0':
                    able[7] += 1
                if self.shape == '0':           # 조커 낸 후
                    if my_cards[i][1] == 'J':
                        able[1] += 1
                    elif my_cards[i][1] == 'Q':
                        able[2] += 1
                    elif my_cards[i][1] == 'K':
                        able[3] += 1
                    elif my_cards[i][1] == '3':
                        able[4] += 1
                    elif my_cards[i][1] == '2':
                        able[5] += 1
                    elif my_cards[i][1] == 'A':
                        able[6] += 1
                    else:
                        able[0] += 1
                elif self.shape == my_cards[i][0]:      # 문양 같은 경우
                    if my_cards[i][1] == 'J':
                        able[1] += 1
                    elif my_cards[i][1] == 'Q':
                        able[2] += 1
                    elif my_cards[i][1] == 'K':
                        able[3] += 1
                    elif my_cards[i][1] == '3':
                        able[4] += 1
                    elif my_cards[i][1] == '2':
                        able[5] += 1
                    elif my_cards[i][1] == 'A':
                        able[6] += 1
                    else:
                        able[0] += 1

                elif self.top_card[1] == my_cards[i][1]:        # 종류 같은 경우
                    if my_cards[i][1] == 'J':
                        able[1] += 1
                    elif my_cards[i][1] == 'Q':
                        able[2] += 1
                    elif my_cards[i][1] == 'K':
                        able[3] += 1
                    elif my_cards[i][1] == '3':
                        able[4] += 1
                    elif my_cards[i][1] == '2':
                        able[5] += 1
                    elif my_cards[i][1] == 'A':
                        able[6] += 1
                    else:
                        able[0] += 1
        if able == [0 for _ in range(8)]:
            return False
        return able

    def shape_able(self, my_cards, able):
        able.pop()
        for n in able:
            if n > 1:
                for i in range(len(my_cards)):


    def step(self, action):         # 행동 반영
        self.cards.append(self.top_card)
        self.top_card = action
