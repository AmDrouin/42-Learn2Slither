"""Display in terminal and in pygame window."""

import pygame
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


def print_action(action: Action) -> None:
    """Print the action taken by the agent."""
    print(action.name)


CELL_SIZE = 30
DOT_RADIUS = 3
HEAD_RADIUS = CELL_SIZE // 3
TRIANGLE_SIZE = CELL_SIZE // 3
APPLE_RADIUS = CELL_SIZE // 4

COLOR_BG = (20, 20, 20)
COLOR_GRID_DOT = (90, 90, 90)
COLOR_GREEN_APPLE = (0, 200, 0)
COLOR_RED_APPLE = (200, 0, 0)
COLOR_HEAD = (220, 30, 30)
COLOR_BODY = (0, 180, 0)


class GraphicalDisplay:
    """Pygame window rendering the game."""

    def __init__(self, env, fps: int = 10):
        """."""
        self.env = env
        self.fps = fps
        pygame.init()
        width_px = env.width * CELL_SIZE
        height_px = env.height * CELL_SIZE
        self.screen = pygame.display.set_mode((width_px, height_px))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()

    def _cell_center(self, pos: tuple[int, int]) -> tuple[int, int]:
        row, col = pos
        return (col * CELL_SIZE + CELL_SIZE // 2,  row * CELL_SIZE + CELL_SIZE // 2)

    def _draw_dot(self, pos, color, radius) -> None:
        pygame.draw.circle(self.screen, color, self._cell_center(pos), radius)

    def _draw_head(self, pos: tuple[int, int]) -> None:
        self._draw_dot(pos, COLOR_HEAD, HEAD_RADIUS)

    def _draw_body_triangle(self, pos: tuple[int, int]) -> None:
        cX, cY = self._cell_center(pos)
        summit = [
            (cX, cY - TRIANGLE_SIZE),
            (cX - TRIANGLE_SIZE, cY + TRIANGLE_SIZE),
            (cX + TRIANGLE_SIZE, cY + TRIANGLE_SIZE),
        ]
        pygame.draw.polygon(self.screen, COLOR_BODY, summit)

    def render(self) -> None:
        """."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
                raise SystemExit
        self.screen.fill(COLOR_BG)
        for row in range(self.env.height):
            for col in range(self.env.width):
                self._draw_dot((row, col), COLOR_GRID_DOT, DOT_RADIUS)
        for apple in self.env.green_apples:
            self._draw_dot(apple, COLOR_GREEN_APPLE, APPLE_RADIUS)
        self._draw_dot(self.env.red_apple, COLOR_RED_APPLE, APPLE_RADIUS)
        self._draw_head(self.env.snake[0])
        for _ in self.env.snake[1:]:
            self._draw_body_triangle(_)
        pygame.display.flip()
        self.clock.tick(self.fps)

    def close(self) -> None:
        """Close the pygame window."""
        pygame.quit()
