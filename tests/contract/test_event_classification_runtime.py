from __future__ import annotations

import pytest

from tigr_asgi_contract import (
    Framing,
    classify_event,
    validate_event_classification,
    validate_event_payload,
    validate_framing_for_classification,
)


def scope(scope_type: str, binding: str, *, framing: str | None = None, wt: dict | None = None) -> dict:
    return {
        "type": scope_type,
        "ext": {
            "transport": {
                "binding": binding,
                "network": "quic" if scope_type == "webtransport" else "tcp",
                "secure": binding in {"websocket", "webtransport"},
                "alpn": "h3" if scope_type == "webtransport" else "http/1.1",
                "framing": framing,
            },
            "family_capabilities": {},
            "webtransport": wt,
        },
    }


@pytest.mark.parametrize(
    ("case_scope", "channel", "event_type", "payload", "family", "exchange", "framing"),
    [
        (scope("http", "rest"), "receive", "http.request", {"framing": "json"}, "request", "unary", "json"),
        (scope("http", "jsonrpc"), "send", "http.response.body", {"framing": "jsonrpc", "jsonrpc_complete": True}, "request", "unary", "jsonrpc"),
        (scope("http", "http.stream"), "receive", "http.request", {"framing": "ndjson"}, "stream", "client_stream", "ndjson"),
        (scope("http", "sse"), "send", "http.response.body", {"framing": "sse"}, "stream", "server_stream", "sse"),
        (scope("websocket", "websocket"), "receive", "websocket.receive", {"framing": "jsonrpc", "jsonrpc_complete": True}, "message", "duplex", "jsonrpc"),
        (
            scope("webtransport", "webtransport", wt={"supports_bidi_streams": True, "supports_uni_streams": True, "supports_datagrams": True}),
            "receive",
            "webtransport.connect",
            {},
            "session",
            "unary",
            None,
        ),
        (
            scope("webtransport", "webtransport", wt={"supports_bidi_streams": True, "supports_uni_streams": True, "supports_datagrams": True}),
            "receive",
            "webtransport.stream.receive",
            {"stream_id": 1, "stream_direction": "bidi", "framing": "jsonrpc", "jsonrpc_complete": True, "more": True},
            "stream",
            "duplex",
            "jsonrpc",
        ),
        (
            scope("webtransport", "webtransport", wt={"supports_bidi_streams": True, "supports_uni_streams": True, "supports_datagrams": True}),
            "receive",
            "webtransport.stream.receive",
            {"stream_id": 2, "stream_direction": "client_to_server", "framing": "ndjson", "more": True},
            "stream",
            "client_stream",
            "ndjson",
        ),
        (
            scope("webtransport", "webtransport", wt={"supports_bidi_streams": True, "supports_uni_streams": True, "supports_datagrams": True}),
            "send",
            "webtransport.stream.send",
            {"stream_id": 3, "stream_direction": "server_to_client", "framing": "text", "more": True},
            "stream",
            "server_stream",
            "text",
        ),
        (
            scope("webtransport", "webtransport", wt={"supports_bidi_streams": True, "supports_uni_streams": True, "supports_datagrams": True}),
            "send",
            "webtransport.datagram.send",
            {"datagram_id": 4, "framing": "binary"},
            "datagram",
            "duplex",
            "binary",
        ),
    ],
)
def test_representative_classifications_accept_payloads(
    case_scope: dict,
    channel: str,
    event_type: str,
    payload: dict,
    family: str,
    exchange: str,
    framing: str | None,
) -> None:
    classification = classify_event(case_scope, channel, event_type, payload)

    assert classification.family == family
    assert classification.exchange == exchange
    assert validate_event_classification(case_scope, channel, event_type, payload) is True
    assert validate_event_payload(event_type, payload, classification) is True
    assert validate_framing_for_classification(framing, classification) is True


def test_event_channel_mismatch_is_rejected() -> None:
    assert validate_event_classification(scope("http", "rest"), "send", "http.request") is False


def test_unknown_framing_is_rejected() -> None:
    classification = classify_event(scope("http", "rest"), "receive", "http.request", {"framing": "json"})
    assert validate_framing_for_classification("cbor", classification) is False


def test_jsonrpc_requires_jsonrpc_framing_and_complete_document() -> None:
    classification = classify_event(scope("http", "jsonrpc"), "send", "http.response.body", {"framing": "jsonrpc"})

    assert validate_framing_for_classification(Framing.JSON.value, classification) is False
    assert validate_framing_for_classification(Framing.NDJSON.value, classification) is False
    assert validate_event_payload("http.response.body", {"framing": "jsonrpc"}, classification) is False
    assert validate_event_payload(
        "http.response.body",
        {"framing": "jsonrpc", "jsonrpc_complete": True},
        classification,
    ) is True


def test_stream_payload_discriminators_are_required() -> None:
    wt_scope = scope("webtransport", "webtransport", wt={"supports_bidi_streams": True, "supports_uni_streams": True})
    classification = classify_event(
        wt_scope,
        "receive",
        "webtransport.stream.receive",
        {"stream_id": 1, "stream_direction": "bidi"},
    )

    assert validate_event_payload("webtransport.stream.receive", {"stream_direction": "bidi"}, classification) is False
    assert validate_event_classification(
        wt_scope,
        "receive",
        "webtransport.stream.receive",
        {"stream_id": 1},
    ) is False


def test_datagram_payload_discriminators_and_framings_are_required() -> None:
    wt_scope = scope("webtransport", "webtransport", wt={"supports_datagrams": True})
    classification = classify_event(wt_scope, "send", "webtransport.datagram.send", {"datagram_id": 9})

    assert validate_event_payload("webtransport.datagram.send", {}, classification) is False
    assert validate_framing_for_classification("jsonrpc", classification) is False
    assert validate_framing_for_classification("ndjson", classification) is False
    assert validate_event_payload("webtransport.datagram.send", {"datagram_id": 9, "framing": "jsonrpc"}, classification) is False


def test_webtransport_message_lane_and_subsurface_are_rejected() -> None:
    wt_scope = scope("webtransport", "webtransport", wt={"supports_bidi_streams": True})

    assert validate_event_classification(wt_scope, "receive", "websocket.receive", {}) is False
    classification = classify_event(
        wt_scope,
        "receive",
        "webtransport.stream.receive",
        {"stream_id": 1, "stream_direction": "bidi"},
    )
    assert validate_event_payload(
        "webtransport.stream.receive",
        {"stream_id": 1, "stream_direction": "bidi", "subsurface": "wt.bidi_stream"},
        classification,
    ) is False
