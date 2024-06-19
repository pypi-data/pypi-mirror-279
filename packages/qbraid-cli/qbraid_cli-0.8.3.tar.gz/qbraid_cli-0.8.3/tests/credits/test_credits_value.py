# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Unit tests for the 'qbraid credits value' command.

"""
from unittest.mock import patch

from typer.testing import CliRunner

from qbraid_cli.credits import credits_app

runner = CliRunner()


def test_credits_value_success():
    """Test the 'qbraid credits value' command with a successful response."""
    credits_value = 100.4573

    class MockQbraidClient:  # pylint: disable=too-few-public-methods
        """Mock class for the QbraidClient."""

        def user_credits_value(self):
            """ "Mock user_credits_value method."""
            return credits_value

    with (
        patch("qbraid_cli.handlers.run_progress_task") as mock_run_progress_task,
        patch("qbraid_core.QbraidClient") as mock_qbraid_client,
    ):

        mock_response = credits_value
        mock_qbraid_client.return_value = MockQbraidClient()

        # Setup mock for run_progress_task to return the credits directly
        mock_run_progress_task.return_value = mock_response

        result = runner.invoke(credits_app)

        assert "qBraid credits remaining:" in result.output
        assert str(credits_value) in result.output
        assert result.exit_code == 0
