"""Environment settings for integration tests."""
import docker


def before_all(context):
    """Disable scheduling of new analyses."""
    client = docker.from_env(version="auto")
    context.release_monitor = client.containers.run(
        "fabric8-analytics-release-monitor-tests",
        environment=["ENABLE_SCHEDULING=0"],
        detach=True
    )


def after_all(context):
    """Kill container."""
    try:
        context.release_monitor.kill()
    except docker.errors.APIError:
        print(context.release_monitor.logs())
