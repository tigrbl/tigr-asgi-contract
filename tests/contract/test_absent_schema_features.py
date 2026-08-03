from __future__ import annotations

import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

from tigr_asgi_contract import (
    CONTRACT_ARTIFACT_SCHEMA_PATHS,
    event_payload_schema_path_for_payload,
    frame_payload_schema_path_for_payload,
    validate_event_payload_discriminator,
    validate_frame_payload_discriminator,
)


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "contract"


EXPECTED_ARTIFACT_SCHEMAS = {
    "bindings.yaml",
    "capabilities.yaml",
    "exchanges.yaml",
    "families.yaml",
    "ids.yaml",
    "manifest.json",
    "scope_types.yaml",
    "subevents.yaml",
    "surfaces.yaml",
}


def _load_artifact(path: str) -> object:
    target = CONTRACT / path
    if target.suffix == ".json":
        return json.loads(target.read_text(encoding="utf-8"))
    return yaml.safe_load(target.read_text(encoding="utf-8"))


def _load_schema(schema_path: str) -> dict:
    return json.loads((ROOT / schema_path).read_text(encoding="utf-8"))


def test_absent_top_level_artifact_schemas_exist_and_validate_artifacts() -> None:
    assert set(CONTRACT_ARTIFACT_SCHEMA_PATHS) == EXPECTED_ARTIFACT_SCHEMAS

    for artifact_path, schema_path in CONTRACT_ARTIFACT_SCHEMA_PATHS.items():
        schema_file = ROOT / schema_path
        assert schema_file.is_file(), artifact_path
        schema = _load_schema(schema_path)
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(_load_artifact(artifact_path))


def test_top_level_artifact_schemas_fail_closed_on_wrong_root_key() -> None:
    for artifact_path, schema_path in CONTRACT_ARTIFACT_SCHEMA_PATHS.items():
        schema = _load_schema(schema_path)
        assert not Draft202012Validator(schema).is_valid({"not_the_contract_artifact": []}), artifact_path


def test_frames_registry_links_every_frame_to_existing_payload_schema() -> None:
    frames = yaml.safe_load((CONTRACT / "frames.yaml").read_text(encoding="utf-8"))["frames"]
    for frame, metadata in frames.items():
        expected = f"contract/schemas/frames/{frame}.schema.json"
        assert metadata["schema"] == expected
        assert (ROOT / metadata["schema"]).is_file()


def test_event_schema_dispatch_uses_canonical_type_discriminator() -> None:
    payload = {
        "type": "webtransport.stream.receive",
        "stream_id": 7,
            "stream_direction": "bidi",
            "body": "chunk",
            "more": True,
    }
    assert event_payload_schema_path_for_payload(payload) == (
        "contract/schemas/events/webtransport.stream.receive.schema.json"
    )
    assert validate_event_payload_discriminator(payload)
    assert not validate_event_payload_discriminator({"type": "webtransport.stream.receive", "stream_id": 7})
    assert not validate_event_payload_discriminator({"type": "not.real"})
    assert not validate_event_payload_discriminator({"stream_id": 7})


def test_frame_schema_dispatch_uses_frame_discriminator() -> None:
    payload = {
        "frame": "webtransport-stream-frame",
        "stream_id": 7,
        "stream_direction": "server_to_client",
    }
    assert frame_payload_schema_path_for_payload(payload) == (
        "contract/schemas/frames/webtransport-stream-frame.schema.json"
    )
    assert validate_frame_payload_discriminator(payload)
    assert not validate_frame_payload_discriminator({"frame": "webtransport-stream-frame", "stream_id": 7})
    assert not validate_frame_payload_discriminator({"frame": "not-real"})
    assert not validate_frame_payload_discriminator({"stream_id": 7})
