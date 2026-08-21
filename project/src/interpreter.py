"""Get the state of the Environment and change it to a vision for the snake."""


from environment import Environment, Action, MOV_DELTA, Event

CHAR_EMPTY = "0"
CHAR_WALL = "W"
CHAR_SNAKE_BODY = "S"
CHAR_GREEN_APPLE = "G"
CHAR_RED_APPLE = "R"

REWARD_GREEN_APPLE = 10
REWARD_RED_APPLE = -10
REWARD_DEATH = -100
REWARD_STEP = -1

REWARD_BY_EVENT = {
    Event.ATE_GREEN: REWARD_GREEN_APPLE,
    Event.ATE_RED: REWARD_RED_APPLE,
    Event.HIT_WALL: REWARD_DEATH,
    Event.HIT_SELF: REWARD_DEATH,
    Event.NOTHING: REWARD_STEP,
}


class Interpreter:
    """Get Environment state into snake vision."""

    def __init__(self, env: Environment):
        """Assign environment."""
        self.env = env

    def _char_for(self, pos: tuple[int, int]) -> str:
        if pos in self.env.snake:
            return CHAR_SNAKE_BODY
        if pos in self.env.green_apples:
            return CHAR_GREEN_APPLE
        if pos == self.env.red_apple:
            return CHAR_RED_APPLE
        return CHAR_EMPTY

    def _look(self, direction: Action) -> str:
        d_row, d_col = MOV_DELTA[direction]
        row, col = self.env.snake[0]
        vision = ""
        while True:
            row, col = row + d_row, col + d_col
            if not self.env._is_within_bounds((row, col)):
                vision += CHAR_WALL
                break
            vision += self._char_for((row, col))
        return vision

    def get_vision(self) -> dict[Action, str]:
        """Return string in all direction."""
        return {direction: self._look(direction) for direction in Action}

    def to_state_key(self, vision: dict[Action, str]) -> tuple[str, ...]:
        """Flatten a vision dict into an ordered, hashable Q-table key."""
        return tuple(vision[direction] for direction in Action)

    def reward_for(self, event: Event) -> float:
        """Map a step Event to its scalar reward."""
        return REWARD_BY_EVENT[event]
