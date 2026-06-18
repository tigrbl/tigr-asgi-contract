from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[2] / "tools" / "bump_release_version.py"
SPEC = importlib.util.spec_from_file_location("bump_release_version", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC is not None and SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def write_files(root: Path, version: str) -> None:
    (root / "VERSION").write_text(f"{version}\n", encoding="utf-8")
    (root / "packages/artifacts-py").mkdir(parents=True, exist_ok=True)
    (root / "packages/contract-py").mkdir(parents=True, exist_ok=True)
    (root / "packages/artifacts-npm").mkdir(parents=True, exist_ok=True)
    (root / "packages/contract-npm").mkdir(parents=True, exist_ok=True)
    (root / "packages/artifacts-rs").mkdir(parents=True, exist_ok=True)
    (root / "packages/contract-rs").mkdir(parents=True, exist_ok=True)

    (root / "packages/artifacts-py/pyproject.toml").write_text(
        f'[project]\nname = "pkg-artifacts"\nversion = "{version}"\n',
        encoding="utf-8",
    )
    (root / "packages/contract-py/pyproject.toml").write_text(
        f'[project]\nname = "pkg-contract"\nversion = "{version}"\n',
        encoding="utf-8",
    )
    (root / "packages/artifacts-npm/package.json").write_text(
        '{\n  "name": "@tigrbljs/tigr-asgi-contract-artifacts",\n  "version": "' + version + '"\n}\n',
        encoding="utf-8",
    )
    (root / "packages/contract-npm/package.json").write_text(
        '{\n  "name": "@tigrbljs/tigr-asgi-contract",\n  "version": "' + version + '"\n}\n',
        encoding="utf-8",
    )
    (root / "packages/artifacts-rs/Cargo.toml").write_text(
        f'[package]\nname = "tigr_artifacts"\nversion = "{version}"\n',
        encoding="utf-8",
    )
    (root / "packages/contract-rs/Cargo.toml").write_text(
        f'[package]\nname = "tigr_contract"\nversion = "{version}"\n',
        encoding="utf-8",
    )


def test_bump_version_semver() -> None:
    assert MODULE.bump_version("0.1.0", "patch") == "0.1.1-dev1"
    assert MODULE.bump_version("0.1.0", "minor") == "0.2.0-dev1"
    assert MODULE.bump_version("0.1.0", "major") == "1.0.0-dev1"
    assert MODULE.bump_version("0.1.1-dev1", "patch") == "0.1.1-dev2"
    assert MODULE.bump_version("0.1.1-dev2", "finalize") == "0.1.1"
    assert MODULE.bump_version("0.1.1", "finalize") == "0.1.1"


def test_bump_repo_version_updates_all_files(tmp_path: Path) -> None:
    write_files(tmp_path, "0.1.0")

    current, new = MODULE.bump_repo_version(tmp_path, "minor")

    assert current == "0.1.0"
    assert new == "0.2.0-dev1"
    for relative_path in MODULE.VERSION_PATHS:
        assert MODULE.read_version(tmp_path / relative_path) == "0.2.0-dev1"


def test_finalize_repo_version_updates_all_files(tmp_path: Path) -> None:
    write_files(tmp_path, "0.2.0-dev2")

    current, new = MODULE.bump_repo_version(tmp_path, "finalize")

    assert current == "0.2.0-dev2"
    assert new == "0.2.0"
    for relative_path in MODULE.VERSION_PATHS:
        assert MODULE.read_version(tmp_path / relative_path) == "0.2.0"


def test_bump_repo_version_requires_consistent_versions(tmp_path: Path) -> None:
    write_files(tmp_path, "0.1.0")
    (tmp_path / "packages/contract-py/pyproject.toml").write_text(
        '[project]\nname = "pkg-contract"\nversion = "0.1.1"\n',
        encoding="utf-8",
    )

    with pytest.raises(RuntimeError, match="out of sync"):
        MODULE.bump_repo_version(tmp_path, "patch")
