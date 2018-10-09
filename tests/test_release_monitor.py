"""Unit tests for the release monitor."""


def setup_module(module):
    """
        Perform setup of any state specific
        to the execution of the given module.
    """
    global ENABLE_SCHEDULING
    global SLEEP_INTERVAL
    global PYPI_URL
    global NPM_URL

    assert module is not None


def teardown_module(module):
    """Tear down any specific state."""
    assert module is not None


def test_fetched_releases(self):
    """Test fetching of new releases."""
    pass


def test_sleep_period(self):
    """Test sleep period between RSS feed updates."""
    pass


def test_liveness_probe(self):
    """Test livenss probe."""
    pass
