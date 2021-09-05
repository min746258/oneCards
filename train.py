from Environment import Game
from DQN_Player import *
from tqdm import tqdm

if __name__ == '__main__':
    env = Game()
    state_size = env.state_size
    action_size = env.action_size

    agent = Agent(state_size, action_size)

    scores, episodes = list(), list()
    score_avg = 0

    episode_num = 600

    startingCards_num = 5

    P1_win = 0
    P2_win = 0
    P3_win = 0
    draw = 0

    for game in tqdm(range(episode_num)):
        env.resetGame()
        P1_cards = env.giveCards(startingCards_num)
        P2_cards = env.giveCards(startingCards_num)
        P3_cards = env.giveCards(startingCards_num)

        done = False
        winner = False
        next_state = False
        P1_reward = 0
        P2_reward = 0
        P3_reward = 0

        for t in range(300):
            print('\n\n', env.turn)
            print('P1 : ', P1_cards)
            print('P2 : ', P2_cards)
            print('P3 : ', P3_cards)
            print('top card : ', env.top_card)
            print('attack : ', env.attack)

            if env.turn % 3 == 1:           # P1
                print('\nP1 turn')
                state = env.action_able(P1_cards)
                print('P1 state : ', state)
                if not state:
                    if env.attack:
                        P1_cards += env.giveCards(env.attack)
                        P2_reward += env.attack + 1
                        P3_reward += env.attack + 1
                        env.attack = 0
                    else:
                        P1_cards.append(env.giveCards(1)[0])
                        P2_reward += 1
                        P3_reward += 1
                    env.turn += env.direction
                    continue
                while True:
                    action = agent.get_action(state)
                    if state[action] == 1:
                        break

                print('P1 action : ', action)
                able = list()
                if action == 0:
                    for i in range(len(P1_cards)):
                        if P1_cards[i][0] == env.top_card[0]:
                            able.append(P1_cards[i])
                elif action == 1:
                    for i in range(len(P1_cards)):
                        if P1_cards[i][1] == env.top_card[1]:
                            able.append(P1_cards[i])
                elif action == 2:
                    for i in range(len(P1_cards)):
                        if P1_cards[i][1] == 'J':
                            able.append(P1_cards[i])
                    P1_reward += 1
                    env.turn += env.direction * 2
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
                    print('K')
                    env.turn += 3
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
                if len(able) > 1:
                    final_action = random.sample(able, 1)[0]
                else:
                    final_action = able[0]

                print('1 final action : ', final_action)
                env.step(final_action)
                P1_cards.remove(final_action)
                if next_state:
                    agent.append_sample(state, action, P1_reward, next_state, done)
                P1_reward = 0
                if len(agent.memory) >= agent.train_start:
                    agent.train_model()
                next_state = state
                if not P1_cards:
                    done = True
                    P1_win += 1
                    agent.append_sample(state, action, 100, next_state, done)
                    break

            elif env.turn % 3 == 2:             # P2
                print('\nP2 turn')
                state = env.action_able(P2_cards)
                print('P2 state : ', state)
                if not state:
                    if env.attack:
                        P2_cards += env.giveCards(env.attack)
                        P1_reward += env.attack + 1
                        P3_reward += env.attack + 1
                        env.attack = 0
                    else:
                        P2_cards.append(env.giveCards(1)[0])
                        P1_reward += 1
                        P3_reward += 1
                    env.turn += env.direction
                    continue
                while True:
                    action = agent.get_action(state)
                    if state[action] == 1:
                        break

                print('P2 action : ', action)
                able = list()

                if action == 0:
                    for i in range(len(P2_cards)):
                        if P2_cards[i][0] == env.top_card[0]:
                            able.append(P2_cards[i])
                elif action == 1:
                    for i in range(len(P2_cards)):
                        if P2_cards[i][1] == env.top_card[1]:
                             able.append(P2_cards[i])
                elif action == 2:
                    for i in range(len(P2_cards)):
                        if P2_cards[i][1] == 'J':
                            able.append(P2_cards[i])
                    P2_reward += 1
                    env.turn += env.direction * 2
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
                    env.turn += 3
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
                next_state = state
                if not P2_cards:
                    done = True
                    P2_win += 1
                    agent.append_sample(state, action, 100, next_state, done)
            else:           # P3
                print('\nP3 turn')
                state = env.action_able(P3_cards)
                print('P3 state : ', state)
                if not state:
                    if env.attack:
                        P3_cards += env.giveCards(env.attack)
                        P1_reward += env.attack + 1
                        P3_reward += env.attack + 1
                        env.attack = 0
                    else:
                        P3_cards.append(env.giveCards(1)[0])
                        P1_reward += 1
                        P2_reward += 1
                    env.turn += env.direction
                    continue
                while True:
                    action = agent.get_action(state)
                    if state[action] == 1:
                        break
                print('P3 action : ', action)
                able = list()

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
                next_state = state
                if not P3_cards:
                    done = True
                    P3_win += 1
                    agent.append_sample(state, action, 100, next_state, done)

            if done:
                agent.update_target_model()
                break

            env.turn += env.direction

        print('P1 win : {0:0.2f}% | P2 win : {0:0.2f}% | P3 win : {0:0.2f}% | draw :  {0:0.2f}%'
              .format(P1_win/episode_num*100, P2_win/episode_num*100, P3_win/episode_num*100, draw/episode_num*100))

agent.model.save_weights(".save_model/model", save_format="tf")
