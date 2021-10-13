# 파이썬과 케라스로 배우는 강화학습

import numpy as np
import random
from collections import deque
import tensorflow as tf
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.initializers import RandomUniform

class DQN(tf.keras.Model):              # 모델 정의
    def __init__(self, action_size):
        super(DQN, self).__init__()
        self.fc1 = Dense(9, activation='relu')                                                  # 입력층?
        self.fc2 = Dense(9, activation='relu')                                                  # 은닉층1
        self.fc_out = Dense(action_size, kernel_initializer=RandomUniform(-1e-3, 1e-3))         # 출력층(가중치 초기화)

    def call(self, x):                  # 큐함수 반환?
        x = self.fc1(x)
        x = self.fc2(x)
        q = self.fc_out(x)
        return q

class Agent:
    def __init__(self, state_size, action_size):
        #self.render = True
        self.state_size = state_size
        self.action_size = action_size

        self.discount_rate = 0.99                       # 보상 할인율
        self.learning_rate = 0.005                      # 학습 속도
        self.epsilon = 1.0
        self.epsilon_decay = 0.60                       # 에피소드의 45% 진행했을 때 엡실론 0 되도록 함
        self.epsilon_min = 0.05
        self.batch_size = 60
        self.train_start = 1200
        self.memory = deque(maxlen=2000)

        self.model = DQN(action_size)
        self.model.load_weights("./.save_model/model_001").expect_partial()
        self.target_model = DQN(action_size)
        self.optimizer = Adam(lr=self.learning_rate)

        self.update_target_model()

        self.loss = 0

    def update_target_model(self):                       # 타겟 모델 업데이트
        self.target_model.set_weights(self.model.get_weights())

    def get_action(self, state):                         # 엡실론-탐욕 함수 기반으로 행동 선택
        state = np.reshape(state, [1, self.state_size])
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        else:
            q_value = self.model(state)
            return np.argmax(q_value[0])

    def append_sample(self, state, action, reward, next_state, done):                   # 리플레이 메모리 업데이트
        self.memory.append((state, action, reward, next_state, done))

    def train_model(self):                              # 모델 훈련
        if self.epsilon > self.epsilon_min:                                             # 엡실론 값 업데이트
            self.epsilon *= self.epsilon_decay

        mini_batch = random.sample(self.memory, self.batch_size)                        # 미니배치 가져온다
        # print(len(mini_batch))
        # print('mini_batch : ', mini_batch)
        states = np.array([sample[0] for sample in mini_batch])
        # print(states)
        actions = np.array([sample[1] for sample in mini_batch])
        # print(actions)
        rewards = np.array([sample[2] for sample in mini_batch])
        # print(rewards)
        next_states = np.array([sample[3] for sample in mini_batch])
        # print(next_states)
        dones = np.array([sample[4] for sample in mini_batch])

        model_params = self.model.trainable_variables
        with tf.GradientTape() as tape:
            predicts = self.model(states)                                               # 케라스 모델의 입력(numpy array 형태여야 한다)으로 상태 준다
            one_hot_action = tf.one_hot(actions, self.action_size)                      # 실제로 에이전트가 한 행동의 큐함수 값 가져온다
            predicts = tf.reduce_sum(one_hot_action * predicts, axis=1)                 # 오류함수의 예측 부분

            target_predicts = self.target_model(next_states)                            # 타겟 모델 예측
            target_predicts = tf.stop_gradient(target_predicts)

            max_q = np.amax(target_predicts, axis=1)                                    # 다음 상태의 Q함수 중 가장 큰 값 가져온다
            targets = rewards + (1 - dones) * self.discount_rate * max_q
            loss = tf.reduce_mean(tf.square(targets - predicts))                        # (MSE) 오류함수 구한다

        grads = tape.gradient(loss, model_params)                                       # 오류함수 기반으로 현재 모델 업데이트
        self.optimizer.apply_gradients(zip(grads, model_params))

        self.loss = loss

