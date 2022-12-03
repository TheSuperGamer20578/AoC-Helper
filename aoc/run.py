import sys


def run(parse: callable, solve: callable):
    """Runs the day without the cli"""
    if len(sys.argv) > 2 and sys.argv[1] == "literal":
        input = parse(" ".join(sys.argv[2:]).strip())
    else:
        with open(" ".join(sys.argv[1:]) if len(sys.argv) > 1 else ".input") as f:
            input = parse(f.read().strip())
    print(solve(input))
