import datetime
import os

import click

from . import util


def day(_: click.Context, __: click.Option, day: int):
    if day is None:
        day = util.day()
    if not 1 <= day <= 25:
        raise click.BadParameter("Invalid day")
    return day


def year(_: click.Context, __: click.Option, year: int):
    if year is None:
        year = util.year()
    if not 2015 <= year <= datetime.date.today().year:
        raise click.BadParameter("Invalid year")
    return year


def token_file(ctx: click.Context, _: click.Option, token_file: str):
    if ctx.params["token"] is not None and token_file is not None:
        raise click.BadParameter("Token file is mutually exclusive with token")
    if ctx.params["token"] is None is token_file:
        return util.token()
    if not os.path.isfile(token_file):
        raise click.BadParameter("Token file does not exist")
    with open(token_file) as f:
        return f.read()


def output_file(_: click.Context, __: click.Option, file: str):
    if os.path.exists(file):
        raise click.BadParameter("File already exists")
    return file


def part(_: click.Context, __: click.Option, part):
    if part not in (1, 2):
        raise click.BadParameter("Part must be 1 or 2")
    if not os.path.isfile(f"{part}.py"):
        raise click.BadParameter("File not found")
    return part
