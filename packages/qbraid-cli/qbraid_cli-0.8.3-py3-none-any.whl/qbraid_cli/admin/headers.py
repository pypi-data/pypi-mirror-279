# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Script to verify qBraid copyright file headers

"""
import os
from typing import List, Optional

import typer
from rich.console import Console

from qbraid_cli.handlers import handle_error

# pylint: disable=too-many-branches,too-many-statements

DEFAULT_HEADER = """# Copyright (c) 2024, qBraid Development Team
# All rights reserved.
"""

DEFAULT_HEADER_GPL = """# Copyright (C) 2024 qBraid
#
# This file is part of the qBraid-SDK
#
# The qBraid-SDK is free software released under the GNU General Public License v3
# or later. You can redistribute and/or modify it under the terms of the GPL v3.
# See the LICENSE file in the project root or <https://www.gnu.org/licenses/gpl-3.0.html>.
#
# THERE IS NO WARRANTY for the qBraid-SDK, as per Section 15 of the GPL v3.
"""

HEADER_TYPES = {
    "default": DEFAULT_HEADER,
    "gpl": DEFAULT_HEADER_GPL,
}


def check_and_fix_headers(
    src_paths: List[str],
    header_type: str = "default",
    skip_files: Optional[List[str]] = None,
    fix: bool = False,
) -> None:
    """Script to add or verify qBraid copyright file headers"""
    try:
        header = HEADER_TYPES[header_type]
    except KeyError:
        handle_error(
            error_type="ValueError",
            message=(
                f"Invalid header type: {HEADER_TYPES}. Expected one of {list(HEADER_TYPES.keys())}"
            ),
        )

    for path in src_paths:
        if not os.path.exists(path):
            handle_error(error_type="FileNotFoundError", message=f"Path '{path}' does not exist.")

    header_2023 = header.replace("2024", "2023")

    skip_files = skip_files or []

    failed_headers = []
    fixed_headers = []

    console = Console()

    def should_skip(file_path: str, content: str) -> bool:
        if file_path in skip_files:
            return True

        if os.path.basename(file_path) == "__init__.py":
            return not content.strip()

        skip_header_tag = "# qbraid: skip-header"
        line_number = 0

        for line in content.splitlines():
            line_number += 1
            if 5 <= line_number <= 30 and skip_header_tag in line:
                return True
            if line_number > 30:
                break

        return False

    def replace_or_add_header(file_path: str, fix: bool = False) -> None:
        with open(file_path, "r", encoding="ISO-8859-1") as f:
            content = f.read()

        # This finds the start of the actual content after skipping initial whitespace and comments.
        lines = content.splitlines()
        first_non_comment_line_index = next(
            (i for i, line in enumerate(lines) if not line.strip().startswith("#")), None
        )

        # Prepare the content by stripping leading and trailing whitespace and separating into lines
        actual_content = (
            "\n".join(lines[first_non_comment_line_index:]).strip()
            if first_non_comment_line_index is not None
            else ""
        )

        # Check if the content already starts with the header or if the file should be skipped
        if (
            content.lstrip().startswith(header)
            or content.lstrip().startswith(header_2023)
            or should_skip(file_path, content)
        ):
            return

        if not fix:
            failed_headers.append(file_path)
        else:
            # Form the new content by combining the header, one blank line, and the actual content
            new_content = header.strip() + "\n\n" + actual_content
            with open(file_path, "w", encoding="ISO-8859-1") as f:
                f.write(new_content)
            fixed_headers.append(file_path)

    def process_files_in_directory(directory: str, fix: bool = False) -> int:
        count = 0
        if not os.path.isdir(directory):
            return count
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    replace_or_add_header(file_path, fix)
                    count += 1
        return count

    checked = 0
    for item in src_paths:
        if os.path.isdir(item):
            checked += process_files_in_directory(item, fix)
        elif os.path.isfile(item) and item.endswith(".py"):
            replace_or_add_header(item, fix)
            checked += 1
        else:
            handle_error(error_type="FileNotFoundError", message=f"Path '{item}' does not exist.")

    if checked == 0:
        console.print("[bold]No Python files present. Nothing to do[/bold] 😴")
        raise typer.Exit(0)

    if not fix:
        if failed_headers:
            for file in failed_headers:
                console.print(f"[bold]would fix {file}[/bold]")
            num_failed = len(failed_headers)
            num_passed = checked - num_failed
            s1, s2 = ("", "s") if num_failed == 1 else ("s", "")
            s_passed = "" if num_passed == 1 else "s"
            console.print("[bold]\nOh no![/bold] 💥 💔 💥")
            if num_passed > 0:
                punc = ", "
                passed_msg = f"[blue]{num_passed}[/blue] file{s_passed} would be left unchanged."
            else:
                punc = "."
                passed_msg = ""

            failed_msg = f"[bold][blue]{num_failed}[/blue] file{s1} need{s2} updating{punc}[/bold]"
            console.print(f"{failed_msg}{passed_msg}")
            raise typer.Exit(1)

        s_checked = "" if checked == 1 else "s"
        console.print("[bold]All done![/bold] ✨ 🚀 ✨")
        console.print(f"[blue]{checked}[/blue] file{s_checked} would be left unchanged.")
        raise typer.Exit(0)

    for file in fixed_headers:
        console.print(f"[bold]fixed {file}[/bold]")
    num_fixed = len(fixed_headers)
    num_ok = checked - num_fixed
    s_fixed = "" if num_fixed == 1 else "s"
    s_ok = "" if num_ok == 1 else "s"
    console.print("\n[bold]All done![/bold] ✨ 🚀 ✨")
    if num_ok > 0:
        punc = ", "
        unchanged_msg = f"[blue]{num_ok}[/blue] file{s_ok} left unchanged."
    else:
        punc = "."
        unchanged_msg = ""

    if num_fixed > 0:
        fixed_msg = f"[bold][blue]{num_fixed}[/blue] file{s_fixed} fixed{punc}[/bold]"
    else:
        fixed_msg = ""

    console.print(f"{fixed_msg}{unchanged_msg}")
    raise typer.Exit(0)
