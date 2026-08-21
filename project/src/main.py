"""Main: wire Environment, Interpreter and Agent into a training loop."""

from cli import parse_args
from agent import Agent
from interpreter import Interpreter
from environment import Environment
from display import print_action, print_vision, GraphicalDisplay, SPEED_FPS


def run_episode(
    env, interp, agent, learn: bool, visual: bool, disp, step_by_step: bool
) -> tuple[int, int]:
    """."""
    env.reset()
    duration = 0
    max_length = len(env.snake)
    while not env.game_over:
        vision = interp.get_vision()
        state = interp.to_state_key(vision)
        action = agent.choose_action(state, greedy=not learn)
        result = env.step(action)
        if visual:
            print_vision(vision)
            print_action(action)
        if disp:
            disp.render()
        if step_by_step:
            input()
        if learn:
            if result.done:
                next_state = None
            else:
                next_state = interp.to_state_key(interp.get_vision())
            reward = interp.reward_for(result.event)
            agent.learn(state, action, reward, next_state, result.done)
        duration += 1
        max_length = max(max_length, len(env.snake))
    return max_length, duration


def main() -> None:
    """."""
    args = parse_args()
    env = Environment()
    interp = Interpreter(env)
    agent = Agent()
    if args.load:
        agent.load(args.load)
        print(f"Load trained model from {args.load}")
    learn = not args.dontlearn
    visual = args.visual == "on"
    disp = GraphicalDisplay(env, fps=SPEED_FPS[args.speed]) if visual else None
    for _ in range(args.sessions):
        mlen, dur = run_episode(
            env, interp, agent, learn, visual, disp, args.step_by_step
        )
        if learn:
            agent.decay_epsilon()
        print(f"Game over, max length = {mlen}, max duration = {dur}")
    if disp:
        disp.close()
    if args.save:
        agent.save(args.save)
        print(f"Save learning state in {args.save}")


if __name__ == "__main__":
    main()
