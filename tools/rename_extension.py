#!/usr/bin/env python3
"""Renames a GDExtension throughout the project.

Usage:
    python tools/rename_extension.py <old_name> <new_name>

Example:
    python tools/rename_extension.py myextension my_game

This will:
    - Rename the CMake target
    - Rename the init function (<old_name>_init -> <new_name>_init)
    - Update library paths in the .gdextension file
    - Rename the .gdextension file itself
    - Update the project name in the top-level CMakeLists.txt
"""

import sys
import os
import re

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKIP_DIRS = {".git", ".godot", "third_party", "build", "godot"}

SEARCH_EXTENSIONS = {".cpp", ".hpp", ".h", ".txt", ".cmake"}


def validate_name(name: str, label: str) -> None:
    if not re.match(r"^[a-z][a-z0-9_]*$", name):
        print(f"Error: {label} '{name}' is not a valid name.")
        print("Use lowercase letters, numbers, and underscores. Must start with a letter.")
        sys.exit(1)


def find_source_files() -> list[str]:
    """Find all source and build files that could contain extension references."""
    files = []
    for root, dirs, filenames in os.walk(PROJECT_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for filename in filenames:
            if os.path.splitext(filename)[1] in SEARCH_EXTENSIONS:
                files.append(os.path.join(root, filename))
    return files


def find_gdextension_files(name: str) -> list[str]:
    """Find all .gdextension files matching the given name under godot/."""
    godot_dir = os.path.join(PROJECT_ROOT, "godot")
    if not os.path.isdir(godot_dir):
        return []

    skip = {".godot", "build"}
    files = []
    for root, dirs, filenames in os.walk(godot_dir):
        dirs[:] = [d for d in dirs if d not in skip]
        if f"{name}.gdextension" in filenames:
            files.append(os.path.join(root, f"{name}.gdextension"))
    return files


def replace_in_file(filepath: str, replacements: list[tuple[str, str]]) -> bool:
    with open(filepath, "r") as f:
        content = f.read()

    original = content
    for old, new in replacements:
        content = content.replace(old, new)

    if content == original:
        return False

    with open(filepath, "w") as f:
        f.write(content)
    return True


def main() -> None:
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    old_name = sys.argv[1]
    new_name = sys.argv[2]

    validate_name(old_name, "old name")
    validate_name(new_name, "new name")

    if old_name == new_name:
        print("Error: old and new names are the same.")
        sys.exit(1)

    old_init = f"{old_name}_init"
    new_init = f"{new_name}_init"

    print(f"Renaming extension: {old_name} -> {new_name}")
    print(f"Init function: {old_init} -> {new_init}")
    print()

    # Order matters: replace the longer init name first to avoid partial matches
    replacements = [
        (old_init, new_init),
        (old_name, new_name),
    ]

    found_anything = False

    # Update source and build files
    for filepath in find_source_files():
        if replace_in_file(filepath, replacements):
            print(f"  Updated {os.path.relpath(filepath, PROJECT_ROOT)}")
            found_anything = True

    # Update, rename, and clean up .gdextension files
    for gdext_path in find_gdextension_files(old_name):
        rel_dir = os.path.relpath(os.path.dirname(gdext_path), PROJECT_ROOT)
        new_gdext_path = os.path.join(os.path.dirname(gdext_path), f"{new_name}.gdextension")
        uid_path = gdext_path + ".uid"

        replace_in_file(gdext_path, replacements)
        print(f"  Updated {rel_dir}/{old_name}.gdextension")

        os.rename(gdext_path, new_gdext_path)
        print(f"  Renamed {rel_dir}/{old_name}.gdextension -> {new_name}.gdextension")

        if os.path.exists(uid_path):
            os.remove(uid_path)
            print(f"  Removed {rel_dir}/{old_name}.gdextension.uid (Godot will regenerate it)")

        found_anything = True

    if not found_anything:
        print(f"  No references to '{old_name}' found. Is the name correct?")
        sys.exit(1)

    print()
    print("Done. Remember to re-run cmake to pick up the changes:")
    print("  cmake --preset debug")
    print("  cmake --build --preset debug")


if __name__ == "__main__":
    main()
