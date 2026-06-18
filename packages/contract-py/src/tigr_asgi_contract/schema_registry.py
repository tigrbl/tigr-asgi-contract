from __future__ import annotations

from typing import Any

from .registry import FRAMES


CONTRACT_ARTIFACT_SCHEMA_PATHS: dict[str, str] = {
    "bindings.yaml": "contract/schemas/bindings.schema.json",
    "capabilities.yaml": "contract/schemas/capabilities.schema.json",
    "exchanges.yaml": "contract/schemas/exchanges.schema.json",
    "families.yaml": "contract/schemas/families.schema.json",
    "ids.yaml": "contract/schemas/ids.schema.json",
    "manifest.json": "contract/schemas/manifest.schema.json",
    "scope_types.yaml": "contract/schemas/scope_types.schema.json",
    "subevents.yaml": "contract/schemas/subevents.schema.json",
    "surfaces.yaml": "contract/schemas/surfaces.schema.json",
}

EVENT_PAYLOAD_SCHEMA_PATHS: dict[str, str] = {
    "http.disconnect": "contract/schemas/events/http.disconnect.schema.json",
    "http.request": "contract/schemas/events/http.request.schema.json",
    "http.response.body": "contract/schemas/events/http.response.body.schema.json",
    "http.response.pathsend": "contract/schemas/events/http.response.pathsend.schema.json",
    "http.response.start": "contract/schemas/events/http.response.start.schema.json",
    "lifespan.shutdown": "contract/schemas/events/lifespan.shutdown.schema.json",
    "lifespan.shutdown.complete": "contract/schemas/events/lifespan.shutdown.complete.schema.json",
    "lifespan.shutdown.failed": "contract/schemas/events/lifespan.shutdown.failed.schema.json",
    "lifespan.startup": "contract/schemas/events/lifespan.startup.schema.json",
    "lifespan.startup.complete": "contract/schemas/events/lifespan.startup.complete.schema.json",
    "lifespan.startup.failed": "contract/schemas/events/lifespan.startup.failed.schema.json",
    "stream.resume.accept": "contract/schemas/events/stream.resume.accept.schema.json",
    "stream.resume.reject": "contract/schemas/events/stream.resume.reject.schema.json",
    "stream.resume.request": "contract/schemas/events/stream.resume.request.schema.json",
    "transport.emit.complete": "contract/schemas/events/transport.emit.complete.schema.json",
    "transport.emit.failed": "contract/schemas/events/transport.emit.failed.schema.json",
    "websocket.accept": "contract/schemas/events/websocket.accept.schema.json",
    "websocket.close": "contract/schemas/events/websocket.close.schema.json",
    "websocket.connect": "contract/schemas/events/websocket.connect.schema.json",
    "websocket.disconnect": "contract/schemas/events/websocket.disconnect.schema.json",
    "websocket.receive": "contract/schemas/events/websocket.receive.schema.json",
    "websocket.send": "contract/schemas/events/websocket.send.schema.json",
    "webtransport.accept": "contract/schemas/events/webtransport.accept.schema.json",
    "webtransport.close": "contract/schemas/events/webtransport.close.schema.json",
    "webtransport.connect": "contract/schemas/events/webtransport.connect.schema.json",
    "webtransport.datagram.receive": "contract/schemas/events/webtransport.datagram.receive.schema.json",
    "webtransport.datagram.send": "contract/schemas/events/webtransport.datagram.send.schema.json",
    "webtransport.disconnect": "contract/schemas/events/webtransport.disconnect.schema.json",
    "webtransport.stream.close": "contract/schemas/events/webtransport.stream.close.schema.json",
    "webtransport.stream.receive": "contract/schemas/events/webtransport.stream.receive.schema.json",
    "webtransport.stream.reset": "contract/schemas/events/webtransport.stream.reset.schema.json",
    "webtransport.stream.send": "contract/schemas/events/webtransport.stream.send.schema.json",
    "webtransport.stream.stop_sending": "contract/schemas/events/webtransport.stream.stop_sending.schema.json",
}

FRAME_PAYLOAD_SCHEMA_PATHS: dict[str, str] = {
    frame: f"contract/schemas/frames/{frame}.schema.json" for frame in FRAMES
}

EVENT_SCHEMA_IDS = frozenset(EVENT_PAYLOAD_SCHEMA_PATHS)
FRAME_SCHEMA_IDS = frozenset(FRAME_PAYLOAD_SCHEMA_PATHS)

_FRAMINGS = frozenset({"json", "jsonrpc", "ndjson", "sse", "text", "bytes", "binary"})
_STREAM_DIRECTIONS = frozenset({"bidi", "client_to_server", "server_to_client"})
_EVENTS_REQUIRING_JSONRPC_COMPLETION = frozenset(
    {
        "http.request",
        "http.response.body",
        "websocket.receive",
        "websocket.send",
        "webtransport.stream.receive",
        "webtransport.stream.send",
    }
)
_EVENT_FRAMING_ALLOWLISTS = {
    "websocket.receive": frozenset({"text", "bytes", "binary", "json", "jsonrpc", "ndjson"}),
    "websocket.send": frozenset({"text", "bytes", "binary", "json", "jsonrpc", "ndjson"}),
    "webtransport.stream.receive": frozenset({"bytes", "binary", "text", "json", "jsonrpc", "ndjson"}),
    "webtransport.stream.send": frozenset({"bytes", "binary", "text", "json", "jsonrpc", "ndjson"}),
    "webtransport.datagram.receive": frozenset({"bytes", "binary", "text", "json"}),
    "webtransport.datagram.send": frozenset({"bytes", "binary", "text", "json"}),
}


def event_payload_schema_path(event_type: str) -> str:
    try:
        return EVENT_PAYLOAD_SCHEMA_PATHS[event_type]
    except KeyError as exc:
        raise KeyError(f"unknown event payload schema: {event_type}") from exc


def contract_artifact_schema_path(artifact_path: str) -> str:
    try:
        return CONTRACT_ARTIFACT_SCHEMA_PATHS[artifact_path]
    except KeyError as exc:
        raise KeyError(f"unknown contract artifact schema: {artifact_path}") from exc


def frame_payload_schema_path(frame: str) -> str:
    try:
        return FRAME_PAYLOAD_SCHEMA_PATHS[frame]
    except KeyError as exc:
        raise KeyError(f"unknown frame payload schema: {frame}") from exc


def event_has_payload_schema(event_type: str) -> bool:
    return event_type in EVENT_PAYLOAD_SCHEMA_PATHS


def contract_artifact_has_schema(artifact_path: str) -> bool:
    return artifact_path in CONTRACT_ARTIFACT_SCHEMA_PATHS


def frame_has_payload_schema(frame: str) -> bool:
    return frame in FRAME_PAYLOAD_SCHEMA_PATHS


def event_payload_schema_path_for_payload(event: dict[str, Any]) -> str:
    if not isinstance(event, dict):
        raise TypeError("event payload must be an object")
    event_type = event.get("type")
    if not isinstance(event_type, str):
        raise KeyError("event payload is missing string type discriminator")
    return event_payload_schema_path(event_type)


def frame_payload_schema_path_for_payload(payload: dict[str, Any]) -> str:
    if not isinstance(payload, dict):
        raise TypeError("frame payload must be an object")
    frame = payload.get("frame")
    if not isinstance(frame, str):
        raise KeyError("frame payload is missing string frame discriminator")
    return frame_payload_schema_path(frame)


def validate_event_payload_discriminator(event: dict[str, Any]) -> bool:
    try:
        event_type = event.get("type") if isinstance(event, dict) else None
        if not isinstance(event_type, str):
            return False
        event_payload_schema_path(event_type)
    except KeyError:
        return False
    return not event_payload_schema_errors(event_type, event)


def validate_frame_payload_discriminator(payload: dict[str, Any]) -> bool:
    try:
        frame = payload.get("frame") if isinstance(payload, dict) else None
        if not isinstance(frame, str):
            return False
        frame_payload_schema_path(frame)
    except KeyError:
        return False
    return not frame_payload_schema_errors(frame, payload)


def _is_present_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value)


def _has_unit_id(value: Any) -> bool:
    return isinstance(value, int) or _is_present_string(value)


def event_payload_schema_errors(event_type: str, event: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if event_type not in EVENT_PAYLOAD_SCHEMA_PATHS:
        errors.append("unknown_event_type")
        return errors
    if not isinstance(event, dict):
        errors.append("payload_not_object")
        return errors
    actual_type = event.get("type")
    if actual_type != event_type:
        errors.append("event_type_mismatch")
    if "subsurface" in event:
        errors.append("subsurface_not_allowed")
    if event_type.startswith("webtransport.message") or actual_type == "webtransport.message":
        errors.append("webtransport_message_not_native")
    framing = event.get("framing")
    if framing is not None and framing not in _FRAMINGS:
        errors.append("unknown_framing")
    allowed_framings = _EVENT_FRAMING_ALLOWLISTS.get(event_type)
    if framing is not None and allowed_framings is not None and framing not in allowed_framings:
        errors.append("framing_not_allowed_for_event")
    if framing == "jsonrpc" and event_type in _EVENTS_REQUIRING_JSONRPC_COMPLETION and not event.get("jsonrpc_complete", False):
        errors.append("jsonrpc_requires_complete_document")
    if framing == "ndjson" and event.get("jsonrpc_complete", False):
        errors.append("ndjson_must_not_assert_jsonrpc_complete")
    if event_type == "http.response.start" and not isinstance(event.get("status"), int):
        errors.append("status_required")
    if event_type == "http.response.pathsend" and not _is_present_string(event.get("path")):
        errors.append("path_required")
    if event_type.endswith(".failed") or event_type == "transport.emit.failed":
        if not _is_present_string(event.get("message")):
            errors.append("message_required")
    if ".stream." in event_type:
        if not _has_unit_id(event.get("stream_id")):
            errors.append("stream_id_required")
        if event_type in {"webtransport.stream.receive", "webtransport.stream.send"}:
            if event.get("stream_direction") not in _STREAM_DIRECTIONS:
                errors.append("stream_direction_required")
        if "datagram_id" in event:
            errors.append("datagram_field_not_allowed_on_stream_event")
    elif "stream_id" in event or "stream_direction" in event:
        errors.append("stream_field_not_allowed_on_non_stream_event")
    if ".datagram." in event_type:
        if not _has_unit_id(event.get("datagram_id")):
            errors.append("datagram_id_required")
        if "stream_id" in event or "stream_direction" in event:
            errors.append("stream_field_not_allowed_on_datagram_event")
    elif "datagram_id" in event:
        errors.append("datagram_field_not_allowed_on_non_datagram_event")
    return errors


def validate_event_payload_schema(event_type: str, event: dict[str, Any]) -> bool:
    return not event_payload_schema_errors(event_type, event)


def validate_event_payload_schema_strict(event_type: str, event: dict[str, Any]) -> bool:
    return validate_event_payload_schema(event_type, event)


def frame_payload_schema_errors(frame: str, payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if frame not in FRAME_PAYLOAD_SCHEMA_PATHS:
        errors.append("unknown_frame")
        return errors
    if not isinstance(payload, dict):
        errors.append("payload_not_object")
        return errors
    if payload.get("frame") != frame:
        errors.append("frame_mismatch")
    if "subsurface" in payload:
        errors.append("subsurface_not_allowed")
    if frame == "http-response-start-frame" and not isinstance(payload.get("status"), int):
        errors.append("status_required")
    if frame == "asgi-pathsend-extension" and not _is_present_string(payload.get("path")):
        errors.append("path_required")
    if frame in {"websocket-receive-text", "websocket-send-text"}:
        if not _is_present_string(payload.get("text")):
            errors.append("text_required")
    if frame in {"websocket-receive-bytes", "websocket-send-bytes"}:
        if "bytes" not in payload:
            errors.append("bytes_required")
    if frame == "webtransport-stream-frame":
        if not _has_unit_id(payload.get("stream_id")):
            errors.append("stream_id_required")
        if payload.get("stream_direction") not in _STREAM_DIRECTIONS:
            errors.append("stream_direction_required")
        if "datagram_id" in payload:
            errors.append("datagram_field_not_allowed_on_stream_frame")
    elif "stream_id" in payload or "stream_direction" in payload:
        errors.append("stream_field_not_allowed_on_non_stream_frame")
    if frame == "webtransport-datagram-frame":
        if not _has_unit_id(payload.get("datagram_id")):
            errors.append("datagram_id_required")
        if "stream_id" in payload or "stream_direction" in payload:
            errors.append("stream_field_not_allowed_on_datagram_frame")
    elif "datagram_id" in payload:
        errors.append("datagram_field_not_allowed_on_non_datagram_frame")
    if frame.startswith("sse-") and frame.endswith("-field"):
        if "value" not in payload:
            errors.append("value_required")
    return errors


def validate_frame_payload_schema(frame: str, payload: dict[str, Any]) -> bool:
    return not frame_payload_schema_errors(frame, payload)


def validate_frame_payload_schema_strict(frame: str, payload: dict[str, Any]) -> bool:
    return validate_frame_payload_schema(frame, payload)
