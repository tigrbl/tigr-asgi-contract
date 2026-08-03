from __future__ import annotations

from tigr_asgi_contract.schema_registry import validate_event_payload_schema


def _event(event_type: str, *, more: bool) -> dict[str, object]:
    return {
        "type": event_type,
        "stream_id": 4,
        "stream_direction": "bidi",
        "body": "record",
        "more": more,
        "jsonrpc_complete": True,
    }


def test_complete_record_can_keep_webtransport_stream_open() -> None:
    assert validate_event_payload_schema(
        "webtransport.stream.receive",
        _event("webtransport.stream.receive", more=True),
    )
    assert validate_event_payload_schema(
        "webtransport.stream.send",
        _event("webtransport.stream.send", more=True),
    )


def test_explicit_false_is_a_valid_terminal_stream_event() -> None:
    assert validate_event_payload_schema(
        "webtransport.stream.send",
        _event("webtransport.stream.send", more=False),
    )


def test_stream_continuation_cannot_be_omitted() -> None:
    payload = _event("webtransport.stream.send", more=True)
    payload.pop("more")
    assert not validate_event_payload_schema("webtransport.stream.send", payload)


def test_record_completion_does_not_supply_stream_continuation() -> None:
    payload = _event("webtransport.stream.receive", more=True)
    payload.pop("more")
    assert payload["jsonrpc_complete"] is True
    assert not validate_event_payload_schema("webtransport.stream.receive", payload)
