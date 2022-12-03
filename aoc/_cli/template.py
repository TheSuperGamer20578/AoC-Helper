from typing import Any

from aoc import *


def parse(input: str) -> Any:
    """Parse the input"""
    ...


def solve(input: Any) -> int | str | Answer:
    """Solve the puzzle"""
    ...


if __name__ == "__main__":
    from aoc.run import run
    run(parse, solve)
