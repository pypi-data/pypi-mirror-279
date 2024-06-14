"""Main CLI for cookiecutter-python-cli-app-demo."""

import click

from . import __version__

context_settings = {"help_option_names": ["-h", "--help"]}


@click.group(context_settings=context_settings)
@click.version_option(__version__, "-v", "--version")
def cli() -> None:
    """Demo of https://github.com/sgraaf/cookiecutter-python-cli-app."""


@cli.command()
@click.argument("input_", metavar="INPUT")
@click.option(
    "-r",
    "--reverse",
    is_flag=True,
    help="Reverse the input.",
)
def repeat(input_: str, *, reverse: bool = False) -> None:
    """Repeat the input."""
    click.echo(input_ if not reverse else input_[::-1])
