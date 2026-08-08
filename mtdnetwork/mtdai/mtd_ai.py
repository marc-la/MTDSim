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
    # np.array (not asarray): the tensor's buffer is read-only, and the target
    # for the chosen action is written in place below.
    targets = np.array(main_network([states, time_series], training=False))
    next_q_main = np.asarray(main_network([next_states, next_time_series], training=False))
    next_q_target = np.asarray(target_network([next_states, next_time_series], training=False))

    rows = np.arange(len(minibatch))
    # Double DQN: the main network picks the next action, the target network
    # prices it.
    best_next = np.argmax(next_q_main, axis=1)
    bootstrap = np.where(dones, 0.0, next_q_target[rows, best_next])
    targets[rows, actions] = rewards + gamma * bootstrap

    main_network.train_on_batch([states, time_series], targets)





# --- the state vocabularies, and the reward -------------------------------
#
# The order of these two lists *is* the layout of the state and time-series
# vectors. Both operation classes build their vectors from them and the reward
# reads them back by the same index, so the two can never drift apart; the
# inherited code built the vectors from a dict literal in one file and indexed
# them by the caller's selection list in another, which happened to agree only
# because the selection was always the whole vocabulary.

STATE_FEATURE_ORDER = [
    "host_compromise_ratio",
    "attack_path_exposure",
    "overall_asr_avg",
    "roa",
    "risk",
]

TIME_FEATURE_ORDER = [
    "mtd_freq",
    "overall_mttc_avg",
    "time_since_last_mtd",
    "shortest_path_variability",
    "ip_variability",
    "attack_type",
    "downtime_ratio",
]

# The four mechanisms the action space ranges over, in Tay's order, and the
# canonical feature selection that goes with them.
#
# These live here for the same reason the two vocabularies above do: an action
# index is meaningless without the list it indexes, so a driver that builds its
# own list can silently re-point action 1 at a different mechanism than the one
# the agent was trained to deploy. Action 0 is the no-op, so the action space is
# ``len(MTD_ACTION_SPACE) + 1``. Imported by every driver rather than restated —
# ``tools/mtd_ai_run.py`` and the movement runner both read it from here.
#
# The import is deferred into the accessor so that reading the action space does
# not drag TensorFlow in behind it: the movement runner wants the list on a path
# that has no other reason to load a deep-learning stack.
def mtd_action_space():
    """The deploying actions, indexed 1..4 as the agent's output layer expects."""
    from mtdnetwork.mtd.completetopologyshuffle import CompleteTopologyShuffle
    from mtdnetwork.mtd.ipshuffle import IPShuffle
    from mtdnetwork.mtd.osdiversity import OSDiversity
    from mtdnetwork.mtd.servicediversity import ServiceDiversity

    return [CompleteTopologyShuffle, IPShuffle, OSDiversity, ServiceDiversity]


#: The live 5/6 state head (MTDAI-02). Both vectors are emitted at full width
#: with unselected features zeroed, so the network signature is fixed by the
#: vocabularies above rather than by this selection.
CANONICAL_FEATURES = {
    "static": list(STATE_FEATURE_ORDER),
    "time": list(TIME_FEATURE_ORDER),
}

# Security-posture weights, inherited from Tay's implementation unchanged. The
# paper contains no reward function at all -- §4.2 gives the Bellman target,
# Figure 2 has a box captioned "Calculate Reward for Action" with nothing behind
# it -- so these are the code's, undocumented, and they are kept rather than
# re-derived so that the only deliberate change to the reward is the cost term
# below.
SECURITY_WEIGHTS = {
    # static
    "host_compromise_ratio": 0,
    "attack_path_exposure": -75,
    "overall_asr_avg": -75,
    "roa": -75,
    "risk": -75,
    # time series
    "mtd_freq": 0,
    "overall_mttc_avg": 75,
    "time_since_last_mtd": 0,
    "shortest_path_variability": 75,
    "ip_variability": 75,
    "attack_type": 0,
    "downtime_ratio": 0,   # priced by downtime_lambda, not here
}

# Full-scale range per feature, used to put the deltas on a common footing
# before the weights are applied.
#
# MTDAI-12 (2026-08-08). The inherited normalisation was min-max against the
# replay buffer *as it grew*, which makes the reward scale a function of how far
# training has progressed: a transition stored at buffer size 50 and one stored
# at 2000 are priced by different rulers, and both sit in the same buffer being
# sampled against the same Q-function. It also read `item[5]` (the *next* time
# series) where `item[1]` (the current one) was meant. Fixing the index would
# not have fixed the scale, so the buffer-derived normaliser is replaced
# outright by fixed divisors, and the index defect dissolves with it.
#
# Each divisor is the feature's natural full-scale range under the substrate's
# own constants, not a fitted quantity:
#   risk = complexity x impact, with complexity <= 1 and impact < 10  -> 10
#   roa  = risk / exploit_time, with exploit_time >= 10 s             -> 1
#   overall_mttc_avg is a mean over SCAN_PORT / EXPLOIT_VULN /
#     BRUTE_FORCE durations, the largest of which is 25 s             -> 25
#   the remaining priced features are already ratios in [0, 1]        -> 1
# Features carrying weight 0 take 1 and are inert either way.
REWARD_FEATURE_SCALE = {
    "host_compromise_ratio": 1.0,
    "attack_path_exposure": 1.0,
    "overall_asr_avg": 1.0,
    "roa": 1.0,
    "risk": 10.0,
    "mtd_freq": 1.0,
    "overall_mttc_avg": 25.0,
    "time_since_last_mtd": 1.0,
    "shortest_path_variability": 1.0,
    "ip_variability": 1.0,
    "attack_type": 1.0,
    "downtime_ratio": 1.0,
}


def calculate_reward(current_state, current_time_series, next_state, next_time_series,
                     static_features, time_features, memory=None, downtime_lambda=0.0):
    """Reward for one transition: security posture gained, downtime charged.

        reward = sum of weighted security-posture deltas  -  lambda * delta downtime

    **The cost term is the point of this function's rework.** Every non-zero
    weight in the inherited reward is improved by deploying a mutation -- a
    mutation raises IP and path variability and MTTC and lowers exposure, ASR,
    RoA and risk -- and the two features that could have priced moving too
    often, `mtd_freq` and `time_since_last_mtd`, are weighted exactly 0. Under
    that reward the optimal policy is to deploy on every decision and the no-op
    has no route to positive value, which is why the paper's claim to have
    "minimised unnecessary MTD deployments" has nothing in the implementation
    that could produce it.

    `downtime_lambda` is the calibration knob. It is declared and swept, never
    fitted, and **at lambda = 0 this function is exactly the pre-rework reward
    up to the normalisation change**, so the ablation is exact.

    The charge is on the *change* in downtime, not its level, which keeps it
    dimensionally the same kind of quantity as every other term: recovering
    availability is worth precisely what losing it cost, rather than the agent
    paying a standing tax for having ever moved.

    `static_features` and `time_features` are the *selected* feature sets. An
    unselected feature is zeroed in both state vectors, so its delta is already
    0; they are consulted only so that an ablation over the state head is also
    an ablation over the reward. `memory` is retained for call compatibility and
    is no longer read -- see REWARD_FEATURE_SCALE.
    """
    reward = 0.0

    for index, feature in enumerate(STATE_FEATURE_ORDER):
        if feature not in static_features:
            continue
        delta = (next_state[index] - current_state[index]) / REWARD_FEATURE_SCALE[feature]
        reward += delta * SECURITY_WEIGHTS[feature]

    for index, feature in enumerate(TIME_FEATURE_ORDER):
        if feature not in time_features:
            continue
        delta = (next_time_series[index] - current_time_series[index]) / REWARD_FEATURE_SCALE[feature]
        reward += delta * SECURITY_WEIGHTS[feature]

    if downtime_lambda and "downtime_ratio" in time_features:
        index = TIME_FEATURE_ORDER.index("downtime_ratio")
        delta = ((next_time_series[index] - current_time_series[index])
                 / REWARD_FEATURE_SCALE["downtime_ratio"])
        reward -= downtime_lambda * delta

    return float(reward)
