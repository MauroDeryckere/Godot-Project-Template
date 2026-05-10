#!/usr/bin/env python3
"""Installs the GodotSteam GDExtension addon into the project.

Usage:
    python tools/install_godotsteam.py              # latest release
    python tools/install_godotsteam.py --version 4.18.1
    python tools/install_godotsteam.py --force      # reinstall

Downloads the release zip from https://codeberg.org/godotsteam/godotsteam,
extracts `addons/godotsteam/` into `godot/project/addons/godotsteam/`, and
writes a placeholder `steam_appid.txt` (480 = Spacewar, Steam's free test app).

You still need to enable the plugin in Godot via
Project Settings > Plugins, and replace `steam_appid.txt` with your real
Steam app ID before shipping.
"""

import argparse
import io
import json
import os
import shutil
import sys
import urllib.request
import zipfile

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GODOT_PROJECT = os.path.join(PROJECT_ROOT, "godot", "project")
ADDONS_DIR = os.path.join(GODOT_PROJECT, "addons")
ADDON_DIR = os.path.join(ADDONS_DIR, "godotsteam")
STEAM_APPID_PATH = os.path.join(GODOT_PROJECT, "steam_appid.txt")

API_BASE = "https://codeberg.org/api/v1/repos/godotsteam/godotsteam/releases"
ZIP_PREFIX = "addons/godotsteam/"


def fetch_release(version: str | None) -> dict:
    if version:
        url = f"{API_BASE}/tags/v{version}-gde"
    else:
        url = f"{API_BASE}/latest"
    with urllib.request.urlopen(url) as resp:
        return json.loads(resp.read())


def pick_zip_url(release: dict) -> str:
    assets = release.get("assets", [])
    zips = [a for a in assets if a.get("name", "").lower().endswith(".zip")]
    if not zips:
        raise RuntimeError(f"No .zip asset on release {release.get('tag_name')!r}.")
    preferred = [
        a for a in zips
        if "gdextension" in a["name"].lower() and "server" not in a["name"].lower()
    ]
    asset = preferred[0] if preferred else zips[0]
    return asset["browser_download_url"]


def extract_addon(data: bytes) -> int:
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        members = [n for n in zf.namelist() if n.startswith(ZIP_PREFIX) and not n.endswith("/")]
        if not members:
            raise RuntimeError(
                f"Zip does not contain '{ZIP_PREFIX}' — release format may have changed."
            )
        os.makedirs(ADDONS_DIR, exist_ok=True)
        for name in members:
            rel = name[len("addons/"):]
            target = os.path.join(ADDONS_DIR, rel.replace("/", os.sep))
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with zf.open(name) as src, open(target, "wb") as dst:
                shutil.copyfileobj(src, dst)
        return len(members)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Install the GodotSteam GDExtension addon."
    )
    parser.add_argument(
        "--version",
        help="GodotSteam version, e.g. 4.18.1. Defaults to latest.",
    )
    parser.add_argument(
        "--app-id",
        default="480",
        help="Steam app ID to write to steam_appid.txt (default 480 = Spacewar).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Reinstall even if the addon directory already exists.",
    )
    args = parser.parse_args()

    if not os.path.isdir(GODOT_PROJECT):
        print(f"Error: {GODOT_PROJECT} not found. Run this from the project root.")
        sys.exit(1)

    if os.path.isdir(ADDON_DIR):
        if not args.force:
            rel = os.path.relpath(ADDON_DIR, PROJECT_ROOT)
            print(f"GodotSteam already installed at {rel}.")
            print("Pass --force to reinstall.")
            sys.exit(0)
        shutil.rmtree(ADDON_DIR)

    release = fetch_release(args.version)
    print(f"Installing GodotSteam {release.get('tag_name', '?')}")

    url = pick_zip_url(release)
    print(f"Downloading {url}")
    with urllib.request.urlopen(url) as resp:
        data = resp.read()

    count = extract_addon(data)
    print(f"Extracted {count} files into {os.path.relpath(ADDON_DIR, PROJECT_ROOT)}")

    if not os.path.exists(STEAM_APPID_PATH):
        with open(STEAM_APPID_PATH, "w") as f:
            f.write(args.app_id + "\n")
        rel = os.path.relpath(STEAM_APPID_PATH, PROJECT_ROOT)
        print(f"Wrote {rel} with app id {args.app_id}")
    else:
        print(f"Kept existing {os.path.relpath(STEAM_APPID_PATH, PROJECT_ROOT)}")

    print()
    print("Next steps:")
    print("  1. Open the project in Godot.")
    print("  2. Enable 'GodotSteam GDExtension' under Project Settings > Plugins.")
    print("  3. Replace steam_appid.txt with your real Steam app ID before shipping.")
    print("  See https://godotsteam.com/tutorials/initializing/ for usage.")


if __name__ == "__main__":
    main()
