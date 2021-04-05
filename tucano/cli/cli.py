import logging

import click

from ..workspace import Workspace

default_log_level = 'WARNING'
log_choices = click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], case_sensitive=False)


@click.group()
def cli():
    pass


def init_logs(log_level):
    """Initialize the logs at the desired logging level."""
    numeric_level = getattr(logging, log_level.upper(), None)

    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {log_level}')

    log_format = "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"

    logging.basicConfig(level=numeric_level, format=log_format)


@click.command()
@click.option('--force', '-f', default=False, is_flag=True, help='Force to recreate the workspace to default files')
@click.option('--log_level', '-l', default=default_log_level, type=log_choices,
              help='Level to produce the logs.')
def init(force, log_level):
    """Initialize the workspace.yaml file in this folder."""
    init_logs(log_level)

    print('Initializing the workspace')
    Workspace.initialize_workspace(force)
    print("Workspace initialized. You should now build the local image with `tucano build` Give it a try (:")


@click.command()
@click.option('--yaml_file', default=Workspace.workspace_file, type=str,
              help='yaml file to read the workspace configuration from.')
@click.option('--log_level', '-l', default=default_log_level, type=log_choices,
              help='Level to produce the logs.')
def build(yaml_file, log_level):
    """Does the necessary setup before running the workspace."""

    init_logs(log_level)
    print('Building the workspace')

    with open(yaml_file) as f:
        workspace = Workspace.from_yaml(f)

    workspace.build()


@click.command()
@click.option('--yaml_file', default=Workspace.workspace_file, type=str,
              help='yaml file to read the workspace configuration from.')
@click.option('--log_level', '-l', default=default_log_level, type=log_choices,
              help='Level to produce the logs.')
def shell(yaml_file, log_level):
    """Opens a shell in the container of the current workspace."""
    init_logs(log_level)
    print('Entering shell the workspace')

    with open(yaml_file) as f:
        workspace = Workspace.from_yaml(f)

    workspace.shell()


@click.command(context_settings=dict(
    ignore_unknown_options=True,
))
@click.option('--yaml_file', default=Workspace.workspace_file, type=str,
              help='yaml file to read the workspace configuration from.')
@click.option('--log_level', '-l', default=default_log_level, type=log_choices,
              help='Level to produce the logs.')
@click.argument('command', nargs=-1, type=click.UNPROCESSED)
def run(yaml_file, log_level, command):
    """Runs a single command inside the container of the current workspace."""
    init_logs(log_level)
    with open(yaml_file) as f:
        workspace = Workspace.from_yaml(f)

    workspace.run(' '.join(command))


cli.add_command(init)
cli.add_command(build)
cli.add_command(shell)
cli.add_command(run)

if __name__ == "__main__":
    cli()
