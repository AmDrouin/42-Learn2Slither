from enum import Enum, auto
from dataclasses import dataclass
import random


DEFAULT_WIDTH = 10
DEFAULT_HEIGHT = 10
INITIAL_SNAKE_SIZE = 3
NUM_GREEN_APPLES = 2
NUM_RED_APPLES = 1


class Action(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class Event(Enum):
    NOTHING = auto()
    ATE_GREEN = auto()
    ATE_RED = auto()
    HIT_WALL = auto()
    HIT_SELF = auto()


@dataclass(frozen=True)
class StepResult:
    event: Event
    done: bool
    length: int


class Environment:
    def __init__(self, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, seed=None):
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
        # TODO stub
        raise NotImplementedError

    def _is_within_bounds(self, pos: tuple[int, int]) -> bool:
        raise NotImplementedError

    def _spawn_snake(self) -> list[tuple[int, int]]:
        raise NotImplementedError

    def _spawn_apple(self, excluded: set[tuple[int, int]]) -> tuple[int, int]:
        raise NotImplementedError

    def _is_reverse(self, action: Action) -> bool:
        raise NotImplementedError

    def step(self, action: Action) -> StepResult:
        raise NotImplementedError
