# 이상민 작업

from Environment import Game
from DQN_Player import *
from tqdm import tqdm
# import matplotlib.pyplot as plt

if __name__ == '__main__':

    env = Game()                                                            # 게임 모듈 호출
    state_size = env.state_size
    action_size = env.action_size

    agent = Agent(state_size, action_size)                                  # 게임 플레이어 모듈 호출

    scores, episodes = list(), list()
    score_avg = 0

    episode_num = int(input('how many games? : '))                          # 학습할 에피소드 횟수 입력

    startingCards_num = int(input('How many cards to start with? : '))      # 시작할 카드 수 입력

    P1_win = 0                                                              # 승수 초기화
    P2_win = 0
    P3_win = 0
    draw = 0

    P1_reward_log = list()                                                     # 게임 결과 플레이어별로 저장
    P2_reward_log = list()                                                     # 나중에 학습 결과에 참고하기 위함
    P3_reward_log = list()
    draw_log = list()

    for game in tqdm(range(episode_num)):
        env.resetGame()
        P1_cards = env.giveCards(startingCards_num)                         # 처음에 카드 지급
        P2_cards = env.giveCards(startingCards_num)
        P3_cards = env.giveCards(startingCards_num)

        done = False                                                        # 상태 초기화
        winner = False
        next_state = False
        P1_reward = 0
        P2_reward = 0
        P3_reward = 0
        loss_log = list()

        for t in range(300):
            if env.turn % 3 == 1:                                           # P1 차례
                state = env.action_able(P1_cards)                           # 상태 정보 반환
                if not state:                                               # 행동을 취할 수 없는 상태라면
                    if env.attack:                                          # 공격받는 상태라면
                        if len(env.cards) >= env.attack:                    # 카드를 가져올 수 있다면 가져온다
                            P1_cards += env.giveCards(env.attack)
                        else:                                               # 카드를 가져올 수 없다면 무승부
                            draw += 1
                            break
                        P2_reward += env.attack + 1
                        P3_reward += env.attack + 1
                        env.attack = 0
                        continue
                    else:                                                   # 공격받는 상태가 아니라면
                        if env.cards:                                       # 카드를 가져올 수 있다면 가져온다
                            P1_cards.append(env.giveCards(1)[0])
                        else:                                               # 카드를 가져올 수 없다면 무승부
                            draw += 1
                            break
                        P2_reward += 1
                        P3_reward += 1
                    env.turn += env.direction
                    continue
                while True:
                    action = agent.get_action(state)                        # 취할 행동을 정한다. 할 수 있는 행동이 반환될
                    if state[action] == 1:                                  # 때까지 반복하고, 보상이 -1000인 샘플을 추가함
                        break
                    else:
                        agent.append_sample(state, action, -1000, [0 for _ in range(9)], False)

                print('P1 action : ', action)
                able = list()
                if action == 0:                                             # 취한 행동 따라 낼 수 있는 카드 파악
                    for i in range(len(P1_cards)):
                        if P1_cards[i][0] == env.top_card[0] and P1_cards[i][1] not in env.special_card:
                            able.append(P1_cards[i])
                        elif env.top_card[0] == 'J' and P1_cards[i][1] not in env.special_card:
                            able.append(P1_cards[i])
                elif action == 1:
                    for i in range(len(P1_cards)):
                        if P1_cards[i][1] == env.top_card[1] and P1_cards[i][1] not in env.special_card:
                            able.append(P1_cards[i])
                elif action == 2:
                    for i in range(len(P1_cards)):
                        if P1_cards[i][1] == 'J':
                            able.append(P1_cards[i])
                    P1_reward += 1
                    env.turn += env.direction
                elif action == 3:
                    for i in range(len(P1_cards)):
                        if P1_cards[i][1] == 'Q':
                            able.append(P1_cards[i])
                    env.direction *= -1
                elif action == 4:
                    for i in range(len(P1_cards)):
                        if P1_cards[i][1] == 'K':
                            able.append(P1_cards[i])
                    P1_reward += 2
                    env.turn += 2
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
                print('P1 able : ', able)
                if len(able) > 1:                                           # 낼 수 있는 카드가 여러 개라면 무작위로 선택
                    final_action = random.sample(able, 1)[0]
                else:
                    final_action = able[0]

                print('1 final action : ', final_action)
                env.step(final_action)                                      # 행동을 게임 환경에 반영
                P1_cards.remove(final_action)                               # 낸 카드를 가지고 있는 카드 목록에서 제거
                if next_state:
                    agent.append_sample(state, action, P1_reward, next_state, done)         # 플래시 메모리에 샘플 추가
                P1_reward = 0
                if len(agent.memory) >= agent.train_start:
                    agent.train_model()                                     # 인공지능 모델 훈련
                    loss_log.append(agent.loss)
                next_state = state
                if not P1_cards:                                            # 가진 카드 없다면 --> 승리!
                    done = True
                    P1_win += 1
                    P1_reward += 200
                    P2_reward -= 100
                    P3_reward -= 100
                    agent.append_sample(state, action, 200, next_state, done)
                    break

            elif env.turn % 3 == 2:             # P2(P1과 구조 동일하므로 주석 달지 않았음)
                print('\nP2 turn')
                state = env.action_able(P2_cards)
                print('P2 state : ', state)
                if not state:
                    if env.attack:
                        if len(env.cards) >= env.attack:
                            P2_cards += env.giveCards(env.attack)
                        else:
                            break
                        P1_reward += env.attack + 1
                        P3_reward += env.attack + 1
                        env.attack = 0
                    else:
                        if env.cards:
                            P2_cards.append(env.giveCards(1)[0])
                        else:
                            break
                        P1_reward += 1
                        P3_reward += 1
                    env.turn += env.direction
                    continue
                while True:
                    action = agent.get_action(state)
                    if state[action] == 1:
                        break
                    else:
                        agent.append_sample(state, action, -1000, [0 for _ in range(9)], False)

                print('P2 action : ', action)
                able = list()

                if action == 0:
                    for i in range(len(P2_cards)):
                        if P2_cards[i][0] == env.top_card[0] and P2_cards[i][1] not in env.special_card:
                            able.append(P2_cards[i])
                        elif env.top_card[0] == 'J' and P2_cards[i][1] not in env.special_card:
                            able.append(P2_cards[i])

                elif action == 1:
                    for i in range(len(P2_cards)):
                        if P2_cards[i][1] == env.top_card[1] and P2_cards[i][1] not in env.special_card:
                             able.append(P2_cards[i])
                elif action == 2:
                    for i in range(len(P2_cards)):
                        if P2_cards[i][1] == 'J':
                            able.append(P2_cards[i])
                    P2_reward += 1
                    env.turn += env.direction
                elif action == 3:
                    for i in range(len(P2_cards)):
                        if P2_cards[i][1] == 'Q':
                            able.append(P2_cards[i])
                    env.direction *= -1
                elif action == 4:
                    for i in range(len(P2_cards)):
                        if P2_cards[i][1] == 'K':
                            able.append(P2_cards[i])
                    P2_reward += 2
                    env.turn += 2
                elif action == 5:
                    for i in range(len(P2_cards)):
                        if P2_cards[i][1] == '3':
                            able.append(P2_cards[i])
                    env.attack = 0
                elif action == 6:
                    for i in range(len(P2_cards)):
                        if P2_cards[i][1] == '2':
                            able.append(P2_cards[i])
                    env.attack += 2
                elif action == 7:
                    for i in range(len(P2_cards)):
                        if P2_cards[i][1] == 'A':
                            able.append(P2_cards[i])
                    env.attack += 3
                elif action == 8:
                    for i in range(len(P2_cards)):
                        if P2_cards[i][0] == 'J':
                            able.append(P2_cards[i])
                    env.attack += 5
                print('P2 able : ', able)
                if len(able) > 1:
                    final_action = random.sample(able, 1)[0]
                else:
                    final_action = able[0]
                P2_cards.remove(final_action)
                print('P2 final action : ', final_action)
                env.step(final_action)
                if next_state:
                    agent.append_sample(state, action, P2_reward, next_state, done)
                P2_reward = 0
                if len(agent.memory) >= agent.train_start:
                    agent.train_model()
                    loss_log.append(agent.loss)
                next_state = state
                if not P2_cards:
                    done = True
                    P2_win += 1
                    P2_reward += 200
                    P1_reward -= 100
                    P3_reward -= 100
                    agent.append_sample(state, action, 200, next_state, done)
            else:           # P3(P1과 구조 동일하므로 주석 달지 않았음)
                print('\nP3 turn')
                state = env.action_able(P3_cards)
                print('P3 state : ', state)
                if not state:
                    if env.attack:
                        if len(env.cards) >= env.attack:
                            P3_cards += env.giveCards(env.attack)
                        else:
                            break
                        P1_reward += env.attack + 1
                        P3_reward += env.attack + 1
                        env.attack = 0
                    else:
                        if env.cards:
                            P3_cards.append(env.giveCards(1)[0])
                        else:
                            break
                        P1_reward += 1
                        P2_reward += 1
                    env.turn += env.direction
                    continue
                while True:
                    action = agent.get_action(state)
                    if state[action] == 1:
                        break
                    else:
                        agent.append_sample(state, action, -1000, [0 for _ in range(9)], False)
                print('P3 action : ', action)
                able = list()

                if action == 0:
                    for i in range(len(P3_cards)):
                        if P3_cards[i][0] == env.top_card[0] and P3_cards[i][1] not in env.special_card:
                            print('action0_normal')
                            able.append(P3_cards[i])
                        elif env.top_card[0] == 'J' and P3_cards[i][1] not in env.special_card:
                            print('action0_joker')
                            able.append(P3_cards[i])
                elif action == 1:
                    for i in range(len(P3_cards)):
                        if P3_cards[i][1] == env.top_card[1] and P3_cards[i][1] not in env.special_card:
                            able.append(P3_cards[i])
                elif action == 2:
                    for i in range(len(P3_cards)):
                        if P3_cards[i][1] == 'J':
                            able.append(P3_cards[i])
                    P3_reward += 1
                    env.turn += env.direction
                elif action == 3:
                    for i in range(len(P3_cards)):
                        if P3_cards[i][1] == 'Q':
                            able.append(P3_cards[i])
                    env.direction *= -1
                elif action == 4:
                    for i in range(len(P3_cards)):
                        if P3_cards[i][1] == 'K':
                            able.append(P3_cards[i])
                    P3_reward += 2
                    env.turn += 2
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
                print('P3 able : ', able)
                if len(able) > 1:
                    final_action = random.sample(able, 1)[0]
                else:
                    final_action = able[0]
                P3_cards.remove(final_action)
                print('P3 final action : ', final_action)
                env.step(final_action)
                if next_state:
                    agent.append_sample(state, action, P3_reward, next_state, done)
                P3_reward = 0
                if len(agent.memory) >= agent.train_start:
                    agent.train_model()
                    loss_log.append(agent.loss)
                next_state = state
                if not P3_cards:
                    done = True
                    P3_win += 1
                    P3_reward += 200
                    P1_reward -= 100
                    P2_reward -= 100
                    agent.append_sample(state, action, 200, next_state, done)

            if done:                                    # 게임이 종료되었다면 --> 현재 신경망의 가중치를 타겟 신경망의 가중치에 복사
                agent.update_target_model()
                break

            env.turn += env.direction

        # print(P1_win, P2_win, P3_win, draw)
        # P1_reward_log.append(P1_reward)
        # P2_reward_log.append(P2_reward)
        # P3_reward_log.append(P3_reward)
        # draw_log.append(draw)

        # print('P1 win : {0:0.2f}% | P2 win : {0:0.2f}% | P3 win : {0:0.2f}% | draw :  {0:0.2f}%'
              # .format(P1_win/game*100, P2_win/game*100, P3_win/game*100, draw/game*100))

print(P1_win, P2_win, P3_win, draw)                                 # 총 게임 결과 출력
game_num = [i for i in range(len(loss_log))]
plt.plot(game_num, loss_log, 'r')
# plt.plot(game_num, P2_reward_log, 'g')
# plt.plot(game_num, P3_reward_log, 'b')
plt.show()                                                          # 총 게임 결과 그래프로 출력
agent.model.save_weights(".save_model/model", save_format="tf")     # 학습한 모델 저장
print('done!')