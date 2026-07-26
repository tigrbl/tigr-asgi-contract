from __future__ import annotations

import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

from tigr_asgi_contract import (
    event_payload_schema_errors,
    frame_payload_schema_errors,
    validate_event_payload_schema_strict,
    validate_frame_payload_schema_strict,
)


ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "contract" / "schemas"


def _event_ids() -> list[str]:
    schema = json.loads((SCHEMAS / "event.schema.json").read_text(encoding="utf-8"))
    return list(schema["properties"]["type"]["enum"])


def _frame_ids() -> list[str]:
    frames = yaml.safe_load((ROOT / "contract" / "frames.yaml").read_text(encoding="utf-8"))
    return list(frames["frames"])


def _schema_validator(kind: str, name: str) -> Draft202012Validator:
    schema = json.loads((SCHEMAS / kind / f"{name}.schema.json").read_text(encoding="utf-8"))
    return Draft202012Validator(schema)


def test_unknown_event_and_frame_id_fail_closed() -> None:
    assert event_payload_schema_errors("unknown.event", {"type": "unknown.event"}) == ["unknown_event_type"]
    assert frame_payload_schema_errors("unknown-frame", {"frame": "unknown-frame"}) == ["unknown_frame"]


def test_mismatched_event_and_frame_discriminators_fail_closed() -> None:
    errors = event_payload_schema_errors("http.request", {"type": "http.response.body"})
    assert "event_type_mismatch" in errors

    errors = frame_payload_schema_errors("bytes", {"frame": "json"})
    assert "frame_mismatch" in errors


def test_subsurface_is_rejected_by_every_event_and_frame_runtime_validator() -> None:
    for event_type in _event_ids():
        assert not validate_event_payload_schema_strict(
            event_type,
            {"type": event_type, "subsurface": "not-a-canonical-asgi-field"},
        )

    for frame in _frame_ids():
        assert not validate_frame_payload_schema_strict(
            frame,
            {"frame": frame, "subsurface": "not-a-canonical-frame-field"},
        )


def test_subsurface_is_rejected_by_every_event_and_frame_json_schema() -> None:
    for event_type in _event_ids():
        assert not _schema_validator("events", event_type).is_valid(
            {"type": event_type, "subsurface": "not-a-canonical-asgi-field"}
        )

    for frame in _frame_ids():
        assert not _schema_validator("frames", frame).is_valid(
            {"frame": frame, "subsurface": "not-a-canonical-frame-field"}
        )


def test_stream_events_reject_missing_invalid_or_cross_lane_discriminators() -> None:
    missing = event_payload_schema_errors(
        "webtransport.stream.receive",
        {"type": "webtransport.stream.receive", "stream_direction": "bidi"},
    )
    assert "stream_id_required" in missing

    invalid_direction = event_payload_schema_errors(
        "webtransport.stream.receive",
        {"type": "webtransport.stream.receive", "stream_id": 1, "stream_direction": "sideways"},
    )
    assert "stream_direction_required" in invalid_direction

    receive_wrong_way = event_payload_schema_errors(
        "webtransport.stream.receive",
        {
            "type": "webtransport.stream.receive",
            "stream_id": 1,
            "stream_direction": "server_to_client",
        },
    )
    assert "stream_direction_not_allowed_for_event" in receive_wrong_way

    send_wrong_way = event_payload_schema_errors(
        "webtransport.stream.send",
        {
            "type": "webtransport.stream.send",
            "stream_id": 1,
            "stream_direction": "client_to_server",
        },
    )
    assert "stream_direction_not_allowed_for_event" in send_wrong_way

    cross_lane = event_payload_schema_errors(
        "webtransport.stream.send",
        {
            "type": "webtransport.stream.send",
            "stream_id": 1,
            "stream_direction": "server_to_client",
            "datagram_id": 3,
        },
    )
    assert "datagram_field_not_allowed_on_stream_event" in cross_lane


def test_datagram_events_reject_missing_or_cross_lane_discriminators() -> None:
    missing = event_payload_schema_errors(
        "webtransport.datagram.receive",
        {"type": "webtransport.datagram.receive"},
    )
    assert "datagram_id_required" in missing

    cross_lane = event_payload_schema_errors(
        "webtransport.datagram.send",
        {"type": "webtransport.datagram.send", "datagram_id": 2, "stream_id": 1},
    )
    assert "stream_field_not_allowed_on_datagram_event" in cross_lane


def test_stream_and_datagram_frames_reject_cross_lane_discriminators() -> None:
    stream_errors = frame_payload_schema_errors(
        "webtransport-stream-frame",
        {"frame": "webtransport-stream-frame", "stream_id": 1, "stream_direction": "bidi", "datagram_id": 7},
    )
    assert "datagram_field_not_allowed_on_stream_frame" in stream_errors

    datagram_errors = frame_payload_schema_errors(
        "webtransport-datagram-frame",
        {"frame": "webtransport-datagram-frame", "datagram_id": 7, "stream_id": 1},
    )
    assert "stream_field_not_allowed_on_datagram_frame" in datagram_errors


def test_webtransport_datagram_rejects_jsonrpc_and_ndjson_framing() -> None:
    jsonrpc_errors = event_payload_schema_errors(
        "webtransport.datagram.receive",
        {"type": "webtransport.datagram.receive", "datagram_id": 1, "framing": "jsonrpc", "jsonrpc_complete": True},
    )
    assert "framing_not_allowed_for_event" in jsonrpc_errors

    ndjson_errors = event_payload_schema_errors(
        "webtransport.datagram.send",
        {"type": "webtransport.datagram.send", "datagram_id": 1, "framing": "ndjson"},
    )
    assert "framing_not_allowed_for_event" in ndjson_errors


def test_jsonrpc_and_ndjson_boundary_rules_fail_closed() -> None:
    incomplete_jsonrpc = event_payload_schema_errors(
        "websocket.receive",
        {"type": "websocket.receive", "framing": "jsonrpc"},
    )
    assert "jsonrpc_requires_complete_document" in incomplete_jsonrpc

    ambiguous_ndjson = event_payload_schema_errors(
        "websocket.receive",
        {"type": "websocket.receive", "framing": "ndjson", "jsonrpc_complete": True},
    )
    assert "ndjson_must_not_assert_jsonrpc_complete" in ambiguous_ndjson


def test_unknown_framing_fails_closed() -> None:
    errors = event_payload_schema_errors(
        "websocket.send",
        {"type": "websocket.send", "framing": "cbor"},
    )
    assert "unknown_framing" in errors


def test_json_schema_and_runtime_agree_on_representative_negative_cases() -> None:
    cases = [
        ("events", "webtransport.stream.receive", {"type": "webtransport.stream.receive", "stream_id": 1}),
        ("events", "webtransport.datagram.receive", {"type": "webtransport.datagram.receive"}),
        ("frames", "webtransport-stream-frame", {"frame": "webtransport-stream-frame", "stream_id": 1}),
        ("frames", "webtransport-datagram-frame", {"frame": "webtransport-datagram-frame"}),
    ]
    for kind, name, payload in cases:
        assert not _schema_validator(kind, name).is_valid(payload), name
        if kind == "events":
            assert not validate_event_payload_schema_strict(name, payload)
        else:
            assert not validate_frame_payload_schema_strict(name, payload)
