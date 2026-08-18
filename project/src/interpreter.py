"""Get the state of the Environment and change it to a vision for the snake."""


from environment import Environment, Action, MOV_DELTA

CHAR_EMPTY = "0"
CHAR_WALL = "W"
CHAR_SNAKE_BODY = "S"
CHAR_GREEN_APPLE = "G"
CHAR_RED_APPLE = "R"


class Interpreter:
    """Change snake vision into Environment state."""

    def __init__(self, env : Environment):
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
