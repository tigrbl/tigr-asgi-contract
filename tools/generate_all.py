from __future__ import annotations
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_DIRS = [
    ROOT / "packages" / "artifacts-py",
    ROOT / "packages" / "artifacts-npm",
    ROOT / "packages" / "artifacts-rs",
    ROOT / "packages" / "contract-py",
    ROOT / "packages" / "contract-npm",
    ROOT / "packages" / "contract-rs",
]

def run(path: str) -> None:
    subprocess.run([sys.executable, str(ROOT / path)], check=True)


def sync_package_licenses() -> None:
    license_bytes = (ROOT / "LICENSE").read_bytes()
    for package_dir in PACKAGE_DIRS:
        (package_dir / "LICENSE").write_bytes(license_bytes)

def main() -> None:
    run("tools/build_compatibility.py")
    run("tools/build_manifest.py")
    run("tools/build_checksums.py")
    run("generators/python/generate.py")
    run("generators/rust/generate.py")
    run("generators/ts/generate.py")
    run("tools/generate_readmes.py")
    sync_package_licenses()

if __name__ == "__main__":
    main()
