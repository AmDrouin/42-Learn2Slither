"""."""

import random
from environment import Action


DEFLT_ALPHA = 0.1    # taux d'apprentissage
DEFLT_GAMMA = 0.99     # facteur d'actualisation (importance du futur)
DEFLT_EPSILON = 0.1   # taux d'exploration (epsilon-greedy)

REWARD_GREEN_APPLE = 0
REWARD_RED_APPLE = 0
REWARD_DEATH = 0
REWARD_STEP = 0


class Agent:
    """Q-learning agent: chooses actions and learns from experience."""

    def __init__(self, alpha=DEFLT_ALPHA, gamma=DEFLT_GAMMA, epsilon=DEFLT_EPSILON, seed=None):
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
