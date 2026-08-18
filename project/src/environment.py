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


OPPOSITE = {
    Action.UP: Action.DOWN,
    Action.DOWN: Action.UP,
    Action.LEFT: Action.RIGHT,
    Action.RIGHT: Action.LEFT,
}

DELTA = {
    Action.RIGHT: (0, -1),
    Action.LEFT: (0, 1),
    Action.UP: (1, 0),
    Action.DOWN: (-1, 0),
}


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

    def _is_within_bounds(self, pos: tuple[int, int]) -> bool:
        row, col = pos
        return 0 <= row < self.height and 0 <= col < self.width

    def _spawn_snake(self) -> list[tuple[int, int]]:
        direction = self._rng.choice(list(Action))
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

        d_row, d_col = DELTA[direction]
        snake = [
            (row + d_row * i, col + d_col * i)
            for i in range(INITIAL_SNAKE_SIZE)
        ]
        self.direction = direction
        return snake

    def _spawn_apple(self, excluded: set[tuple[int, int]]) -> tuple[int, int]:
        possibleSpawn = [
            (row, col)
            for row in range(self.height)
            for col in range(self.width)
            if (row, col) not in excluded
        ]
        return self._rng.choice(possibleSpawn)

    def _is_reverse(self, action: Action) -> bool:
        return action == OPPOSITE[self.direction]

    def step(self, action: Action) -> StepResult:
        """Advance the game by one action and return what happened."""
        if not self._is_reverse(action):
            self.direction = action

        d_row, d_col = DELTA[self.direction]
        head_row, head_col = self.snake[0]
        new_head = (head_row + d_row, head_col + d_col)

        if not self._is_within_bounds(new_head):
            self.game_over = True
            return StepResult(Event.HIT_WALL, True, len(self.snake))

        body_without_end = set(self.snake[:-1])
        if new_head in body_without_end:
            self.game_over = True
            return StepResult(Event.HIT_SELF, True, len(self.snake))

        if new_head in self.green_apples:
            self.snake.insert(0, new_head)
            self.green_apples.remove(new_head)
            occupied = (
                set(self.snake) | set(self.green_apples) | set([self.red_apple])
            )
            self.green_apples.append(self._spawn_apple(occupied))
            return StepResult(Event.ATE_GREEN, True, len(self.snake))

        if new_head == self.red_apple:
            self.snake.insert(0, new_head)
            self.snake.pop()
            self.snake.pop()
            if not self.snake:
                self.game_over = True
                return StepResult(Event.ATE_RED, True, 0)
            occupied = set(self.snake) | set(self.green_apples)
            self.red_apple = self._spawn_apple(occupied)
            return StepResult(Event.ATE_RED, False, len(self.snake))

        self.snake.insert(0, new_head)
        self.snake.pop()
        return StepResult(Event.NOTHING, False, len(self.snake))

    def reset(self) -> None:
        """Respawn the snake and apples, clearing game-over state."""
        self.snake = self._spawn_snake()
        occupied = set(self.snake)
        self.green_apples = []
        for _ in range(NUM_GREEN_APPLES):
            apple = self._spawn_apple(occupied)
            self.green_apples.append(apple)
            occupied.add(apple)
        self.red_apple = self._spawn_apple(occupied)
        self.game_over = False
