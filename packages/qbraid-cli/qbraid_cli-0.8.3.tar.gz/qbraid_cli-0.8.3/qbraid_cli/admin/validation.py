# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Module for validating command arguments for qBraid admin commands.

"""

import os
from typing import List

import typer

from qbraid_cli.admin.headers import HEADER_TYPES
from qbraid_cli.handlers import _format_list_items, validate_item


def validate_header_type(value: str) -> str:
    """Validate header type."""
    header_types = list(HEADER_TYPES.keys())
    return validate_item(value, header_types, "Header type")


def validate_paths_exist(paths: List[str]) -> List[str]:
    """Verifies that each path in the provided list exists."""
    non_existent_paths = [path for path in paths if not os.path.exists(path)]
    if non_existent_paths:
        if len(non_existent_paths) == 1:
            raise typer.BadParameter(f"Path '{non_existent_paths[0]}' does not exist")
        raise typer.BadParameter(
            f"The following paths do not exist: {_format_list_items(non_existent_paths)}"
        )
    return paths
