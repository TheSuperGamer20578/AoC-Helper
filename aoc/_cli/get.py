import click
import requests

from . import util, validators


@click.command()
@click.option("--day", "-d", default=None, type=int, callback=validators.day, show_default="Name of the current directory", help="Day to get input for")
@click.option("--year", "-y", default=None, type=int, callback=validators.year, show_default="Name of the directory containing the current directory", help="Year to get input for")
@click.option("--token-file", "-f", "token", type=click.Path(), callback=validators.token_file, show_default=".token in ./, ../ or ../../", help="File to read token from, mutually exclusive with --token")
@click.option("--token", "-t", default=None, type=str, is_eager=True, show_default="Contents of --token-file", help="Token to use for submitting, mutually exclusive with --token-file")
@click.option("--output-file", "--output", "-o", default=".input", type=click.Path(), callback=validators.output_file, show_default=True, help="File to write input to")
def get(day, year, token, output_file):
    """Saves the day's input"""
    resp = requests.get(f"{util.URL.format(day=day, year=year)}/input", cookies={"session": token.strip()})
    if not resp.ok:
        click.secho("Could not get input", fg="bright_red", bold=True, err=True)
        click.secho(resp.text, fg="red", err=True)
        raise click.Abort()
    with open(output_file, "x") as f:
        f.write(resp.text.strip())
    click.secho("Successfully got input", fg="bright_green")
