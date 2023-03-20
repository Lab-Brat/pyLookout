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
@click.option(
    "--background", is_flag=True, default=False, help="Run in background?"
)
def cli(threshold, mode, containers, background):
    """
    Cli interface to easily pass parameters to PyLookout
    """
    lookout = PyLookout(threshold, mode, containers)
    if background:
        lookout.run_in_background()
    else:
        lookout.checker()
