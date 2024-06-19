# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Module defining commands in the 'qbraid envs' namespace.

"""

import shutil
import subprocess
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Tuple

import typer
from rich.console import Console

from qbraid_cli.envs.create import create_qbraid_env_assets, create_venv
from qbraid_cli.envs.data_handling import get_envs_data as installed_envs_data
from qbraid_cli.envs.data_handling import validate_env_name
from qbraid_cli.handlers import QbraidException, run_progress_task

if TYPE_CHECKING:
    from qbraid_core.services.environments.client import EnvironmentManagerClient as EMC

envs_app = typer.Typer(help="Manage qBraid environments.")


@envs_app.command(name="create")
def envs_create(  # pylint: disable=too-many-statements
    name: str = typer.Option(
        ..., "--name", "-n", help="Name of the environment to create", callback=validate_env_name
    ),
    description: Optional[str] = typer.Option(
        None, "--description", "-d", help="Short description of the environment"
    ),
    auto_confirm: bool = typer.Option(
        False, "--yes", "-y", help="Automatically answer 'yes' to all prompts"
    ),
) -> None:
    """Create a new qBraid environment."""
    env_description = description or ""

    def create_environment(*args, **kwargs) -> "Tuple[dict, EMC]":
        """Create a qBraid environment."""
        from qbraid_core.services.environments.client import EnvironmentManagerClient

        client = EnvironmentManagerClient()
        return client.create_environment(*args, **kwargs), client

    def gather_local_data() -> Tuple[Path, str]:
        """Gather environment data and return the slug."""
        from qbraid_core.services.environments import get_default_envs_paths

        env_path = get_default_envs_paths()[0]

        result = subprocess.run(
            [sys.executable, "--version"],
            capture_output=True,
            text=True,
            check=True,
        )

        python_version = result.stdout or result.stderr

        return env_path, python_version

    environment, emc = run_progress_task(
        create_environment,
        name,
        env_description,
        description="Validating request...",
        error_message="Failed to create qBraid environment",
    )

    env_path, python_version = run_progress_task(
        gather_local_data,
        description="Solving environment...",
        error_message="Failed to create qBraid environment",
    )
    slug = environment.get("slug")
    display_name = environment.get("displayName")
    prompt = environment.get("prompt")
    description = environment.get("description")
    tags = environment.get("tags")
    kernel_name = environment.get("kernelName")

    slug_path = env_path / slug
    description = "None" if description == "" else description

    typer.echo("\n\n## qBraid Metadata ##\n")
    typer.echo(f"  name: {display_name}")
    typer.echo(f"  description: {description}")
    typer.echo(f"  tags: {tags}")
    typer.echo(f"  slug: {slug}")
    typer.echo(f"  shellPrompt: {prompt}")
    typer.echo(f"  kernelName: {kernel_name}")

    typer.echo("\n\n## Environment Plan ##\n")
    typer.echo(f"  location: {slug_path}")
    typer.echo(f"  version: {python_version}\n")

    user_confirmation = auto_confirm or typer.confirm("Proceed", default=True)
    typer.echo("")
    if not user_confirmation:
        emc.delete_environment(slug)
        typer.echo("qBraidSystemExit: Exiting.")
        raise typer.Exit()

    run_progress_task(
        create_qbraid_env_assets,
        slug,
        prompt,
        kernel_name,
        slug_path,
        description="Generating qBraid assets...",
        error_message="Failed to create qBraid environment",
    )

    run_progress_task(
        create_venv,
        slug_path,
        prompt,
        description="Creating virtual environment...",
        error_message="Failed to create qBraid environment",
    )

    console = Console()
    console.print(
        f"\n[bold green]Successfully created qBraid environment: "
        f"[/bold green][bold magenta]{name}[/bold magenta]\n"
    )
    typer.echo("# To activate this environment, use")
    typer.echo("#")
    typer.echo(f"#     $ qbraid envs activate {name}")
    typer.echo("#")
    typer.echo("# To deactivate an active environment, use")
    typer.echo("#")
    typer.echo("#     $ deactivate")


@envs_app.command(name="remove")
def envs_remove(
    name: str = typer.Option(..., "-n", "--name", help="Name of the environment to remove"),
    auto_confirm: bool = typer.Option(
        False, "--yes", "-y", help="Automatically answer 'yes' to all prompts"
    ),
) -> None:
    """Delete a qBraid environment."""

    def delete_environment(slug: str) -> None:
        """Delete a qBraid environment."""
        from qbraid_core.services.environments.client import EnvironmentManagerClient

        emc = EnvironmentManagerClient()
        emc.delete_environment(slug)

    def gather_local_data(env_name: str) -> Tuple[Path, str]:
        """Get environment path and slug from name (alias)."""
        installed, aliases = installed_envs_data()
        for alias, slug in aliases.items():
            if alias == env_name:
                path = installed[slug]

                return path, slug

        raise QbraidException(f"Environment '{name}' not found.")

    slug_path, slug = gather_local_data(name)

    confirmation_message = (
        f"⚠️  Warning: You are about to delete the environment '{name}' "
        f"located at '{slug_path}'.\n"
        "This will remove all local packages and permanently delete all "
        "of its associated qBraid environment metadata.\n"
        "This operation CANNOT be undone.\n\n"
        "Are you sure you want to continue?"
    )

    if auto_confirm or typer.confirm(confirmation_message, abort=True):
        typer.echo("")
        run_progress_task(
            delete_environment,
            slug,
            description="Deleting remote environment data...",
            error_message="Failed to delete qBraid environment",
        )

        run_progress_task(
            shutil.rmtree,
            slug_path,
            description="Deleting local environment...",
            error_message="Failed to delete qBraid environment",
        )
        typer.echo(f"\nEnvironment '{name}' successfully removed.")


@envs_app.command(name="list")
def envs_list():
    """List installed qBraid environments."""
    installed, aliases = installed_envs_data()

    console = Console()

    if len(installed) == 0:
        console.print(
            "No qBraid environments installed.\n\n"
            + "Use 'qbraid envs create' to create a new environment.",
            style="yellow",
        )
        return

    alias_path_pairs = [(alias, installed[slug_name]) for alias, slug_name in aliases.items()]
    sorted_alias_path_pairs = sorted(
        alias_path_pairs,
        key=lambda x: (x[0] != "default", str(x[1]).startswith(str(Path.home())), x[0]),
    )

    current_env_path = Path(sys.executable).parent.parent.parent

    max_alias_length = (
        max(len(str(alias)) for alias, envpath in sorted_alias_path_pairs)
        if sorted_alias_path_pairs
        else 0
    )

    output_lines = []
    output_lines.append("# qbraid environments:")
    output_lines.append("#")
    output_lines.append("")

    for alias, path in sorted_alias_path_pairs:
        mark = "*" if path == current_env_path else " "
        line = f"{alias.ljust(max_alias_length + 3)}{mark} {path}"
        output_lines.append(line)

    final_output = "\n".join(output_lines)

    console.print(final_output)


@envs_app.command(name="activate")
def envs_activate(
    name: str = typer.Argument(..., help="Name of the environment. Values from 'qbraid envs list'.")
):
    """Activate qBraid environment.

    NOTE: Currently only works on qBraid Lab platform, and select few other OS types.
    """
    installed, aliases = installed_envs_data()
    if name in aliases:
        venv_path: Path = installed[aliases[name]] / "pyenv"
    elif name in installed:
        venv_path: Path = installed[name] / "pyenv"
    else:
        raise typer.BadParameter(f"Environment '{name}' not found.")

    from .activate import activate_pyvenv

    activate_pyvenv(venv_path)


if __name__ == "__main__":
    envs_app()
