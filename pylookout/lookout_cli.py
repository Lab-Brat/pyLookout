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
def cli(threshold, mode):
    """
    Cli interface to easily pass parameters to PyLookout
    """
    PyLookout(threshold, mode).checker()


if __name__ == "__main__":
    cli()
