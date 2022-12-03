import os
import shutil

import click

from . import util


def validate_day(_: click.Context, __: click.Option, day: int):
    if not 1 <= day <= 25:
        raise click.BadParameter("Invalid day")
    return day


def validate_year(_: click.Context, __: click.Option, year: int):
    if year is None:
        path = os.getcwd().split("/")
        try:
            year = int(path[-1])
        except ValueError:
            raise click.BadParameter("Could not auto-detect year")
        if not 2015 <= year:
            raise click.BadParameter("Detected year is invalid")
    elif not 2015 <= year:
        raise click.BadParameter("Invalid year")
    return year


@click.command()
@click.argument("day", type=int, callback=validate_day)
@click.option("--year", "-y", default=None, type=int, callback=validate_year, show_default="Name of the current directory", help="Year to prepare for")
def prep(day, year):
    """Makes a directory for the current day and copies a template"""
    padded = f"{day:02d}"
    if os.path.exists(padded):
        click.confirm(f"Day {day} already exists, overwrite?", abort=True, err=True)
        if os.path.isdir(padded):
            shutil.rmtree(padded)
        else:
            os.remove(padded)
    os.mkdir(padded)
    with open(os.path.join(os.path.dirname(__file__), "template.py")) as template:
        with open(f"{padded}/1.py", "x") as f:
            f.write(f'"""{util.URL.format(day=day, year=year)}"""\n')
            f.write(template.read())
    click.secho("Preparation done", fg="bright_green")
