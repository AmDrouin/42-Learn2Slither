"""Environment: board, snake, apples, collisions, step()."""


from enum import Enum, auto
from dataclasses import dataclass
import random


DEFAULT_WIDTH = 10
DEFAULT_HEIGHT = 10
INITIAL_SNAKE_SIZE = 3
NUM_GREEN_APPLES = 2
NUM_RED_APPLES = 1


class Action(Enum):
    """Direction the snake moves on a single step."""

    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class Event(Enum):
    """Outcome produced by a single Environment.step() call."""

    NOTHING = auto()
    ATE_GREEN = auto()
    ATE_RED = auto()
    HIT_WALL = auto()
    HIT_SELF = auto()


@dataclass(frozen=True)
class StepResult:
    """Immutable summary of what happened during one step()."""

    event: Event
    done: bool
    length: int


class Environment:
    """Grid snake and apples; own the game rules and step()."""

    def __init__(self, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, seed=None):
        """Build  a fresh Environment and spawn an initial episode."""
        self.width = width
        self.height = height
        self._rng = random.Random(seed)
        self.snake = []
        self.direction = Action.UP
        self.green_apples = []
        self.red_apple = None
        self.game_over = False
        self.reset()

    def reset(self) -> None:
        """Respawn the snake and apples, clearing game-over state."""
        # TODO stub
        raise NotImplementedError

    def _is_within_bounds(self, pos: tuple[int, int]) -> bool:
        row, col = pos
        return 0 <= row < self.height and 0 <= col < self.width

    def _spawn_snake(self) -> list[tuple[int, int]]:
        direction = self._rng.choice(list(Action))
        deltas = {
            Action.RIGHT: (0, -1),
            Action.LEFT: (0, 1),
            Action.UP: (1, 0),
            Action.DOWN: (-1, 0),
        }

        if direction == Action.RIGHT:
            col = self._rng.randint(INITIAL_SNAKE_SIZE - 1, self.width - 1)
            row = self._rng.randint(0, self.height - 1)
        elif direction == Action.LEFT:
            col = self._rng.randint(0, self.width - INITIAL_SNAKE_SIZE)
            row = self._rng.randint(0, self.height - 1)
        elif direction == Action.DOWN:
            row = self._rng.randint(INITIAL_SNAKE_SIZE - 1, self.height - 1)
            col = self._rng.randint(0, self.width - 1)
        else:
            row = self._rng.randint(0, self.height - INITIAL_SNAKE_SIZE)
            col = self._rng.randint(0, self.width - 1)

        d_row, d_col = deltas[direction]
        snake = [
            (row + d_row * i, col + d_col * i)
            for i in range(INITIAL_SNAKE_SIZE)
        ]
        self.direction = direction
        return snake

    def _spawn_apple(self, excluded: set[tuple[int, int]]) -> tuple[int, int]:
        raise NotImplementedError

    def _is_reverse(self, action: Action) -> bool:
        raise NotImplementedError

    def step(self, action: Action) -> StepResult:
        """."""
        raise NotImplementedError
