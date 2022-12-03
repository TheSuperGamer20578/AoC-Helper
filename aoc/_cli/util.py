import os
import datetime

import click

URL = "https://adventofcode.com/{year}/day/{day}"
match os.name:
    case "posix":
        PATH_SEP = "/"
    case "nt":
        PATH_SEP = "\\"
    case os_name:
        click.secho(f"Unsupported OS: {os_name}", fg="red", err=True)
        raise click.Abort()


def day() -> int:
    """Get the current day"""
    path = os.getcwd().split(PATH_SEP)
    try:
        day = int(path[-1])
    except ValueError:
        raise click.BadParameter("Could not auto-detect day")
    if not 1 <= day <= 25:
        raise click.BadParameter("Detected day is invalid")
    return day


def year() -> int:
    """Get the current year"""
    path = os.getcwd().split(PATH_SEP)
    try:
        year = int(path[-2])
    except ValueError:
        raise click.BadParameter("Could not auto-detect year")
    if not 2015 <= year <= datetime.date.today().year:
        raise click.BadParameter("Detected year is invalid")
    return year


def token() -> str:
    """Get the token"""
    if ".token" in os.listdir():
        with open(".token") as f:
            return f.read()
    if ".token" in os.listdir(".."):
        with open("../.token") as f:
            return f.read()
    if ".token" in os.listdir("../.."):
        with open("../../.token") as f:
            return f.read()
    raise click.BadParameter("Could not locate .token in ./, ../ or ../../")
