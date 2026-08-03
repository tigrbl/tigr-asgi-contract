from __future__ import annotations

from tigr_asgi_contract import (
    protocol_binding,
    validate_automata_sequence,
    validate_event_payload,
)


def test_generated_protocol_binding_lookup() -> None:
    assert protocol_binding("http.rest") == "rest"
    assert protocol_binding("asgi.pathsend") == "http.stream"


def test_generated_automata_accept_valid_sequences() -> None:
    assert validate_automata_sequence(
        "request",
        [
            "request.open",
            "request.close",
            "request.dispatch",
            "response.open",
            "response.body_out",
            "response.emit_complete",
            "response.finalize",
        ],
    )
    assert validate_automata_sequence(
        "stream",
        ["stream.open", "stream.chunk_out", "stream.finalize", "stream.emit_complete"],
    )


def test_generated_automata_reject_invalid_sequences() -> None:
    assert not validate_automata_sequence("request", ["response.body_out"])
    assert not validate_automata_sequence("stream", ["stream.chunk_out", "stream.close"])


def test_generated_automata_accept_standard_lifecycle_outcomes() -> None:
    assert validate_automata_sequence("session", ["session.open", "session.reject"])
    assert validate_automata_sequence("session", ["session.open", "session.disconnect"])
    assert validate_automata_sequence(
        "message",
        ["message.in", "message.decode_failed"],
    )
    assert validate_automata_sequence(
        "message",
        ["message.in", "message.decode", "message.handle_failed"],
    )
    assert validate_automata_sequence(
        "message",
        ["message.in", "message.decode", "message.handle", "message.out", "message.emit_failed"],
    )
    assert validate_automata_sequence("stream", ["stream.open", "stream.reset"])
    assert validate_automata_sequence("stream", ["stream.open", "stream.stop_sending"])
    assert validate_automata_sequence("datagram", ["datagram.in", "datagram.handle", "datagram.out", "datagram.emit_failed"])
    assert validate_automata_sequence("lifespan", ["lifespan.startup", "lifespan.startup_complete"])
    assert validate_automata_sequence("lifespan", ["lifespan.startup", "lifespan.startup_failed"])
    assert validate_automata_sequence("lifespan", ["lifespan.shutdown", "lifespan.shutdown_complete"])


def test_generated_event_payload_validator() -> None:
    assert validate_event_payload("http.response.pathsend", {"path": "/tmp/file.bin"})
    assert not validate_event_payload("http.response.pathsend", {})
    assert validate_event_payload(
        "webtransport.stream.receive",
        {"stream_id": 7, "stream_direction": "bidi", "more": True},
    )
    assert not validate_event_payload("webtransport.stream.receive", {})
    assert validate_event_payload("webtransport.datagram.send", {"datagram_id": 9})
    assert not validate_event_payload("webtransport.datagram.send", {})
