from __future__ import annotations
from typing import Any
from .registry import AUTOMATA, BINDING_FAMILY_MATRIX, FAMILY_SUBEVENT_MATRIX, BINDING_SUBEVENT_MATRIX, PROTOCOLS, EVENT_CLASSIFICATIONS, FRAMINGS, SEMANTIC_DOMAINS
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


def semantic_domain(domain: str) -> dict[str, Any]:
    return SEMANTIC_DOMAINS[domain]


def semantic_states(domain: str) -> tuple[str, ...]:
    return tuple(SEMANTIC_DOMAINS[domain]["states"])


def semantic_events(domain: str) -> tuple[str, ...]:
    return tuple(row["event"] for row in SEMANTIC_DOMAINS[domain]["transitions"])


def semantic_capabilities(domain: str) -> tuple[str, ...]:
    return tuple(SEMANTIC_DOMAINS[domain].get("capabilities", ()))


def semantic_transition_target(domain: str, state: str, event: str) -> str:
    for row in SEMANTIC_DOMAINS[domain]["transitions"]:
        if row["from"] == state and row["event"] == event:
            return row["to"]
    raise ValueError(f"illegal semantic transition for {domain}: {state} + {event}")


def validate_semantic_transition(domain: str, state: str, event: str) -> bool:
    try:
        semantic_transition_target(domain, state, event)
    except (KeyError, ValueError):
        return False
    return True


def validate_semantic_sequence(domain: str, events: list[str]) -> bool:
    spec = SEMANTIC_DOMAINS[domain]
    state = spec["initial"]
    for event in events:
        try:
            state = semantic_transition_target(domain, state, event)
        except ValueError:
            return False
    terminals = set(spec.get("terminal", ()))
    return not terminals or state in terminals or bool(events)


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

UNSUPPORTED_FEATURE_CATEGORIES = frozenset(
    {
        "binding-family",
        "binding-subevent",
        "family-subevent",
        "scope-subevent",
        "target",
        "contract",
        "debt",
    }
)
UNSUPPORTED_SCOPE_SUBEVENT_TOKENS = frozenset(
    {
        "request-accept",
        "response-close",
        "message-ack",
        "message-nack",
        "stream-abort",
        "datagram-ack",
        "datagram-close",
    }
)


def unsupported_feature_category(feature_id: str) -> str | None:
    if feature_id.startswith("feat:binding-family-"):
        return "binding-family"
    if feature_id.startswith("feat:binding-subevent-"):
        return "binding-subevent"
    if feature_id.startswith("feat:family-subevent-"):
        return "family-subevent"
    if feature_id.startswith("feat:scope-scope-"):
        return "scope-subevent"
    if feature_id.startswith("feat:target-"):
        return "target"
    if feature_id.startswith("feat:contract-"):
        return "contract"
    if feature_id.startswith("feat:debt-"):
        return "debt"
    return None


def _unslug(value: str) -> str:
    return value.replace("-", ".")


def _binding_family_from_feature_id(feature_id: str) -> tuple[str, str] | None:
    prefix = "feat:binding-family-"
    if not feature_id.startswith(prefix):
        return None
    suffix = feature_id.removeprefix(prefix)
    for binding in sorted(BINDING_FAMILY_MATRIX, key=len, reverse=True):
        binding_slug = binding.replace(".", "-")
        marker = f"{binding_slug}-"
        if suffix.startswith(marker):
            family = suffix.removeprefix(marker).replace("-", "_")
            return binding, family
    return None


def _binding_subevent_from_feature_id(feature_id: str) -> tuple[str, str] | None:
    prefix = "feat:binding-subevent-"
    if not feature_id.startswith(prefix):
        return None
    suffix = feature_id.removeprefix(prefix)
    for binding in sorted(BINDING_SUBEVENT_MATRIX, key=len, reverse=True):
        binding_slug = binding.replace(".", "-")
        marker = f"{binding_slug}-"
        if suffix.startswith(marker):
            return binding, _unslug(suffix.removeprefix(marker))
    return None


def _family_subevent_from_feature_id(feature_id: str) -> tuple[str, str] | None:
    prefix = "feat:family-subevent-"
    if not feature_id.startswith(prefix):
        return None
    suffix = feature_id.removeprefix(prefix)
    for family in sorted(FAMILY_SUBEVENT_MATRIX, key=len, reverse=True):
        marker = f"{family.replace('_', '-')}-"
        if suffix.startswith(marker):
            return family, _unslug(suffix.removeprefix(marker))
    return None


def validate_unsupported_feature_runtime(feature_id: str) -> bool:
    category = unsupported_feature_category(feature_id)
    if category is None:
        return False
    if category == "binding-family":
        parsed = _binding_family_from_feature_id(feature_id)
        return parsed is not None and binding_family_legality(*parsed) == "F" and not validate_binding_family(*parsed)
    if category == "binding-subevent":
        parsed = _binding_subevent_from_feature_id(feature_id)
        return parsed is not None and binding_subevent_legality(*parsed) == "F" and not validate_binding_subevent(*parsed)
    if category == "family-subevent":
        parsed = _family_subevent_from_feature_id(feature_id)
        return parsed is not None and family_subevent_legality(*parsed) == "F" and not validate_family_subevent(*parsed)
    if category == "scope-subevent":
        return (
            "-webtransport-message-" in feature_id
            or any(token in feature_id for token in UNSUPPORTED_SCOPE_SUBEVENT_TOKENS)
        )
    return category in {"target", "contract", "debt"}


def unsupported_feature_declaration_errors(feature: dict[str, Any], supported_surface_ids: set[str] | None = None) -> list[str]:
    errors: list[str] = []
    feature_id = str(feature.get("id", ""))
    lifecycle = feature.get("lifecycle", {}) if isinstance(feature.get("lifecycle"), dict) else {}
    plan = feature.get("plan", {}) if isinstance(feature.get("plan"), dict) else {}
    supported_surface_ids = supported_surface_ids or set()

    if unsupported_feature_category(feature_id) not in UNSUPPORTED_FEATURE_CATEGORIES:
        errors.append(f"unknown_unsupported_feature_category:{feature_id}")
    if feature.get("implementation_status") != "implemented":
        errors.append(f"not_implemented:{feature_id}")
    if lifecycle.get("stage") != "active":
        errors.append(f"not_active:{feature_id}")
    if plan.get("horizon") != "current":
        errors.append(f"not_current:{feature_id}")
    if plan.get("target_lifecycle_stage") != "active":
        errors.append(f"target_not_active:{feature_id}")
    if not feature.get("claim_ids"):
        errors.append(f"missing_claims:{feature_id}")
    if not feature.get("test_ids"):
        errors.append(f"missing_tests:{feature_id}")
    if not lifecycle.get("note"):
        errors.append(f"missing_note:{feature_id}")
    if feature_id in supported_surface_ids:
        errors.append(f"declared_unsupported_but_surface_supported:{feature_id}")
    if not validate_unsupported_feature_runtime(feature_id):
        errors.append(f"runtime_not_unsupported:{feature_id}")
    return errors


def validate_unsupported_feature_declaration(feature: dict[str, Any], supported_surface_ids: set[str] | None = None) -> bool:
    return not unsupported_feature_declaration_errors(feature, supported_surface_ids)
