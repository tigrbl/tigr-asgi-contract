from __future__ import annotations

import json
from pathlib import Path

import yaml

from tigr_asgi_contract import (
    EVENT_PAYLOAD_SCHEMA_PATHS,
    EVENT_SCHEMA_IDS,
    FRAME_PAYLOAD_SCHEMA_PATHS,
    FRAME_SCHEMA_IDS,
    event_has_payload_schema,
    event_payload_schema_path,
    frame_has_payload_schema,
    frame_payload_schema_path,
    validate_event_payload_schema,
    validate_frame_payload_schema,
)


ROOT = Path(__file__).resolve().parents[2]


def test_runtime_event_schema_registry_matches_contract_events() -> None:
    event_schema = json.loads((ROOT / "contract" / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
    event_ids = set(event_schema["properties"]["type"]["enum"])

    assert EVENT_SCHEMA_IDS == event_ids
    assert set(EVENT_PAYLOAD_SCHEMA_PATHS) == event_ids
    for event_type in event_ids:
        assert event_has_payload_schema(event_type)
        assert (ROOT / event_payload_schema_path(event_type)).is_file()


def test_runtime_frame_schema_registry_matches_contract_frames() -> None:
    frames = yaml.safe_load((ROOT / "contract" / "frames.yaml").read_text(encoding="utf-8"))["frames"]
    frame_ids = set(frames)

    assert FRAME_SCHEMA_IDS == frame_ids
    assert set(FRAME_PAYLOAD_SCHEMA_PATHS) == frame_ids
    for frame in frame_ids:
        assert frame_has_payload_schema(frame)
        assert (ROOT / frame_payload_schema_path(frame)).is_file()


def test_runtime_event_payload_schema_validation() -> None:
    assert validate_event_payload_schema(
        "webtransport.stream.receive",
        {
            "type": "webtransport.stream.receive",
            "stream_id": 1,
            "stream_direction": "client_to_server",
            "more": True,
        },
    )
    assert not validate_event_payload_schema(
        "webtransport.stream.receive",
        {"type": "webtransport.stream.receive", "stream_id": 1},
    )
    assert not validate_event_payload_schema(
        "webtransport.datagram.receive",
        {"type": "webtransport.datagram.receive"},
    )
    assert not validate_event_payload_schema(
        "http.request",
        {"type": "http.request", "subsurface": "http.rest.request.receive"},
    )
    assert not validate_event_payload_schema("not.real", {"type": "not.real"})


def test_runtime_frame_payload_schema_validation() -> None:
    assert validate_frame_payload_schema(
        "webtransport-stream-frame",
        {"frame": "webtransport-stream-frame", "stream_id": "s1", "stream_direction": "bidi"},
    )
    assert not validate_frame_payload_schema(
        "webtransport-stream-frame",
        {"frame": "webtransport-stream-frame", "stream_id": "s1"},
    )
    assert validate_frame_payload_schema(
        "webtransport-datagram-frame",
        {"frame": "webtransport-datagram-frame", "datagram_id": 1},
    )
    assert not validate_frame_payload_schema(
        "webtransport-datagram-frame",
        {"frame": "webtransport-datagram-frame"},
    )
    assert not validate_frame_payload_schema(
        "bytes",
        {"frame": "bytes", "subsurface": "bytes"},
    )
    assert not validate_frame_payload_schema("not-real", {"frame": "not-real"})
