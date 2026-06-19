#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import tarfile
from dataclasses import dataclass
from pathlib import Path

VERSION_RE = re.compile(
    r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-dev(?P<dev>0|[1-9]\d*))?$"
)


@dataclass(frozen=True)
class NpmTarball:
    path: Path
    package_name: str
    version: str


def parse_version(version: str) -> tuple[int, int, int, int, int]:
    match = VERSION_RE.match(version)
    if match is None:
        raise ValueError(f"Unsupported npm version format: {version!r}")
    dev = match.group("dev")
    prerelease_flag = 0 if dev is None else -1
    dev_number = 0 if dev is None else int(dev)
    return (
        int(match.group("major")),
        int(match.group("minor")),
        int(match.group("patch")),
        prerelease_flag,
        dev_number,
    )


def read_tarball_metadata(path: Path) -> NpmTarball:
    with tarfile.open(path, "r:gz") as archive:
        member = archive.getmember("package/package.json")
        payload = json.load(archive.extractfile(member))
    return NpmTarball(path=path, package_name=payload["name"], version=payload["version"])


def npm_version_exists(package_name: str, version: str) -> bool:
    npm_env = build_npm_env()
    result = subprocess.run(
        ["npm", "view", f"{package_name}@{version}", "version", "--json"],
        check=False,
        capture_output=True,
        text=True,
        env=npm_env,
    )
    return result.returncode == 0 and result.stdout.strip() not in {"", "null"}


def build_npm_env() -> dict[str, str]:
    env = os.environ.copy()
    if env.get("GITHUB_ACTIONS"):
        env.pop("NODE_AUTH_TOKEN", None)
        env.pop("NPM_TOKEN", None)
        env.pop("NPM_CONFIG_ALWAYS_AUTH", None)
        env.pop("NPM_CONFIG_USERCONFIG", None)
        return env
    token = env.get("NODE_AUTH_TOKEN") or env.get("NPM_TOKEN")
    if token:
        env["NODE_AUTH_TOKEN"] = token
        env["NPM_TOKEN"] = token
        env.setdefault("NPM_CONFIG_REGISTRY", "https://registry.npmjs.org/")
        env.setdefault("NPM_CONFIG_ALWAYS_AUTH", "true")
    return env


def publish_tarball(tarball: NpmTarball) -> None:
    if npm_version_exists(tarball.package_name, tarball.version):
        print(f"skip existing {tarball.package_name}@{tarball.version}")
        return
    npm_env = build_npm_env()
    if not (npm_env.get("NODE_AUTH_TOKEN") or npm_env.get("NPM_TOKEN") or npm_env.get("GITHUB_ACTIONS")):
        raise RuntimeError(
            "npm authentication missing. Set NODE_AUTH_TOKEN/NPM_TOKEN or run from "
            "GitHub Actions with npm trusted publishing configured."
        )
    subprocess.run(
        ["npm", "publish", str(tarball.path), "--access", "public", "--registry", "https://registry.npmjs.org/"],
        check=True,
        env=npm_env,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish npm tarballs from downloaded release bundles.")
    parser.add_argument("--root", type=Path, required=True, help="Root directory containing downloaded *.tgz files.")
    args = parser.parse_args()

    tarballs = [read_tarball_metadata(path) for path in sorted(args.root.rglob("*.tgz"))]
    for tarball in sorted(tarballs, key=lambda item: (parse_version(item.version), item.package_name)):
        publish_tarball(tarball)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
