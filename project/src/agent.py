"""."""

import random
from environment import Action
import pickle


DEFLT_ALPHA = 0.1    # taux d'apprentissage
DEFLT_GAMMA = 0.99     # facteur d'actualisation (importance du futur)
EPSILON_START = 1.0
EPSILON_MIN = 0.01
EPSILON_DECAY = 0.995


class Agent:
    """Q-learning agent: chooses actions and learns from experience."""

    def __init__(self, alpha=DEFLT_ALPHA, gamma=DEFLT_GAMMA, epsilon=EPSILON_START, seed=None):
        """Build a Q-learning agent with an empty Q-table."""
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self._rng = random.Random(seed)
        self.q_table : dict[tuple, dict[Action, float]] = {}

    def _ensure_state(self, state: tuple) -> dict[Action, float]:
        """Create a zero-initialized entry for state if missing, then return it."""
        if state not in self.q_table:
            self.q_table[state] = {action : 0.0 for action in Action}
        return self.q_table[state]

    def choose_action(self, state: tuple, greedy: bool = False) -> Action:
        """Epsilon-greedy: explore randomly or exploit the best known action."""
        q_values = self._ensure_state(state)
        explore = (not greedy) and (self._rng.random() < self.epsilon)
        if explore :
            return self._rng.choice(list(Action))
        return max(q_values, key=q_values.get)

    def learn(self, state, action, reward, next_state, done) -> None:
        """Bellman-update the Q-value for (state, action)."""
        q_values = self._ensure_state(state)
        current = q_values[action]
        if done:
            target = reward
        else:
            q_values_next = self._ensure_state(next_state)
            target = reward + self.gamma * max(q_values_next.values())
        q_values[action] = current + self.alpha * (target - current)

    def save(self, path):
        """Persist the Q-table to path."""
        with open(path, "wb") as file:
            pickle.dump(self.q_table, file)

    def load(self, path):
        """Load the Q-table from path."""
        with open(path, "rb") as file:
            self.q_table = pickle.load(file)

    def decay_epsilon(self) -> None:
        """."""
        self.epsilon = max(EPSILON_MIN, self.epsilon * EPSILON_DECAY)
