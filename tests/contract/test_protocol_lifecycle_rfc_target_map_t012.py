from __future__ import annotations

import pytest

from tigr_asgi_contract import semantic_domain, validate_semantic_transition


def _projection_rows() -> list[dict[str, str]]:
    return list(semantic_domain("channel_lifecycle")["protocol_projection"])


def test_t0_protocol_lifecycle_rfc_targets_are_declared() -> None:
    targets = semantic_domain("channel_lifecycle")["rfc_targets"]

    assert targets["http2"] == {
        "rfc": "RFC 9113",
        "sections": ["5.1", "5.2", "6.4", "6.8"],
    }
    assert targets["http3"] == {
        "rfc": "RFC 9114",
        "sections": ["4.1", "4.1.1", "5.2", "6.1"],
    }
    assert targets["quic"] == {
        "rfc": "RFC 9000",
        "sections": ["3", "3.5", "10", "19.4", "19.5"],
    }
    assert targets["websocket_http2"]["rfc"] == "RFC 8441"
    assert targets["websocket_http3"]["rfc"] == "RFC 9220"


@pytest.mark.parametrize(
    ("protocol", "term", "event", "state", "direction"),
    [
        ("http2", "half-closed(remote)", "channel.read_closed", "read_closed", "read"),
        ("http2", "half-closed(local)", "channel.write_closed", "write_closed", "write"),
        ("http2", "RST_STREAM", "channel.lost", "lost", "bidirectional"),
        ("http3", "request stream receive closed", "channel.read_closed", "read_closed", "read"),
        ("http3", "request stream send closed", "channel.write_closed", "write_closed", "write"),
        ("quic", "RESET_STREAM", "channel.write_closed", "write_closed", "write"),
        ("quic", "STOP_SENDING", "channel.write_closed", "write_closed", "write"),
        ("quic", "connection close", "channel.closing", "closing", "connection"),
    ],
)
def test_t1_rfc_projection_rows_map_to_legal_contract_transitions(
    protocol: str,
    term: str,
    event: str,
    state: str,
    direction: str,
) -> None:
    row = next(
        item
        for item in _projection_rows()
        if item["protocol"] == protocol and item["term"] == term
    )

    assert row["event"] == event
    assert row["state"] == state
    assert row["direction"] == direction
    assert validate_semantic_transition("channel_lifecycle", "open", event)


def test_t2_projection_map_does_not_define_ambiguous_half_open_state() -> None:
    rows = _projection_rows()

    assert all(row["state"] != "half_open" for row in rows)
    assert all(row["event"].startswith("channel.") for row in rows)
    assert all(row["direction"] in {"read", "write", "bidirectional", "connection"} for row in rows)


def test_t2_bidirectional_and_connection_events_are_not_directional_half_close() -> None:
    rows = _projection_rows()

    for row in rows:
        if row["direction"] in {"bidirectional", "connection"}:
            assert row["state"] in {"closing", "lost", "failed"}
            assert row["event"] not in {"channel.read_closed", "channel.write_closed"}
