"""Unit tests for the release_monitor."""

import pytest
from unittest.mock import patch
import release_monitor.release_monitor

def setup_module(module):
    """Perform setup of any state specific to the execution of the given module."""
    global NPM_URL
    global PYPI_URL
    global ENABLE_SCHEDULING
    global PROBE_FILE_LOCATION
    global SLEEP_INTERVAL
    global DEBUG

    NPM_URL = 'https://registry.npmjs.org/'
    PYPI_URL = 'https://pypi.org/'
    ENABLE_SCHEDULING = 0
    PROBE_FILE_LOCATION = "/tmp/release_monitoring/liveness.txt"
    SLEEP_INTERVAL = 20
    DEBUG = True


def test_liveness_probe():
    """Dummy test."""
    pass

def renew_rss_feeds():
    """Dummy test."""
    pass

def entry_in_previous_npm_set():
    """Dummy test."""
    pass

def entry_in_previous_pypi_set():
    """Dummy test."""
    pass

if __name__ == '__main__':
    pass
