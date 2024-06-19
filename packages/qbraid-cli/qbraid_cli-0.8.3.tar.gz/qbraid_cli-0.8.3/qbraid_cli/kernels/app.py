# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Module defining commands in the 'qbraid jobs' namespace.

"""
import sys
from pathlib import Path

import typer
from jupyter_client.kernelspec import KernelSpecManager
from rich.console import Console

from qbraid_cli.handlers import handle_error

kernels_app = typer.Typer(help="Manage qBraid kernels.")


def _get_kernels_path(environment: str) -> Path:
    """Get the path to the kernels directory for the given environment."""
    # pylint: disable-next=import-outside-toplevel
    from qbraid_core.services.environments.paths import installed_envs_data

    slug_to_path, name_to_slug = installed_envs_data()

    if environment in name_to_slug:
        slug = name_to_slug.get(environment, None)
    else:
        slug = environment

    if slug not in slug_to_path:
        raise ValueError(f"Environment '{environment}' not found.")

    env_path = slug_to_path[slug]
    kernels_path = env_path / "kernels"
    return kernels_path


@kernels_app.command(name="list")
def kernels_list():
    """List all available kernels."""
    console = Console()

    kernel_spec_manager = KernelSpecManager()
    kernelspecs = kernel_spec_manager.get_all_specs()

    if len(kernelspecs) == 0:
        console.print("No qBraid kernels are active.")
        console.print("\nUse 'qbraid kernels add' to add a new kernel.")
        return

    longest_kernel_name = max(len(kernel_name) for kernel_name in kernelspecs)
    spacing = longest_kernel_name + 10

    output_lines = ["# qbraid kernels:\n#\n"]

    default_kernel_name = "python3"
    python3_kernel_info = kernelspecs.pop(default_kernel_name, None)
    if python3_kernel_info:
        python3_line = f"{default_kernel_name.ljust(spacing)}{python3_kernel_info['resource_dir']}"
        output_lines.append(python3_line)

    for kernel_name, kernel_info in sorted(kernelspecs.items()):
        line = f"{kernel_name.ljust(spacing)}{kernel_info['resource_dir']}"
        output_lines.append(line)

    final_output = "\n".join(output_lines)

    console.print(final_output)


@kernels_app.command(name="add")
def kernels_add(
    environment: str = typer.Argument(
        ..., help="Name of environment for which to add ipykernel. Values from 'qbraid envs list'."
    )
):
    """Add a kernel."""

    try:
        kernels_path = _get_kernels_path(environment)
    except ValueError:
        handle_error(message=f"Environment '{environment}' not found.", include_traceback=False)
        return

    is_local = str(kernels_path).startswith(str(Path.home()))
    resource_path = str(Path.home() / ".local") if is_local else sys.prefix

    kernel_spec_manager = KernelSpecManager()

    for kernel in kernels_path.iterdir():
        kernel_spec_manager.install_kernel_spec(source_dir=str(kernel), prefix=resource_path)


@kernels_app.command(name="remove")
def kernels_remove(
    environment: str = typer.Argument(
        ...,
        help=("Name of environment for which to remove ipykernel. Values from 'qbraid envs list'."),
    )
):
    """Remove a kernel."""
    try:
        kernels_path = _get_kernels_path(environment)
    except ValueError:
        handle_error(message=f"Environment '{environment}' not found.", include_traceback=False)
        return

    kernel_spec_manager = KernelSpecManager()

    for kernel in kernels_path.iterdir():
        kernel_spec_manager.remove_kernel_spec(kernel.name)


if __name__ == "__main__":
    kernels_app()
