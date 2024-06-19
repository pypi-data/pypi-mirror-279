# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Unit tests for the `qbraid_cli.envs.app` module, specifically for the `envs list` command.

"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from qbraid_cli.envs import envs_app


@pytest.mark.parametrize(
    "user_confirmation, expected_output",
    [("y", "Successfully created qBraid environment"), ("n", "qBraidSystemExit: Exiting.")],
)
def test_envs_create_with_user_confirmation(
    user_confirmation, expected_output  # pylint: disable=unused-argument
):
    """Test creating an environment with user confirmation."""

    runner = CliRunner()
    mock_env_data = {
        "slug": "test-slug",
        "displayName": "test_env",
        "prompt": "",
        "description": "",
        "tags": "",
        "kernelName": "",
    }
    with (
        patch(
            "qbraid_core.QbraidSession.post",
            return_value=MagicMock(json=lambda: mock_env_data),
        ),
        patch("subprocess.run", return_value=MagicMock(stdout="Python 3.10")),
        patch(
            "qbraid_core.services.environments.get_default_envs_paths",
            return_value=[Path("/fake/path")],
        ),
        patch("qbraid_cli.envs.create.create_qbraid_env_assets"),
        patch("qbraid_cli.envs.create.create_venv"),
        patch("qbraid_cli.envs.data_handling.request_delete_env") as mock_request_delete_env,
    ):
        runner.invoke(
            envs_app,
            ["create", "--name", "test_env", "--description", "A test environment"],
            input=f"{user_confirmation}\n",
        )
        if not user_confirmation:
            mock_request_delete_env.assert_called_once_with("test-slug")


def test_envs_create_invalid_name():
    """Test creating an environment with an invalid name."""
    runner = CliRunner()

    with patch("qbraid_cli.envs.data_handling.validate_env_name"):
        result = runner.invoke(envs_app, ["create", "--name", "Invalid Env Name"])

        # Assert that the command failed with an error code indicating a bad parameter
        assert result.exit_code == 2, "Expected exit code 2 for a bad parameter"
