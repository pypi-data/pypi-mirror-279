from runloop_api.net import api_post, api_get


def create_devbox(entrypoint: str = None,
                  environment_variables: dict[str, str] = None,
                  setup_commands: list[str] = None) -> dict:
    """
    Create a running devbox.

    Args:
        entrypoint: (Optional) When specified, the Devbox will run this script as its main executable.
            The devbox lifecycle will be bound to entrypoint, shutting down when the process is complete.

        environment_variables: (Optional) Environment variables used to configure your Devbox.

        setup_commands: (Optional) List of commands needed to set up your Devbox. Examples might include
            fetching a tool or building your dependencies. Runloop will look optimize these steps for you.
    Returns:
        Devbox instance in the form of:
        {
            "id": str,
            "status": str (provisioning, initializing, running, failure,  shutdown),
            "create_time_ms": long
        }
    """
    # Set up the headers with the Bearer token
    return api_post("/v1/devboxes/", {
        "entrypoint": entrypoint,
        "environment_variables": environment_variables,
        "setup_commands": setup_commands
    })


def get_devbox(id: str):
    """
    Get updated devbox.

    Args:
        id: Id of the devbox instance.
    Returns:
        Devbox instance in the form of:
        {
            "id": str,
            "status": str (provisioning, initializing, running, failure,  shutdown),
            "create_time_ms": long
        }
    """
    return api_get(f"/v1/devboxes/{id}")


def shutdown_devbox(id: str) -> dict:
    """
    Shutdown devbox.

    Args:
        id: Id of the devbox instance.
    Returns:
        Updated devbox instance in the form of:
        {
            "id": str,
            "status": str (provisioning, initializing, running, failure,  shutdown),
            "create_time_ms": long
        }
    """
    return api_post(f"/v1/devboxes/{id}/shutdown", {})


def list_devboxes() -> dict:
    """
    List previously created devboxes.

    Returns:
        A list of devbox instances in the form of:
        {
            "devboxes: [
                "id": str,
                "status": str (provisioning, initializing, running, failure,  shutdown),
                "create_time_ms": long
            ]
        }
    """
    return api_get("/v1/devboxes/")


def get_devbox_logs(id: str) -> dict:
    """
    Get logs from a particular devbox instance.

    Args:
        id: Id of the devbox instance.
    Returns:
        A devbox object of the following shape:
        {
            "logs: [
                "message": str,
                "level": str,
                "timestamp_ms": long
            ]
        }
    """
    return api_get(f"/v1/devboxes/{id}/logs")
