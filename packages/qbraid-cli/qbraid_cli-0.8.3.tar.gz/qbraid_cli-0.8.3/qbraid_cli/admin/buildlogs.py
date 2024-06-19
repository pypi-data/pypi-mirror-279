# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Module defining commands in the 'qbraid admin buildlogs' namespace.

This module uses the Typer library to create CLI commands for managing Docker builds and logs
in an administrative context.
"""

import json

import typer
from qbraid_core.exceptions import RequestsApiError
from qbraid_core.services.admin.client import AdminClient
from rich.console import Console

from qbraid_cli.handlers import handle_error

buildlogs_app = typer.Typer(
    help="Manage qBraid containerized services logs.", pretty_exceptions_show_locals=False
)
console = Console()


@buildlogs_app.command(name="get")
def get_docker_build_logs(
    build_id: str = typer.Option(None, "--build_id", "-b", help="Name of the build ID")
) -> None:
    """
    Fetches and displays Docker build logs for a specified build ID.

    Args:
        build_id (str, optional): The unique identifier for the Docker build.

    This function queries the administrative backend to retrieve and display build logs.
    If a build ID is provided, it will retrieve and display logs specific to that build ID.
    If build ID not provided, fetches all logs.
    """
    client = AdminClient()

    build_log = client.get_docker_build_logs(build_id)
    if build_id and "buildLogs" in build_log and build_log["buildLogs"]:
        log_entry = build_log["buildLogs"][0]
        console.print(log_entry)
    else:
        console.print(build_log)


@buildlogs_app.command(name="post")
def post_docker_build_log(
    data: str = typer.Option(..., "--data", "-d", help="Data to post to Docker logs")
) -> None:
    """
    Posts a new Docker build log entry.

    Args:
        data (str): JSON string containing the data to be logged.

    This command converts a JSON string into a dictionary and sends it to the backend service
    to create a new Docker build log.
    """
    client = AdminClient()

    try:
        data_dict = json.loads(data)
        console.print(client.post_docker_build_logs(data_dict))
    except RequestsApiError:
        handle_error(message="Couldn't post a build_log.")


@buildlogs_app.command(name="put")
def put_docker_build_log(
    build_id: str = typer.Option(..., "--build_id", "-b", help="Name of the build ID"),
    data: str = typer.Option(..., "--data", "-d", help="Data to post to Docker logs"),
) -> None:
    """
    Updates an existing Docker build log entry by a given build ID.

    Args:
        build_id (str): The unique identifier of the Docker build to update.
        data (str): JSON string containing the updated data for the log.

    This command updates a Docker build log entry, identified by the provided build ID,
    with the new data provided in JSON format.
    """
    client = AdminClient()

    try:
        data_dict = json.loads(data)
        console.print(client.put_docker_build_logs(build_id, data_dict))
    except RequestsApiError:
        handle_error(message="Couldn't post a build_log.")


@buildlogs_app.command(name="delete")
def delete_docker_build_log(
    build_id: str = typer.Option(..., "--build_id", "-b", help="ID of the build log to delete")
) -> None:
    """
    Deletes a Docker build log entry by a specified build ID.

    Args:
        build_id (str): The unique identifier of the Docker build log to delete.

    This command sends a request to delete a Docker build log identified by the provided build ID.
    """
    client = AdminClient()

    console.print(client.delete_docker_build_logs(build_id))


if __name__ == "__main__":
    buildlogs_app()
