# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Module supporting 'qbraid envs create' command.

"""
import json
import os
import shutil
import sys


def create_venv(*args, **kwargs) -> None:
    """Create a python virtual environment for the qBraid environment."""
    from qbraid_core.services.environments import create_local_venv

    return create_local_venv(*args, **kwargs)


def update_state_json(*ags, **kwargs) -> None:
    """Update the state.json file for the qBraid environment."""
    from qbraid_core.services.environments.state import update_install_status

    return update_install_status(*ags, **kwargs)


def create_qbraid_env_assets(slug: str, alias: str, kernel_name: str, slug_path: str) -> None:
    """Create a qBraid environment including python venv, PS1 configs,
    kernel resource files, and qBraid state.json."""
    from jupyter_client.kernelspec import KernelSpecManager

    local_resource_dir = os.path.join(slug_path, "kernels", f"python3_{slug}")
    os.makedirs(local_resource_dir, exist_ok=True)

    # create state.json
    update_state_json(slug_path, 0, 0, env_name=alias)

    # create kernel.json
    kernel_json_path = os.path.join(local_resource_dir, "kernel.json")
    kernel_spec_manager = KernelSpecManager()
    kernelspec_dict = kernel_spec_manager.get_all_specs()
    kernel_data = kernelspec_dict["python3"]["spec"]
    if sys.platform == "win32":
        python_exec_path = os.path.join(slug_path, "pyenv", "Scripts", "python.exe")
    else:
        python_exec_path = os.path.join(slug_path, "pyenv", "bin", "python")
    kernel_data["argv"][0] = python_exec_path
    kernel_data["display_name"] = kernel_name
    with open(kernel_json_path, "w", encoding="utf-8") as file:
        json.dump(kernel_data, file, indent=4)

    # copy logo files
    sys_resource_dir = kernelspec_dict["python3"]["resource_dir"]
    logo_files = ["logo-32x32.png", "logo-64x64.png", "logo-svg.svg"]

    for file in logo_files:
        sys_path = os.path.join(sys_resource_dir, file)
        loc_path = os.path.join(local_resource_dir, file)
        if os.path.isfile(sys_path):
            shutil.copy(sys_path, loc_path)
