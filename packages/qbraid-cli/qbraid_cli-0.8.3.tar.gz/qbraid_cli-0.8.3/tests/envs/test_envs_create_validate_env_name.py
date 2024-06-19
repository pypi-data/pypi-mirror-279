# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Unit tests for the validate_env_name function in the utils module.

"""

from unittest.mock import patch

import pytest
import typer

from qbraid_cli.envs.data_handling import validate_env_name


def test_validate_env_name_success():
    """Test that validate_env_name returns the value for valid environment names."""
    valid_env_name = "valid_name"
    with patch("qbraid_cli.envs.data_handling.is_valid_env_name", return_value=True):
        assert (
            validate_env_name(valid_env_name) == valid_env_name
        ), "Should return the original value for valid names"


def test_validate_env_name_failure():
    """Test that validate_env_name raises BadParameter for invalid environment names."""
    invalid_env_name = "invalid_name"
    with patch("qbraid_cli.envs.data_handling.is_valid_env_name", return_value=False):
        with pytest.raises(typer.BadParameter):
            validate_env_name(invalid_env_name)


@pytest.mark.parametrize(
    "env_name, expected",
    [
        # Valid names
        ("valid_env", True),
        ("env123", True),
        ("_env", True),
        # Invalid names due to invalid characters
        ("env*name", False),
        ("<env>", False),
        ("env|name", False),
        # Reserved names
        ("CON", False),
        ("com1", False),
        # Names that are too long
        ("a" * 21, False),
        # Empty or whitespace names
        ("", False),
        ("   ", False),
        # Python reserved words
        ("False", False),
        ("import", False),
        # Names starting with a number
        ("1env", False),
        ("123", False),
    ],
)
def test_is_valid_env_name(env_name, expected):
    """Test function that verifies valid python venv names."""
    valid = True
    try:
        validate_env_name(env_name)
    except typer.BadParameter:
        valid = False

    assert valid == expected
