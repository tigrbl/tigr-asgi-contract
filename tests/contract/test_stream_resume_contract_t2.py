from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from tigr_asgi_contract import validate_semantic_sequence


ROOT = Path(__file__).resolve().parents[2]
EVENT_SCHEMAS = ROOT / "contract" / "schemas" / "events"


def _validator(event_type: str) -> Draft202012Validator:
    schema = json.loads((EVENT_SCHEMAS / f"{event_type}.schema.json").read_text(encoding="utf-8"))
    return Draft202012Validator(schema)


def test_stream_resume_t2_rejects_malformed_request_payloads() -> None:
    validator = _validator("stream.resume.request")

    invalid_payloads = [
        {
            "type": "stream.resume.request",
            "client_id": "client-a",
            "session_id": "session-a",
            "stream_id": "stream-a",
            "binding": "webtransport",
        },
        {
            "type": "stream.resume.request",
            "resume_token": "rt-a",
            "client_id": "client-a",
            "session_id": "session-a",
            "stream_id": "stream-a",
            "binding": "webtransport",
            "requested_offset": -1,
        },
        {
            "type": "stream.resume.request",
            "resume_token": "rt-a",
            "client_id": "client-a",
            "session_id": "session-a",
            "stream_id": "stream-a",
            "binding": "http.rest",
        },
    ]

    for payload in invalid_payloads:
        assert not validator.is_valid(payload)


def test_stream_resume_t2_rejects_malformed_accept_and_reject_payloads() -> None:
    assert not _validator("stream.resume.accept").is_valid(
        {
            "type": "stream.resume.accept",
            "resume_token": "rt-a",
            "client_id": "client-a",
            "session_id": "session-a",
            "stream_id": "stream-a",
            "binding": "webtransport",
        }
    )
    assert not _validator("stream.resume.reject").is_valid(
        {
            "type": "stream.resume.reject",
            "resume_token": "rt-a",
            "client_id": "client-a",
            "session_id": "session-a",
            "stream_id": "stream-a",
            "binding": "webtransport",
            "reason": "retry_later",
        }
    )
    assert not _validator("stream.resume.reject").is_valid(
        {
            "type": "stream.resume.reject",
            "resume_token": "rt-a",
            "client_id": "client-a",
            "session_id": "session-a",
            "stream_id": "stream-a",
            "binding": "webtransport",
            "reason": "expired",
            "subsurface": "stream.resume.reject.internal",
        }
    )


def test_stream_resume_t2_rejects_illegal_fsm_orderings() -> None:
    assert not validate_semantic_sequence(
        "stream_resume",
        ["stream_resume.requested", "stream_resume.completed"],
    )
    assert not validate_semantic_sequence(
        "stream_resume",
        ["stream_resume.requested", "stream_resume.accepted", "stream_resume.rejected"],
    )
