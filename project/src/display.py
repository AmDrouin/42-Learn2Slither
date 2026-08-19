"""Display in terminal and in pygame window."""

from environment import Action


def print_vision(vision: dict[Action, str]) -> None:
    """Print the snake's vision as a cross in terminal."""
    left = "".join(reversed(vision[Action.LEFT]))
    right = vision[Action.RIGHT]
    line = left + "H" + right
    head_col = len(left)

    high = "".join(reversed(vision[Action.UP]))
    down = vision[Action.DOWN]

    for c in high:
        print(" " * head_col + c)
    print(line)
    for c in down:
        print(" " * head_col + c)
