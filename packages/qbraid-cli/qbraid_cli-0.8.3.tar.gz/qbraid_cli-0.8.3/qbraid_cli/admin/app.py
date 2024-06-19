# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Module defining commands in the 'qbraid admin' namespace.
"""

from typing import List

import typer

from qbraid_cli.admin.buildlogs import buildlogs_app
from qbraid_cli.admin.headers import check_and_fix_headers
from qbraid_cli.admin.validation import validate_header_type, validate_paths_exist

admin_app = typer.Typer(
    help="CI/CD commands for qBraid maintainers.", pretty_exceptions_show_locals=False
)
admin_app.add_typer(buildlogs_app, name="buildlogs")


@admin_app.command(name="headers")
def admin_headers(
    src_paths: List[str] = typer.Argument(
        ..., help="Source file or directory paths to verify.", callback=validate_paths_exist
    ),
    header_type: str = typer.Option(
        "default",
        "--type",
        "-t",
        help="Type of header to use ('default' or 'gpl').",
        callback=validate_header_type,
    ),
    skip_files: List[str] = typer.Option(
        [], "--skip", "-s", help="Files to skip during verification.", callback=validate_paths_exist
    ),
    fix: bool = typer.Option(
        False, "--fix", "-f", help="Whether to fix the headers instead of just verifying."
    ),
):
    """
    Verifies and optionally fixes qBraid headers in specified files and directories.

    """
    check_and_fix_headers(src_paths, header_type=header_type, skip_files=skip_files, fix=fix)


if __name__ == "__main__":
    admin_app()
