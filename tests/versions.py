#!/usr/bin/env python3

import subprocess

import tomllib


def get_version_from_git():
    cmd = "git describe --tags --abbrev=0".split()
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        print(f"Could not get version from git\nCaptured stdout:\n{result.stdout}\nCaptured stderr:\n{result.stderr}")
        return None
    return result.stdout.decode().rstrip("\n")


def get_version_from_pyproject():
    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)
        return "v" + data["project"]["version"]


if __name__ == "__main__":
    versions = [
        get_version_from_git(),
        get_version_from_pyproject(),
    ]
    assert all(v == versions[0] for v in versions), f"Versions are different: {versions}"
