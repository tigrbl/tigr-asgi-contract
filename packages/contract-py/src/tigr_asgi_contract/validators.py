from __future__ import annotations
from typing import Any
from .registry import AUTOMATA, BINDING_FAMILY_MATRIX, FAMILY_SUBEVENT_MATRIX, BINDING_SUBEVENT_MATRIX, PROTOCOLS, EVENT_CLASSIFICATIONS, FRAMINGS
from .models import EventClassification

LEGALITY_CODES = frozenset({"R", "O", "D", "F"})
LEGALITY_ALLOWED_CODES = frozenset({"R", "O", "D"})


def _scope_value(scope: Any, key: str, default: Any = None) -> Any:
    if isinstance(scope, dict):
        return scope.get(key, default)
    return getattr(scope, key, default)


def _binding_from_scope(scope: Any) -> str | None:
    ext = _scope_value(scope, "ext", {}) or {}
    transport = ext.get("transport") if isinstance(ext, dict) else getattr(ext, "transport", None)
    if isinstance(transport, dict):
        return transport.get("binding")
    return getattr(transport, "binding", None)


def _webtransport_ext(scope: Any) -> Any:
    ext = _scope_value(scope, "ext", {}) or {}
    return ext.get("webtransport") if isinstance(ext, dict) else getattr(ext, "webtransport", None)


def _has_capability(scope: Any, gate: str) -> bool:
    wt = _webtransport_ext(scope)
    if wt is None:
        return False
    if isinstance(wt, dict):
        return bool(wt.get(gate))
    return bool(getattr(wt, gate, False))


def binding_supports_family(binding: str, family: str) -> bool:
    return binding_family_legality(binding, family) in LEGALITY_ALLOWED_CODES


def family_supports_subevent(family: str, subevent: str) -> bool:
    return family_subevent_legality(family, subevent) in LEGALITY_ALLOWED_CODES


def binding_supports_subevent(binding: str, subevent: str) -> bool:
    return binding_subevent_legality(binding, subevent) in LEGALITY_ALLOWED_CODES


def binding_family_legality(binding: str, family: str) -> str:
    return BINDING_FAMILY_MATRIX.get(binding, {}).get(family, "F")


def family_subevent_legality(family: str, subevent: str) -> str:
    return FAMILY_SUBEVENT_MATRIX.get(family, {}).get(subevent, "F")


def binding_subevent_legality(binding: str, subevent: str) -> str:
    return BINDING_SUBEVENT_MATRIX.get(binding, {}).get(subevent, "F")


def is_required_legality(code: str) -> bool:
    return code == "R"


def is_optional_legality(code: str) -> bool:
    return code == "O"


def is_derived_legality(code: str) -> bool:
    return code == "D"


def is_forbidden_legality(code: str) -> bool:
    return code == "F"


def validate_binding_family(binding: str, family: str) -> bool:
    return binding_supports_family(binding, family)


def validate_family_subevent(family: str, subevent: str) -> bool:
    return family_supports_subevent(family, subevent)


def validate_binding_subevent(binding: str, subevent: str) -> bool:
    return binding_supports_subevent(binding, subevent)


def legality_matrix_errors() -> list[str]:
    errors: list[str] = []
    bindings = set(BINDING_FAMILY_MATRIX)
    families = set(FAMILY_SUBEVENT_MATRIX)
    subevents = {subevent for values in FAMILY_SUBEVENT_MATRIX.values() for subevent in values}

    for binding, family_map in BINDING_FAMILY_MATRIX.items():
        missing = families - set(family_map)
        extra = set(family_map) - families
        errors.extend(f"binding_family_missing:{binding}:{family}" for family in sorted(missing))
        errors.extend(f"binding_family_unknown:{binding}:{family}" for family in sorted(extra))
        errors.extend(
            f"binding_family_bad_code:{binding}:{family}:{code}"
            for family, code in sorted(family_map.items())
            if code not in LEGALITY_CODES
        )

    for family, subevent_map in FAMILY_SUBEVENT_MATRIX.items():
        errors.extend(
            f"family_subevent_bad_code:{family}:{subevent}:{code}"
            for subevent, code in sorted(subevent_map.items())
            if code not in LEGALITY_CODES
        )
    for binding, subevent_map in BINDING_SUBEVENT_MATRIX.items():
        if binding not in bindings:
            errors.append(f"binding_subevent_unknown_binding:{binding}")
        missing = subevents - set(subevent_map)
        extra = set(subevent_map) - subevents
        errors.extend(f"binding_subevent_missing:{binding}:{subevent}" for subevent in sorted(missing))
        errors.extend(f"binding_subevent_unknown:{binding}:{subevent}" for subevent in sorted(extra))
        errors.extend(
            f"binding_subevent_bad_code:{binding}:{subevent}:{code}"
            for subevent, code in sorted(subevent_map.items())
            if code not in LEGALITY_CODES
        )
    return errors


def validate_legality_matrices() -> bool:
    return not legality_matrix_errors()


def protocol_binding(protocol: str) -> str:
    return PROTOCOLS[protocol]["binding"]


def event_classification_candidates(scope: Any, channel: str, event_type: str, payload: dict | None = None) -> list[EventClassification]:
    payload = payload or {}
    scope_type = _scope_value(scope, "type")
    binding = _binding_from_scope(scope)
    rows = []
    for row in EVENT_CLASSIFICATIONS:
        if row["event"] != event_type or row["channel"] != channel:
            continue
        if row["scope_type"] != scope_type:
            continue
        if binding is not None and row["binding"] != binding:
            continue
        if row.get("stream_direction") and payload.get("stream_direction") != row["stream_direction"]:
            continue
        if any(not _has_capability(scope, gate) for gate in row.get("capability_gates", [])):
            continue
        rows.append(EventClassification(**row))
    return rows


def classify_event(scope: Any, channel: str, event_type: str, payload: dict | None = None) -> EventClassification:
    rows = event_classification_candidates(scope, channel, event_type, payload)
    if not rows:
        raise ValueError(f"No event classification for {channel}:{event_type}")
    return rows[0]


def validate_event_classification(scope: Any, channel: str, event_type: str, payload: dict | None = None) -> bool:
    try:
        classify_event(scope, channel, event_type, payload)
    except ValueError:
        return False
    return True


def validate_framing_for_classification(framing: str | None, classification: EventClassification | dict) -> bool:
    if framing is None:
        return True
    if framing not in FRAMINGS:
        return False
    allowed = classification.allowed_framings if isinstance(classification, EventClassification) else classification.get("allowed_framings", [])
    return framing in allowed


def validate_event_payload(event_type: str, payload: dict, classification: EventClassification | dict | None = None) -> bool:
    if not isinstance(payload, dict) or "subsurface" in payload:
        return False
    if event_type == "http.response.pathsend" and not (isinstance(payload.get("path"), str) and payload["path"]):
        return False
    if ".stream." in event_type and "stream_id" not in payload:
        return False
    if ".datagram." in event_type and "datagram_id" not in payload:
        return False
    if classification is not None:
        required = classification.required_payload_fields if isinstance(classification, EventClassification) else classification.get("required_payload_fields", [])
        if any(field not in payload for field in required):
            return False
        framing = payload.get("framing")
        if framing is not None and not validate_framing_for_classification(framing, classification):
            return False
        if framing == "jsonrpc" and not payload.get("jsonrpc_complete", False):
            return False
        if framing == "ndjson" and payload.get("jsonrpc_complete", False):
            return False
    return True


def validate_automata_sequence(family: str, subevents: list[str]) -> bool:
    automaton = AUTOMATA[family]
    state = automaton["initial"]
    transitions = {(row["from"], row["event"]): row["to"] for row in automaton["transitions"]}
    for subevent in subevents:
        next_state = transitions.get((state, subevent))
        if next_state is None:
            return False
        state = next_state
    return state in set(automaton["terminal"]) or bool(subevents)
