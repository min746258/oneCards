from Enviroment import Game
from Human_Player import Human_Play
from DDQN_Player import *
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
        players_cards = [P2_cards, P3_cards, P1_cards]

        done = False
        winner = False

        for t in range(300):
            turn, direction = env.find_turn()
            state = env.top_card

            action = agent.get_action(state)
            next_state, reward, done, info = env.step(action)
            next_state = np.reshape(next_state, [(1, state_size)])

            agent.append_sample(state, action, reward, next_state, done)
            if len(agent.memory) >= agent.train_start:
                agent.train_model()

            state = next_state

            result = env.play(action)
            if result:
                if env.cards:
                    add = env.giveCards(result)
                    P1_cards.append(add)
                else:
                    draw += 1
                    break
            if not P1_cards:
                P1_win += 1
                winner = 1
                done = True

            if done:
                agent.update_target_model()
                break

    print('P1 win : {0:0.2f}% | P2 win : {0:0.2f}% | P3 win : {0:0.2f}% | draw :  {0:0.2f}%'
          .format(P1_win/episode_num*100, P2_win/episode_num*100, P3_win/episode_num*100, draw/episode_num*100))
    agent.model.save_weights(".save_model/model", save_format="tf")
