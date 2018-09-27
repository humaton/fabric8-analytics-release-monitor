#!/usr/bin/env python3
"""Cli for the release monitor and liveness probe."""
import click

from release_monitor.release_monitor import run_liveness, ReleaseMonitor


@click.command()
@click.option('--liveness', is_flag=True, help="Starts liveness probe")
def cli(liveness):
    """Script starts release monitor service or it's liveness probe."""
    if liveness:
        run_liveness()
    else:
        monitor = ReleaseMonitor()
        monitor.run()
