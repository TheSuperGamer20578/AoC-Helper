import click

from . import get, run, prep, cp


@click.group()
def aoc():
    """Advent of Code helper"""


aoc.add_command(get.get)
aoc.add_command(run.run)
aoc.add_command(prep.prep)
aoc.add_command(cp.cp)


if __name__ == "__main__":
    aoc()
