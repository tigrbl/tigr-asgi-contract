# Publishing

This repository uses a strict six-step release lifecycle:

1. **Generate**
2. **Test**
3. **Prepare**
4. **Promote**
5. **Publish**
6. **Release**

## Exact sequence

### Author sequence

1. Edit `contract/`
2. Run:
   - `uv sync --frozen`
   - `uv run --frozen python tools/validate_yaml.py`
   - `uv run --frozen python tools/validate_jsonschema.py`
   - `uv run --frozen python tools/build_manifest.py`
   - `uv run --frozen python tools/build_checksums.py`
   - `uv run --frozen python tools/generate_all.py`
   - `uv run --frozen python tools/check_versions.py`
   - `uv run --frozen python -m pytest -q`
3. Commit source contract changes and generated downstream outputs together.

### CI sequence

1. Validate YAML and JSON Schema on Python `3.10` through `3.14`.
2. Rebuild `manifest.json` and `checksums.txt` and fail if tracked files change.
3. Regenerate downstream packages and fail if tracked files change across the same Python matrix.
4. Run parity and packaging checks across:
   - Python `3.10` through `3.14`
   - Node `21` through `25`
   - Rust `1.91.0` through `1.95.0`
5. Generate and upload a bindings preview artifact automatically on pull requests, `main` pushes, merge queues, and the daily scheduled CI run.

### Promotion sequence

Promotion is the creation of an immutable release-candidate bundle.

The release-candidate workflow performs:

1. matrix validation across Python `3.10` through `3.14`, Node `21` through `25`, and Rust `1.91.0` through `1.95.0`
2. regeneration
3. clean-tree verification
4. package and release bundle build
5. bundle upload
6. optional GitHub release creation tagged as `tigr-asgi-contracts==<version>`

### Prepare sequence

Preparation bumps the unified repo version before promotion.

The `prepare-release` workflow performs:

1. version bump across `VERSION` and all package manifests
2. version consistency verification
3. commit and push of version-only metadata changes
4. dispatch of `release-candidate` with explicit GitHub Release toggle
5. optional dispatch of `publish` with explicit PyPI, npm, and crates.io toggles

### Publish sequence

Publishing uses the promoted candidate as the source of truth.

- PyPI publishes from the promoted wheel/sdist artifacts.
- PyPI build and publish use `uv build` and `uv publish`.
- npm publishes from the promoted tarballs, with an option to replay the most recent `1` to `5` release bundles.
- crates.io publishes from the promoted source tag / commit.

Required GitHub Actions secrets:

- PyPI trusted publishing configured for this repository and workflow identity
- npm trusted publishing configured for this repository, workflow identity, and package names
- `CRATES_API_TOKEN` for crates.io publishing

### Release sequence

The final GitHub release happens **after** ecosystem publication succeeds.

That means:

- do **not** create the final public release first
- publish to registries first
- finalize the GitHub release last

## Do GitHub workflows commit generation?

No.

GitHub workflows do not commit generated artifacts.

- authors generate and commit locally
- `prepare-release` may commit version metadata only
- CI regenerates and checks cleanliness
- release workflows regenerate in ephemeral workspaces only
- no workflow mutates the canonical history during validation, promotion, or publish
