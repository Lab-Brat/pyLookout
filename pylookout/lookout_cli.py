import click
from .lookout import PyLookout


@click.command()
@click.option(
    "--threshold", default=75, help="Percentage threshold for alerting"
)
@click.option(
    "--mode",
    default="local",
    help="Send notifications: simplepush, sendgrid or locally?",
)
@click.option(
    "--containers", is_flag=True, default=False, help="Monitor containers?"
)
def cli(threshold, mode, containers):
    """
    Cli interface to easily pass parameters to PyLookout
    """
    PyLookout(threshold, mode, containers).checker()
