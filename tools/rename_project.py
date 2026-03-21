#!/usr/bin/env python3
"""Renames the Godot project.

Usage:
    python tools/rename_project.py <new_name>

Example:
    python tools/rename_project.py "My Cool Game"

This will:
    - Update config/name in project.godot
    - Update project/assembly_name in project.godot (for .NET builds)
"""

import sys
import os
import re

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_GODOT = os.path.join(PROJECT_ROOT, "godot", "project", "project.godot")


def rename_project(new_name: str) -> None:
    if not os.path.isfile(PROJECT_GODOT):
        print(f"Error: {PROJECT_GODOT} not found.")
        sys.exit(1)

    with open(PROJECT_GODOT, "r") as f:
        content = f.read()

    original = content

    content = re.sub(
        r'(config/name=)".*"',
        rf'\1"{new_name}"',
        content,
    )
    content = re.sub(
        r'(project/assembly_name=)".*"',
        rf'\1"{new_name}"',
        content,
    )

    if content == original:
        print(f"Project is already named \"{new_name}\".")
        return

    with open(PROJECT_GODOT, "w") as f:
        f.write(content)

    rel_path = os.path.relpath(PROJECT_GODOT, PROJECT_ROOT)
    print(f"Renamed project to \"{new_name}\" in {rel_path}")


def main() -> None:
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    new_name = sys.argv[1]

    if not new_name.strip():
        print("Error: project name cannot be empty.")
        sys.exit(1)

    rename_project(new_name)


if __name__ == "__main__":
    main()
