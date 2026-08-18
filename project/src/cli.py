"""."""
import argparse


def parse_args() -> argparse.Namespace:
    """."""
    parser = argparse.ArgumentParser(prog="snake")
    parser.add_argument("-sessions", type=int, default=1)
    parser.add_argument("-save", type=str, default=None)
    parser.add_argument("-load", type=str, default=None)
    parser.add_argument("-visual", choices=["on", "off"], default="on")
    parser.add_argument("-dontlearn", action="store_true")
    parser.add_argument("-step-by-step", action="store_true", dest="step_by_step")
    return parser.parse_args()
