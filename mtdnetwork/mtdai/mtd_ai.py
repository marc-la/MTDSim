import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, LSTM, Concatenate, ReLU, BatchNormalization, Dropout, Add
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import MeanSquaredError
import numpy as np
import random
from collections import deque
import pandas as pd
# Define the neural network architecture
def create_network(state_size, action_size, time_series_size):
    # Static feature extraction module
    static_input = Input(shape=(state_size,))
    x = Dense(128)(static_input)
    x = ReLU()(x)
    x = BatchNormalization()(x)
    x = Dense(64)(x)
    x = ReLU()(x)
    x = BatchNormalization()(x)
    x = Dropout(0.3)(x)

    # Time-series analysis module
    time_series_input = Input(shape=(time_series_size, 1))
    y = LSTM(64, return_sequences=True)(time_series_input)
    y = ReLU()(y)
    y = BatchNormalization()(y)
    y = LSTM(32)(y)
    y = ReLU()(y)
    y = BatchNormalization()(y)
    y = Dropout(0.3)(y)

    # Feature fusion module
    z = Concatenate()([x, y])
    z = Dense(64)(z)
    z = ReLU()(z)
    z = BatchNormalization()(z)
    z = Dropout(0.3)(z)

    # Q-Network output layer
    output = Dense(action_size)(z)

    model = Model(inputs=[static_input, time_series_input], outputs=output)
    model.compile(loss='mean_squared_error', optimizer=Adam(learning_rate=0.001))
    return model

# Define a function to update the target network
def update_target_model(target_network, main_network):
    target_network.set_weights(main_network.get_weights())

# Function to act based on model's output
def choose_action_traced(state, time_series, main_network, action_size, epsilon):
    """Epsilon-greedy selection, reporting *how* the action was chosen.

    Returns ``(action, source)`` with source in {"random", "greedy"}. The
    calibration study needs the greedy share separated from the exploration
    share: a no-op share measured over both is floored by ``epsilon / n_actions``
    no matter what the policy has learned, so a ladder read off the pooled share
    would report the exploration schedule rather than the policy.
    """
    state = np.asarray(state, dtype="float32").reshape((1, -1))
    time_series = np.asarray(time_series, dtype="float32").reshape((1, -1))

    if np.random.rand() <= epsilon:
        return random.randrange(action_size), "random"
    act_values = np.asarray(main_network([state, time_series], training=False))
    return int(np.argmax(act_values[0])), "greedy"


def choose_action(state, time_series, main_network, action_size, epsilon):
    return choose_action_traced(state, time_series, main_network, action_size, epsilon)[0]

# Learning function
def soft_update_target_model(target_network, main_network, tau=0.1):
    main_weights = np.array(main_network.get_weights())
    target_weights = np.array(target_network.get_weights())
    target_network.set_weights(tau * main_weights + (1 - tau) * target_weights)

# Double Q-learning
def replay(memory, main_network, target_network, batch_size, gamma, epsilon, epsilon_min, epsilon_decay, train_start):
    """One Double-DQN update over a minibatch drawn from the replay buffer.

    MTDAI-07 repair + vectorisation (2026-08-08). This used to loop over the
    minibatch in Python, calling ``predict`` three times and ``fit`` once **per
    sample**, all at batch size 1. Two consequences, one numerical and one
    practical:

    - A batch of one has a per-feature variance of exactly 0, so every
      BatchNormalization layer decayed ``moving_variance`` as ``0.99 ** n``
      toward zero and never recovered. Measured across Tay's checkpoints it is
      *exactly* 0.0 everywhere, which at inference makes the layer compute
      ``(x - mean) / sqrt(0 + 1e-3)`` — a x31.6 amplification at four stacked
      layers, and the direct cause of the observed 10^4-10^6 Q-value gaps. Every
      such checkpoint is numerically broken as an inference object regardless of
      what it learned (mtd_ai_forensics.md §3(a)).
    - Measured on this box the per-sample loop cost 26.5 s per call at batch 64,
      which is what made Tay's sweep unaffordable and the study shallow
      (forensics §4(c)). One batched update is two to three orders of magnitude
      cheaper.

    The epsilon decay that used to sit at the bottom of this function is also
    gone: it multiplied a local float and was therefore dead. The schedule is
    the caller's, and is now declared rather than incidental.
    """
    if len(memory) < train_start:
        return
    minibatch = random.sample(memory, min(batch_size, len(memory)))

    states = np.asarray([t[0] for t in minibatch], dtype="float32")
    time_series = np.asarray([t[1] for t in minibatch], dtype="float32")
    actions = np.asarray([t[2] for t in minibatch], dtype="int64")
    rewards = np.asarray([t[3] for t in minibatch], dtype="float32")
    next_states = np.asarray([t[4] for t in minibatch], dtype="float32")
    next_time_series = np.asarray([t[5] for t in minibatch], dtype="float32")
    dones = np.asarray([t[6] for t in minibatch], dtype=bool)

    # Inference passes go through __call__ rather than predict(): predict()
    # rebuilds a tf.function and a progress-bar callback per call, which
    # dominates the cost at these batch sizes.
    targets = np.asarray(main_network([states, time_series], training=False))
    next_q_main = np.asarray(main_network([next_states, next_time_series], training=False))
    next_q_target = np.asarray(target_network([next_states, next_time_series], training=False))

    rows = np.arange(len(minibatch))
    # Double DQN: the main network picks the next action, the target network
    # prices it.
    best_next = np.argmax(next_q_main, axis=1)
    bootstrap = np.where(dones, 0.0, next_q_target[rows, best_next])
    targets[rows, actions] = rewards + gamma * bootstrap

    main_network.train_on_batch([states, time_series], targets)





def normalize_array(arr, min_val=None, max_val=None):
    if min_val is None:
        min_val = np.min(arr)
    if max_val is None:
        max_val = np.max(arr)
    return (arr - min_val) / (max_val - min_val) if max_val > min_val else arr
# def normalize_array(arr):
#     mean_val = np.mean(arr)
#     std_val = np.std(arr)
    
#     # Avoid division by zero
#     if std_val == 0:
#         return np.zeros_like(arr)  # or return arr, depending on your preference
    
#     return (arr - mean_val) / std_val



def calculate_reward( current_state, current_time_series, next_state, next_time_series, static_features, time_features, memory):
 
    reward = 0

    # Check if memory has data for normalization

    if len(memory) > 0:
        memory_states = np.stack([item[0] for item in memory])
        memory_time_series = np.stack([item[5] for item in memory])
        
        # Create DataFrames
        memory_states_df = pd.DataFrame(memory_states)
        memory_time_series_df = pd.DataFrame(memory_time_series)

        # Convert to pandas Series before concatenating
        memory_states_normalized = pd.concat([memory_states_df, pd.Series(current_state).to_frame().T], ignore_index=True)
        memory_time_series_normalized = pd.concat([memory_time_series_df, pd.Series(current_time_series).to_frame().T], ignore_index=True)
        memory_next_states_normalized = pd.concat([memory_states_df, pd.Series(next_state).to_frame().T], ignore_index=True)
        memory_next_time_series_normalized = pd.concat([memory_time_series_df, pd.Series(next_time_series).to_frame().T], ignore_index=True)



        # Print the normalized DataFrames
        # print("Normalized Memory States:\n", memory_states_normalized)
        # print("\nNormalized Memory Time Series:\n", memory_time_series_normalized)
        # print("\nMemory Next States Normalized:\n", memory_next_states_normalized)
        # print("\nMemory Next Time Series Normalized:\n", memory_next_time_series_normalized)


        # Normalize current and next states
        norm_current_state = memory_states_normalized.apply(lambda x: normalize_array(x), axis=0).iloc[-1]
        norm_next_state = memory_next_states_normalized.apply(lambda x: normalize_array(x), axis=0).iloc[-1]

        # Normalize current and next time series
        norm_current_time_series = memory_time_series_normalized.apply(lambda x: normalize_array(x), axis=0).iloc[-1]
        norm_next_time_series = memory_next_time_series_normalized.apply(lambda x: normalize_array(x), axis=0).iloc[-1]

    
    else:
        # Use raw values if memory is empty
        norm_current_state = current_state
        norm_next_state = next_state
        norm_current_time_series = current_time_series
        norm_next_time_series = next_time_series
    # print(norm_current_state, norm_next_state,norm_current_time_series, norm_next_time_series )
    # print(norm_current_state,norm_current_time_series)
    # Dynamic weights based on context
    context_multiplier = 1  # Adjust this dynamically based on system context
    dynamic_weights = {
        "host_compromise_ratio": 0,
        "attack_path_exposure": -75 * context_multiplier,
        "overall_asr_avg": -75 * context_multiplier,
        "roa": -75 * context_multiplier,
        "risk": -75 * context_multiplier,
        
    }

    # Include time series features in the dynamic weights
    time_series_weights = {
        "mtd_freq": 0,
        "overall_mttc_avg": 75 * context_multiplier,
        "time_since_last_mtd": 0,
        "shortest_path_variability": 75 * context_multiplier,
        "ip_variability": 75 * context_multiplier,
        "attack_type": 0
    }

    # Calculate reward using normalized or raw values
    for index, feature in enumerate(static_features):
        delta = (norm_next_state[index] - norm_current_state[index])
        reward += delta * dynamic_weights.get(feature, 0)
     
    for index, time_series_feature in enumerate(time_features):
        delta = (norm_next_time_series[index] - norm_current_time_series[index])
        reward += delta * time_series_weights.get(time_series_feature, 0)
    # Print normalized values
    # print("\nNormalized Current State:")
    # print(norm_current_state)

    # print("\nNormalized Next State:")
    # print(norm_next_state)

    # print("\nNormalized Current Time Series:")
    # print(norm_current_time_series)

    # print("\nNormalized Next Time Series:")
    # print(norm_next_time_series)
    # print(reward)
    return reward



