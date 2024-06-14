# CLI Reference

This page lists the `--help` for `cookiecutter-python-cli-app-demo` and all its commands.

## cookiecutter-python-cli-app-demo

Running `cookiecutter-python-cli-app-demo --help` or `python -m cookiecutter_python_cli_app_demo --help` shows a list of all of the available options and commands:

<!-- [[[cog
import cog
from cookiecutter_python_cli_app_demo import cli
from click.testing import CliRunner
result = CliRunner().invoke(cli.cli, ["--help"], terminal_width=88)
help = result.output.replace("Usage: cli", "Usage: cookiecutter-python-cli-app-demo")
cog.outl(f"\n```sh\ncookiecutter-python-cli-app-demo --help\n{help.rstrip()}\n```\n")
for command in cli.cli.commands.keys():
    result = CliRunner().invoke(cli.cli, [command, "--help"], terminal_width=88)
    help = result.output.replace("Usage: cli ", "Usage: cookiecutter-python-cli-app-demo ")
    cog.outl(f"## cookiecutter-python-cli-app-demo {command}\n\n```sh\ncookiecutter-python-cli-app-demo {command} --help\n{help.rstrip()}\n```\n")
]]] -->
<!-- [[[end]]] -->
