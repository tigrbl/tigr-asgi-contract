#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 fallback
    import tomli as tomllib

VERSION_RE = re.compile(
    r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-dev(?P<dev>0|[1-9]\d*))?$"
)
PYPROJECT_VERSION_RE = re.compile(
    r'^(?P<prefix>version\s*=\s*")(?P<version>[^"]+)(?P<suffix>"\s*)$',
    re.MULTILINE,
)
PACKAGE_JSON_VERSION_RE = re.compile(
    r'^(?P<prefix>\s*"version"\s*:\s*")(?P<version>[^"]+)(?P<suffix>"\s*,?\s*)$',
    re.MULTILINE,
)
CARGO_VERSION_RE = re.compile(
    r'^(?P<prefix>version\s*=\s*")(?P<version>[^"]+)(?P<suffix>"\s*)$',
    re.MULTILINE,
)

VERSION_PATHS = (
    Path("VERSION"),
    Path("packages/artifacts-py/pyproject.toml"),
    Path("packages/contract-py/pyproject.toml"),
    Path("packages/artifacts-npm/package.json"),
    Path("packages/contract-npm/package.json"),
    Path("packages/artifacts-rs/Cargo.toml"),
    Path("packages/contract-rs/Cargo.toml"),
)


def parse_version(value: str) -> tuple[int, int, int, int | None]:
    match = VERSION_RE.match(value.strip())
    if match is None:
        raise ValueError(f"Unsupported version format: {value!r}")
    dev = match.group("dev")
    return (
        int(match.group("major")),
        int(match.group("minor")),
        int(match.group("patch")),
        int(dev) if dev is not None else None,
    )


def bump_version(current_version: str, bump_type: str) -> str:
    major, minor, patch, dev = parse_version(current_version)
    is_prerelease = dev is not None
    if bump_type == "major":
        return f"{major + 1}.0.0-dev1"
    if bump_type == "minor":
        return f"{major}.{minor + 1}.0-dev1"
    if bump_type == "patch":
        if is_prerelease:
            return f"{major}.{minor}.{patch}-dev{dev + 1}"
        return f"{major}.{minor}.{patch + 1}-dev1"
    if bump_type == "finalize":
        if not is_prerelease:
            return current_version
        return f"{major}.{minor}.{patch}"
    raise ValueError("bump_type must be one of: major, minor, patch, finalize")


def read_pyproject_version(path: Path) -> str:
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    return data["project"]["version"]


def read_package_json_version(path: Path) -> str:
    return json.loads(path.read_text(encoding="utf-8"))["version"]


def read_cargo_version(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = CARGO_VERSION_RE.search(text)
    if match is None:
        raise RuntimeError(f"Could not find Cargo version in {path}")
    return match.group("version")


def read_plain_version(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def read_version(path: Path) -> str:
    if path.name == "pyproject.toml":
        return read_pyproject_version(path)
    if path.name == "package.json":
        return read_package_json_version(path)
    if path.name == "Cargo.toml":
        return read_cargo_version(path)
    if path.name == "VERSION":
        return read_plain_version(path)
    raise ValueError(f"Unsupported version file: {path}")


def _replace_first(path: Path, pattern: re.Pattern[str], current_version: str, new_version: str) -> None:
    content = path.read_text(encoding="utf-8")

    def _replace(match: re.Match[str]) -> str:
        if match.group("version") != current_version:
            return match.group(0)
        return f'{match.group("prefix")}{new_version}{match.group("suffix")}'

    updated, count = pattern.subn(_replace, content, count=1)
    if count == 0 or updated == content:
        raise RuntimeError(f"Failed to update version in {path}")
    path.write_text(updated, encoding="utf-8")


def write_version(path: Path, current_version: str, new_version: str) -> None:
    if path.name == "VERSION":
        path.write_text(f"{new_version}\n", encoding="utf-8")
        return
    if path.name == "pyproject.toml":
        _replace_first(path, PYPROJECT_VERSION_RE, current_version, new_version)
        return
    if path.name == "package.json":
        _replace_first(path, PACKAGE_JSON_VERSION_RE, current_version, new_version)
        return
    if path.name == "Cargo.toml":
        _replace_first(path, CARGO_VERSION_RE, current_version, new_version)
        return
    raise ValueError(f"Unsupported version file: {path}")


def current_version(root: Path) -> str:
    observed: dict[str, list[str]] = {}
    for relative_path in VERSION_PATHS:
        version = read_version(root / relative_path)
        observed.setdefault(version, []).append(relative_path.as_posix())
    if len(observed) != 1:
        details = [
            f"{version}: {', '.join(paths)}"
            for version, paths in sorted(observed.items())
        ]
        raise RuntimeError("Version files are out of sync:\n" + "\n".join(details))
    return next(iter(observed))


def bump_repo_version(root: Path, bump_type: str) -> tuple[str, str]:
    current = current_version(root)
    new_version = bump_version(current, bump_type)
    if new_version == current:
        return current, new_version
    for relative_path in VERSION_PATHS:
        write_version(root / relative_path, current, new_version)
    return current, new_version


def regenerate_derived_artifacts(root: Path) -> None:
    subprocess.run(
        [sys.executable, str(root / "tools/generate_all.py")],
        check=True,
        cwd=root,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Bump the unified release version across all package manifests.")
    parser.add_argument("--bump", required=True, choices=["major", "minor", "patch", "finalize"])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument(
        "--no-generate-derived",
        action="store_true",
        help="Skip regenerating derived artifacts after bumping versions.",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    _, new_version = bump_repo_version(root, args.bump)
    if not args.no_generate_derived:
        regenerate_derived_artifacts(root)
    for relative_path in VERSION_PATHS:
        print(relative_path.as_posix())
    print(f"new_version={new_version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
