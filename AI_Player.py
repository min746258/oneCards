import tensorflow as tf
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.optimizers import Adam
import numpy as np
import random as rand
from Enviroment import Game

class DQN_Player:
    def __init__(self):
        self.name = 'DQN Player'
        self.env = Game()                       # 환경을 호출

        self.state_size = self.env.state_size
        self.action_size = self.env.action_size

        self.node_num = 12                      # 인공신경망 레이어에 들어 있는 노드 개수
        self.learning_rate = 0.0005             # 학습 속도(느릴수록 정확도는 증가하지만 시간 오래 걸린다)
        self.epochs_cnt = 5                     # 배치로 학습하는 데이터 학습 횟수
        self.model = self.build_model()         # 인공신경망 모델 생성하여 저장

        self.discount_rate = 0.99               # 보상 대한 할인율
        self.penalty = -100                     # 패배 시 보상 (-)

        self.episode_num = 1200                 # 학습할 에피소드 횟수

        self.replay_memory_limit = 4096         # 리플레이 메모리 사이즈
        self.replay_size = 32                   # 학습할 데이터 크기
        self.replay_memory = list()

        self.epsilon = 1                        # 엡실론 탐욕 정책 사용
        self.epsilon_decay = 0.45               # 에피소드의 45% 진행했을 때 엡실론 = 0
        self.epsilon_min = 0.02                 # 엡실론 최솟값

        self.reward_list = list()               # 에피소드에서 받은 보상의 합 저장

    def build_model(self):                      # 인공신경망 구성하는 함수
        input_states = Input(shape=(1, self.state_size), name='Input_states')               # 인공신경망의 입력층 설정(shape이 1차원 벡터)
        x = (input_states)
        x = Dense(self.node_num, activation='relu')(x)                                      # 인공신경망의 레이어 설정
        out_actions = Dense(self.action_size, activation='linear', name='output')           # 인공신경망의 출력층 설정

        model = tf.keras.models.Model(inputs=[input_states], outputs=[out_actions])         # 모델 구성
        model.compile(optimizer=Adam(lr=self.learning_rate), loss='mean_squared_error')     # 모델 컴파일 환경 설정(최적화 함수로 Adam을 사용)

        print(model.summary())
        return model

    def train(self):                            # 데이터 수집하고 모델 훈련하는 함수
        for episode in range(self.episode_num):
            state = self.env.resetGame()                          # 환경 정보를 받아옴

            Q, reward_tot = self.action_N_memory(episode, state)                            # 큐함수와 보상 정보를 받아옴

            # self.reward_list.append(reward_tot)                                           # 보상 리스트 업데이트
            self.train_miniBatch(Q)                                                         # 미니배치 학습

        self.save_model()                                                                   # 모델 저장

    def action_N_memory(self, episode, state):
        reward_tot = 0
        done = False
        epsilon = self.get_epsilon(episode)                                                 # 엡실론 값 정한다

        while not done:
            #state_t =
            Q = self.model.predict(state_t)                                                 # 큐함수 값 예측
            action = self.greed_search(epsilon, episode, Q)                                 # 큐함수를 토대로 행동 선택
            # state_next, reward, done, none = self.env.step()                              # 다음 상황 대한 정보 받아옴

            # if done:
                # reward = self.penalty

            self.replay_memory.append([state_t, action, reward, state_next, done])          # 리플레이 메모리 업데이트
            if len(self.replay_memory) > self.replay_memory_limit:
                del self.replay_memory[0]

            reward_tot += reward
            state = state_next
        return Q, reward_tot

    def train_miniBatch(self):                                                              # 리플레이 메모리에서 랜덤하게 데이터 선별해 학습시킴
        array_state = list()
        array_Q = list()
        this_replay_size = self.replay_size
        if len(self.replay_memory) < self.replay_size:
            this_replay_size = len(self.replay_memory)

        for sample in rand.sample(self.replay_memory, this_replay_size):
            state_t, action, reward, state_next, done = sample                              # 학습 데이터 무작위로 선별
            if done:
                Q[0,0,action] = reward                                                      # 종료된 경우 --> Q값 = 보상
            else:
                state_t = np.reshape(state_next, [1,1,self.state_size])
                Q_new = self.model.predict(state_t)
                Q[0,0,action] = reward + self.discount_rate * max(np.max(Q_new))            # 종료 아닌 경우 --> Q값 = 보상 + 다음 상태 Q값 * 할인율
            array_state.append(state_t.reshape(1, self.state_size))
            array_Q.append(Q.reshape(1, self.action_size))                                  # 상태, Q값 사용 가능한 상태로 변환
        array_state_t = np.array(array_state)
        array_Q_t = np.array(array_Q)
        hist = self.model.fit(array_state_t, array_Q_t, epochs=self.epochs_cnt, verbose=0)  # 수집된 데이터로 모델 학습

    def get_epsilon(self, episode):                                                         # 감소한 엡실론 값 구한다
        result = self.epsilon * (1- episode / (self.episode_num * self.epsilon_decay))
        if result < self.epsilon_min:
            result = self.epsilon_min
        return result

    def greed_search(self, epsilon, episode, Q):                                            # 엡실론 탐욕 정책 기반으로 행동 선택
        if epsilon > np.random.rand(1):
            action = self.env.action_space.sample()
        else:
            action = np.argmax(0)
        return action

    def moving_avg(self, data, size=10):                                                    # 학습 과정 모니터링 위해 최근 20회의 결과 평균 나타냄
        if len(data) > 10:
            c = np.array(data[len(data) - size:len(data)])
        else:
            c = np.array(data)
        return np.mean(c)

    def save_model(self):                                                                   # 학습 모델 저장
        self.model.save("./model/dqn")
        print('********* end of learning')


if __name__ == "__main__":
    agent = DQN_Player()
    agent.train()