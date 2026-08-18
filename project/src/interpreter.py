"""Get the state of the Environment and change it to a vision for the snake."""


from environment import Environment

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
