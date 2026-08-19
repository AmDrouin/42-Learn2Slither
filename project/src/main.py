"""Main: wire Environment, Interpreter and Agent into a training loop."""

from cli import parse_args
from agent import Agent
from interpreter import Interpreter
from environment import Environment


def run_episode(env, interp, agent, learn: bool) -> tuple[int, int]:
    """."""
    env.reset()
    duration = 0
    max_length = len(env.snake)
    while not env.game_over:
        vision = interp.get_vision()
        state = interp.to_state_key(vision)
        action = agent.choose_action(state, greedy=not learn)
        result = env.step(action)
        if learn:
            if result.done:
                next_state = None
            else:
                next_state = interp.to_state_key(interp.get_vision())
            reward = agent.reward_for(result.event)
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
    for _ in range(args.sessions):
        len, dur = run_episode(env, interp, agent, learn)
        print(f"Game over, max length = {len}, max duration = {dur}")
    if args.save:
        agent.save(args.save)
        print(f"Save learning state in {args.save}")


if __name__ == "__main__":
    main()
