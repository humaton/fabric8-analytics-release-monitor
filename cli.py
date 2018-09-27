#!/usr/bin/env python3

import click

from release_monitor.release_monitor import run_liveness, ReleaseMonitor


@click.command()
@click.option('--liveness', is_flag=True, help="Starts liveness probe")
def cli(liveness):
    """This scripts starts firehose fetcher service or it's liveness probe"""
    if liveness:
        run_liveness()
    else:
        monitor = ReleaseMonitor()
        monitor.run()