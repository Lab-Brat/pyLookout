import sys
import click
from .lookout import PyLookout


@click.command()
@click.option(
    "--threshold",
    default=75,
    help="Percentage threshold for alerting. Above this threshold will trigger an alert.",
)
@click.option(
    "--mode",
    default="local",
    help="Send notifications: simplepush, sendgrid or locally?",
)
@click.option(
    "--logins",
    default=1,
    help="Normal amount of active logins. -1 if root login is not allowed",
)
@click.option(
    "--containers",
    is_flag=True,
    default=False,
    help="Monitor containers. Alert when there are containers in Exited state.",
)
@click.option(
    "--background",
    is_flag=True,
    default=False,
    help="Run in the background and check every 60 seconds.",
)
@click.option(
    "--gen-service",
    is_flag=True,
    default=False,
    help="Generate a systemd service",
)
def cli(threshold, mode, logins, containers, background, gen_service):
    """
    Cli interface to easily pass parameters to PyLookout
    """
    lookout = PyLookout(threshold, mode, logins, containers)
    if background:
        lookout.run_in_background()
    elif gen_service:
        flags = sys.argv
        if len(flags) > 1:
            flags = sys.argv[1:]
            flags = " ".join(
                flag for flag in flags if flag not in ["--gen-service"]
            )
        else:
            flags = ""
        lookout.create_config(flags)
    else:
        lookout.checker()
