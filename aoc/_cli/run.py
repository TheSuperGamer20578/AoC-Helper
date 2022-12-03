import os
import re
import importlib.util

import click
import requests

from . import validators, util
from ..answers import Answer


@click.command()
@click.argument("part", type=int, callback=validators.part)
@click.option("--input-file", "-i", default=".input", type=click.File(), show_default=True, help="File to read input from")
@click.option("--submit/--no-submit", "-s/-n", default=None, type=bool, show_default="Prompt", help="Submit result after computing")
@click.option("--day", "-d", default=None, type=int, callback=validators.day, show_default="Name of the current directory", help="Day to submit")
@click.option("--year", "-y", default=None, type=int, callback=validators.year, show_default="Name of the directory containing the current directory", help="Year to submit")
@click.option("--token-file", "-f", "token", type=click.Path(), callback=validators.token_file, show_default=".token in ./, ../ or ../../", help="File to read token from, mutually exclusive with --token")
@click.option("--token", "-t", default=None, type=str, is_eager=True, show_default="Contents of --token-file", help="Token to use for submitting, mutually exclusive with --token-file")
def run(part, input_file, submit, day, year, token):
    """Runs a part"""
    input_ = input_file.read().strip()
    spec = importlib.util.spec_from_file_location(str(part), f"{os.getcwd()}/{part}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "parse") or not hasattr(module, "solve"):
        click.secho("Solution files are invalid", fg="bright_red", err=True)
        raise click.Abort()
    parsed = module.parse(input_)
    solution = module.solve(parsed)
    if not isinstance(solution, Answer):
        solution = Answer(solution)
    click.secho(solution, fg="bright_green")
    if submit is None and solution.submit:
        submit = click.confirm("Submit?")
    if not submit:
        return
    if not solution.submit:
        click.secho("Answer is not to be submitted", fg="bright_red", err=True)
        raise click.Abort
    resp = requests.post(f"{util.URL.format(day=day, year=year)}/answer", data={"level": part, "answer": solution}, cookies={"session": token.strip()})
    if not resp.ok:
        click.secho("Could not submit answer", fg="bright_red", bold=True, err=True)
        click.secho(resp.text, fg="red", err=True)
        raise click.Abort()
    match = re.search(r"<main>(.*)</main>", resp.text.replace("\n", " "), flags=re.S)
    message = (re.sub(r"[<[][^<>]*[>\]]", "", match.group(1), flags=re.S).strip()
               .replace("  ", " ").replace(". ", ".").replace(".", ". ")
               .replace(" You can [Shareon  Twitter  Mastodon] this victory or .", "")
               .replace("one gold star", click.style("one gold star", fg="bright_yellow", bold=True) + click.style("", fg="bright_green", reset=False)))
    if message.startswith("That's not the right answer") or message.startswith("You gave an answer too recently") or message.startswith("You don't seem to be solving the right level"):
        click.secho(message, fg="bright_red")
    elif message.startswith("That's the right answer"):
        click.secho(message, fg="bright_green")
    else:
        click.echo(message)
        click.secho("Unknown message", fg="red", err=True)
