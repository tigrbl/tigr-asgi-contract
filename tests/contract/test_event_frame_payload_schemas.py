from __future__ import annotations

import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "contract" / "schemas"


def _load_schema(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _event_ids() -> list[str]:
    schema = _load_schema(SCHEMAS / "event.schema.json")
    return list(schema["properties"]["type"]["enum"])


def _frame_ids() -> list[str]:
    frames = yaml.safe_load((ROOT / "contract" / "frames.yaml").read_text(encoding="utf-8"))
    return list(frames["frames"])


def test_every_canonical_event_has_payload_schema() -> None:
    for event_type in _event_ids():
        path = SCHEMAS / "events" / f"{event_type}.schema.json"
        assert path.is_file(), event_type
        schema = _load_schema(path)
        assert schema["properties"]["type"]["const"] == event_type
        assert "subsurface" not in schema.get("properties", {})


def test_every_canonical_frame_has_payload_schema() -> None:
    for frame in _frame_ids():
        path = SCHEMAS / "frames" / f"{frame}.schema.json"
        assert path.is_file(), frame
        schema = _load_schema(path)
        assert schema["properties"]["frame"]["const"] == frame
        assert "subsurface" not in schema.get("properties", {})


def test_representative_event_payload_schema_validation() -> None:
    cases = [
        ("http.request", {"type": "http.request", "body": "a", "more_body": True}),
        ("http.response.start", {"type": "http.response.start", "status": 200, "headers": []}),
        ("http.response.pathsend", {"type": "http.response.pathsend", "path": "/tmp/body.bin"}),
        ("websocket.send", {"type": "websocket.send", "text": "ok", "framing": "text"}),
        (
            "webtransport.stream.receive",
            {
                "type": "webtransport.stream.receive",
                "stream_id": 7,
                "stream_direction": "bidi",
                "body": "chunk",
                "more": True,
            },
        ),
        (
            "webtransport.datagram.send",
            {"type": "webtransport.datagram.send", "datagram_id": "dg-1", "bytes": "abc"},
        ),
        (
            "stream.resume.request",
            {
                "type": "stream.resume.request",
                "resume_token": "rt-1",
                "client_id": "client-a",
                "session_id": "session-a",
                "stream_id": "stream-a",
                "binding": "webtransport",
                "requested_offset": 2,
            },
        ),
        (
            "stream.resume.accept",
            {
                "type": "stream.resume.accept",
                "resume_token": "rt-1",
                "client_id": "client-a",
                "session_id": "session-a",
                "stream_id": "stream-a",
                "binding": "webtransport",
                "accepted_offset": 2,
                "replay_count": 1,
            },
        ),
        (
            "stream.resume.reject",
            {
                "type": "stream.resume.reject",
                "resume_token": "rt-1",
                "client_id": "client-a",
                "session_id": "session-a",
                "stream_id": "stream-a",
                "binding": "webtransport",
                "reason": "expired",
            },
        ),
        ("lifespan.startup.failed", {"type": "lifespan.startup.failed", "message": "failed"}),
    ]
    for event_type, payload in cases:
        validator = Draft202012Validator(_load_schema(SCHEMAS / "events" / f"{event_type}.schema.json"))
        validator.validate(payload)


def test_representative_frame_payload_schema_validation() -> None:
    cases = [
        ("http-response-start-frame", {"frame": "http-response-start-frame", "status": 200}),
        ("http-request-body-chunk", {"frame": "http-request-body-chunk", "body": "part", "more": True}),
        ("sse-data-field", {"frame": "sse-data-field", "value": "hello"}),
        ("websocket-send-text", {"frame": "websocket-send-text", "text": "hello"}),
        (
            "webtransport-stream-frame",
            {"frame": "webtransport-stream-frame", "stream_id": 3, "stream_direction": "server_to_client"},
        ),
        ("webtransport-datagram-frame", {"frame": "webtransport-datagram-frame", "datagram_id": 5}),
    ]
    for frame, payload in cases:
        validator = Draft202012Validator(_load_schema(SCHEMAS / "frames" / f"{frame}.schema.json"))
        validator.validate(payload)


def test_payload_schemas_reject_missing_discriminators() -> None:
    invalid_cases = [
        ("events", "webtransport.stream.receive", {"type": "webtransport.stream.receive", "stream_id": 1}),
        ("events", "webtransport.datagram.receive", {"type": "webtransport.datagram.receive"}),
        ("events", "http.response.pathsend", {"type": "http.response.pathsend", "path": ""}),
        ("frames", "webtransport-stream-frame", {"frame": "webtransport-stream-frame", "stream_id": 1}),
        ("frames", "webtransport-datagram-frame", {"frame": "webtransport-datagram-frame"}),
    ]
    for directory, name, payload in invalid_cases:
        validator = Draft202012Validator(_load_schema(SCHEMAS / directory / f"{name}.schema.json"))
        assert not validator.is_valid(payload), name


def test_payload_schemas_reject_subsurface_field() -> None:
    validator = Draft202012Validator(_load_schema(SCHEMAS / "events" / "http.request.schema.json"))
    assert not validator.is_valid({"type": "http.request", "subsurface": "http.rest.request.receive"})

    validator = Draft202012Validator(_load_schema(SCHEMAS / "frames" / "bytes.schema.json"))
    assert not validator.is_valid({"frame": "bytes", "subsurface": "bytes"})
