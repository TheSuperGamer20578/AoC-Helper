import os
import shutil

import click
import requests

from . import util


@click.command()
def cp():
    """Copies part 1 to part 2"""
    if os.path.exists("2.py"):
        click.confirm(f"Part 2 already exists, overwrite?", abort=True, err=True)
        if os.path.isdir("2.py"):
            shutil.rmtree("2.py")
        else:
            os.remove("2.py")
    with open("1.py") as template:
        with open("2.py", "x") as f:
            f.write(f'{next(template)[:-4]}#part2"""\n')
            f.write(template.read())
    click.secho("Copy done", fg="bright_green")
