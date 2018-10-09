import docker


def before_all(context):
    client = docker.from_env(version="auto")
    context.release_monitor = client.containers.run(
        "fabric8-analytics-release-monitor-tests",
        environment=["ENABLE_SCHEDULING=0"],
        detach=True
    )


def after_all(context):
    try:
        context.release_monitor.kill()
    except docker.errors.APIError:
        print(context.release_monitor.logs())
        raise
