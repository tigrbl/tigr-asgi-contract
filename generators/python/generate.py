from __future__ import annotations
from pathlib import Path
import json
import sys
from pathlib import Path
from pprint import pformat
ROOT0 = Path(__file__).resolve().parents[1]
if str(ROOT0) not in sys.path:
    sys.path.insert(0, str(ROOT0))
from common import contract_data, member_name

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "packages" / "contract-py" / "src" / "tigr_asgi_contract"

def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

UNSUPPORTED_VALIDATORS_TEXT = '''
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
'''

def emit_enum(module_name: str, class_name: str, values: list[str]) -> None:
    body = "\n".join(f"    {member_name(v)} = {v!r}" for v in values)
    write(OUT / f"{module_name}.py", f"from ._enum_compat import StrEnum\n\n\nclass {class_name}(StrEnum):\n{body}\n")

def main() -> None:
    d = contract_data()
    write(OUT / "_enum_compat.py", 'from __future__ import annotations\nfrom enum import Enum\n\ntry:\n    from enum import StrEnum\nexcept ImportError:\n    class StrEnum(str, Enum):\n        pass\n')
    emit_enum("scope_types", "ScopeType", d["scope_types"])
    emit_enum("channels", "Channel", d["channels"])
    emit_enum("directions", "Direction", d["directions"])
    emit_enum("framing", "Framing", d["framings"])
    emit_enum("bindings", "Binding", list(d["bindings"].keys()))
    emit_enum("protocols", "Protocol", list(d["protocols"].keys()))
    emit_enum("exchanges", "Exchange", d["exchanges"])
    emit_enum("families", "Family", d["families"])
    emit_enum("subevents", "Subevent", d["all_subevents"])
    emit_enum("frames", "Frame", list(d["frames"].keys()))
    emit_enum("completion", "EmitCompletionLevel", list(d["completion"]["levels"].keys()))
    semantic_enum_values = [
        state
        for domain in d["semantic_domains"].values()
        for state in domain["states"]
    ]
    emit_enum("semantics", "SemanticState", sorted(set(semantic_enum_values)))

    write(OUT / "version.py", f'CONTRACT_VERSION = "{d["version"]}"\nCONTRACT_SERDE_VERSION = {d["compatibility"]["serde_version"]}\n')
    write(OUT / "capabilities.py", 'from pydantic import BaseModel\n\n\nclass FamilyCapabilities(BaseModel):\n    request: bool = False\n    session: bool = False\n    message: bool = False\n    stream_in: bool = False\n    stream_out: bool = False\n    datagram: bool = False\n    lifespan: bool = False\n')
    write(OUT / "compatibility.py", 'from pydantic import BaseModel\n\n\nclass Compatibility(BaseModel):\n    contract_name: str\n    contract_version: str\n    serde_version: int\n    schema_draft: str\n    min_tigrcorn_version: str | None = None\n    min_tigrbl_version: str | None = None\n')
    write(OUT / "ids.py", 'from pydantic import BaseModel\n\n\nclass UnitIds(BaseModel):\n    unit_id: str | None = None\n    parent_unit_id: str | None = None\n    session_id: str | None = None\n    stream_id: int | None = None\n    datagram_id: int | None = None\n    emit_id: str | None = None\n')
    write(OUT / "models.py", 'from pydantic import BaseModel, Field\nfrom .capabilities import FamilyCapabilities\n\n\nclass TlsMetadata(BaseModel):\n    version: str | None = None\n    cipher: str | None = None\n    verified: bool = False\n    peer_identity: str | None = None\n    peer_cert: dict | None = None\n\n\nclass TransportMetadata(BaseModel):\n    binding: str\n    network: str\n    secure: bool\n    alpn: str | None = None\n    tls: TlsMetadata | None = None\n    framing: str | None = None\n\n\nclass WebSocketScopeExt(BaseModel):\n    subprotocol: str | None = None\n\n\nclass SseScopeExt(BaseModel):\n    retry_ms: int | None = None\n    last_event_id: str | None = None\n\n\nclass WebTransportScopeExt(BaseModel):\n    session_id: str | None = None\n    supports_datagrams: bool = False\n    supports_bidi_streams: bool = False\n    supports_uni_streams: bool = False\n    max_datagram_size: int | None = None\n\n\nclass ScopeExt(BaseModel):\n    transport: TransportMetadata\n    family_capabilities: FamilyCapabilities\n    websocket: WebSocketScopeExt | None = None\n    sse: SseScopeExt | None = None\n    webtransport: WebTransportScopeExt | None = None\n\n\nclass DerivedEvent(BaseModel):\n    family: str\n    subevent: str\n    repeated: bool = False\n\n\nclass EventClassification(BaseModel):\n    event: str\n    channel: str\n    scope_type: str\n    binding: str\n    family: str\n    exchange: str\n    direction: str\n    allowed_framings: list[str] = Field(default_factory=list)\n    required_scope_fields: list[str] = Field(default_factory=list)\n    required_payload_fields: list[str] = Field(default_factory=list)\n    capability_gates: list[str] = Field(default_factory=list)\n    stream_direction: str | None = None\n')
    write(OUT / "scope.py", 'from pydantic import BaseModel\nfrom .models import ScopeExt\n\n\nclass ContractScope(BaseModel):\n    type: str\n    asgi: dict\n    scheme: str\n    http_version: str | None = None\n    method: str | None = None\n    path: str\n    query_string: bytes = b""\n    headers: list[tuple[bytes, bytes]]\n    client: tuple[str, int] | None = None\n    server: tuple[str, int] | None = None\n    ext: ScopeExt\n')
    events = list(d["schemas"]["event.schema.json"]["properties"]["type"]["enum"])
    event_members = "\n".join(f"    {member_name(v)} = {v!r}" for v in events)
    write(OUT / "events.py", f'from ._enum_compat import StrEnum\nfrom pydantic import BaseModel, Field\n\n\nclass TransportEventType(StrEnum):\n{event_members}\n\n\nclass ContractEvent(BaseModel):\n    type: TransportEventType\n    message: str | None = None\n    payload: dict = Field(default_factory=dict)\n')
    registry_content = "BINDING_FAMILY_MATRIX = " + json.dumps(d["binding_family"], indent=2) + "\n\n"
    registry_content += "FAMILY_SUBEVENT_MATRIX = " + json.dumps(d["family_subevent"], indent=2) + "\n\n"
    registry_content += "BINDING_SUBEVENT_MATRIX = " + json.dumps(d["binding_subevent"], indent=2) + "\n"
    registry_content += "\nPROTOCOLS = " + pformat(d["protocols"], sort_dicts=True) + "\n"
    registry_content += "\nAUTOMATA = " + pformat(d["automata"], sort_dicts=True) + "\n"
    registry_content += "\nFRAMES = " + pformat(d["frames"], sort_dicts=True) + "\n"
    registry_content += "\nEXTENSIONS = " + pformat(d["extensions"], sort_dicts=True) + "\n"
    registry_content += "\nCHANNELS = " + pformat(d["channels"], sort_dicts=True) + "\n"
    registry_content += "\nDIRECTIONS = " + pformat(d["directions"], sort_dicts=True) + "\n"
    registry_content += "\nFRAMINGS = " + pformat(d["framings"], sort_dicts=True) + "\n"
    registry_content += "\nEVENT_CLASSIFICATIONS = " + pformat(d["event_classifications"], sort_dicts=True) + "\n"
    registry_content += "\nSEMANTIC_DOMAINS = " + pformat(d["semantic_domains"], sort_dicts=True) + "\n"
    write(OUT / "registry.py", registry_content)
    write(OUT / "validators.py", 'from __future__ import annotations\nfrom typing import Any\nfrom .registry import AUTOMATA, BINDING_FAMILY_MATRIX, FAMILY_SUBEVENT_MATRIX, BINDING_SUBEVENT_MATRIX, PROTOCOLS, EVENT_CLASSIFICATIONS, FRAMINGS, SEMANTIC_DOMAINS\nfrom .models import EventClassification\n\nLEGALITY_CODES = frozenset({"R", "O", "D", "F"})\nLEGALITY_ALLOWED_CODES = frozenset({"R", "O", "D"})\n\n\ndef _scope_value(scope: Any, key: str, default: Any = None) -> Any:\n    if isinstance(scope, dict):\n        return scope.get(key, default)\n    return getattr(scope, key, default)\n\n\ndef _binding_from_scope(scope: Any) -> str | None:\n    ext = _scope_value(scope, "ext", {}) or {}\n    transport = ext.get("transport") if isinstance(ext, dict) else getattr(ext, "transport", None)\n    if isinstance(transport, dict):\n        return transport.get("binding")\n    return getattr(transport, "binding", None)\n\n\ndef _webtransport_ext(scope: Any) -> Any:\n    ext = _scope_value(scope, "ext", {}) or {}\n    return ext.get("webtransport") if isinstance(ext, dict) else getattr(ext, "webtransport", None)\n\n\ndef _has_capability(scope: Any, gate: str) -> bool:\n    wt = _webtransport_ext(scope)\n    if wt is None:\n        return False\n    if isinstance(wt, dict):\n        return bool(wt.get(gate))\n    return bool(getattr(wt, gate, False))\n\n\ndef semantic_domain(domain: str) -> dict[str, Any]:\n    return SEMANTIC_DOMAINS[domain]\n\n\ndef semantic_states(domain: str) -> tuple[str, ...]:\n    return tuple(SEMANTIC_DOMAINS[domain]["states"])\n\n\ndef semantic_events(domain: str) -> tuple[str, ...]:\n    return tuple(row["event"] for row in SEMANTIC_DOMAINS[domain]["transitions"])\n\n\ndef semantic_capabilities(domain: str) -> tuple[str, ...]:\n    return tuple(SEMANTIC_DOMAINS[domain].get("capabilities", ()))\n\n\ndef semantic_transition_target(domain: str, state: str, event: str) -> str:\n    for row in SEMANTIC_DOMAINS[domain]["transitions"]:\n        if row["from"] == state and row["event"] == event:\n            return row["to"]\n    raise ValueError(f"illegal semantic transition for {domain}: {state} + {event}")\n\n\ndef validate_semantic_transition(domain: str, state: str, event: str) -> bool:\n    try:\n        semantic_transition_target(domain, state, event)\n    except (KeyError, ValueError):\n        return False\n    return True\n\n\ndef validate_semantic_sequence(domain: str, events: list[str]) -> bool:\n    spec = SEMANTIC_DOMAINS[domain]\n    state = spec["initial"]\n    for event in events:\n        try:\n            state = semantic_transition_target(domain, state, event)\n        except ValueError:\n            return False\n    terminals = set(spec.get("terminal", ()))\n    return not terminals or state in terminals or bool(events)\n\n\ndef binding_supports_family(binding: str, family: str) -> bool:\n    return binding_family_legality(binding, family) in LEGALITY_ALLOWED_CODES\n\n\ndef family_supports_subevent(family: str, subevent: str) -> bool:\n    return family_subevent_legality(family, subevent) in LEGALITY_ALLOWED_CODES\n\n\ndef binding_supports_subevent(binding: str, subevent: str) -> bool:\n    return binding_subevent_legality(binding, subevent) in LEGALITY_ALLOWED_CODES\n\n\ndef binding_family_legality(binding: str, family: str) -> str:\n    return BINDING_FAMILY_MATRIX.get(binding, {}).get(family, "F")\n\n\ndef family_subevent_legality(family: str, subevent: str) -> str:\n    return FAMILY_SUBEVENT_MATRIX.get(family, {}).get(subevent, "F")\n\n\ndef binding_subevent_legality(binding: str, subevent: str) -> str:\n    return BINDING_SUBEVENT_MATRIX.get(binding, {}).get(subevent, "F")\n\n\ndef is_required_legality(code: str) -> bool:\n    return code == "R"\n\n\ndef is_optional_legality(code: str) -> bool:\n    return code == "O"\n\n\ndef is_derived_legality(code: str) -> bool:\n    return code == "D"\n\n\ndef is_forbidden_legality(code: str) -> bool:\n    return code == "F"\n\n\ndef validate_binding_family(binding: str, family: str) -> bool:\n    return binding_supports_family(binding, family)\n\n\ndef validate_family_subevent(family: str, subevent: str) -> bool:\n    return family_supports_subevent(family, subevent)\n\n\ndef validate_binding_subevent(binding: str, subevent: str) -> bool:\n    return binding_supports_subevent(binding, subevent)\n\n\ndef legality_matrix_errors() -> list[str]:\n    errors: list[str] = []\n    bindings = set(BINDING_FAMILY_MATRIX)\n    families = set(FAMILY_SUBEVENT_MATRIX)\n    subevents = {subevent for values in FAMILY_SUBEVENT_MATRIX.values() for subevent in values}\n\n    for binding, family_map in BINDING_FAMILY_MATRIX.items():\n        missing = families - set(family_map)\n        extra = set(family_map) - families\n        errors.extend(f"binding_family_missing:{binding}:{family}" for family in sorted(missing))\n        errors.extend(f"binding_family_unknown:{binding}:{family}" for family in sorted(extra))\n        errors.extend(\n            f"binding_family_bad_code:{binding}:{family}:{code}"\n            for family, code in sorted(family_map.items())\n            if code not in LEGALITY_CODES\n        )\n\n    for family, subevent_map in FAMILY_SUBEVENT_MATRIX.items():\n        errors.extend(\n            f"family_subevent_bad_code:{family}:{subevent}:{code}"\n            for subevent, code in sorted(subevent_map.items())\n            if code not in LEGALITY_CODES\n        )\n    for binding, subevent_map in BINDING_SUBEVENT_MATRIX.items():\n        if binding not in bindings:\n            errors.append(f"binding_subevent_unknown_binding:{binding}")\n        missing = subevents - set(subevent_map)\n        extra = set(subevent_map) - subevents\n        errors.extend(f"binding_subevent_missing:{binding}:{subevent}" for subevent in sorted(missing))\n        errors.extend(f"binding_subevent_unknown:{binding}:{subevent}" for subevent in sorted(extra))\n        errors.extend(\n            f"binding_subevent_bad_code:{binding}:{subevent}:{code}"\n            for subevent, code in sorted(subevent_map.items())\n            if code not in LEGALITY_CODES\n        )\n    return errors\n\n\ndef validate_legality_matrices() -> bool:\n    return not legality_matrix_errors()\n\n\ndef protocol_binding(protocol: str) -> str:\n    return PROTOCOLS[protocol]["binding"]\n\n\ndef event_classification_candidates(scope: Any, channel: str, event_type: str, payload: dict | None = None) -> list[EventClassification]:\n    payload = payload or {}\n    scope_type = _scope_value(scope, "type")\n    binding = _binding_from_scope(scope)\n    rows = []\n    for row in EVENT_CLASSIFICATIONS:\n        if row["event"] != event_type or row["channel"] != channel:\n            continue\n        if row["scope_type"] != scope_type:\n            continue\n        if binding is not None and row["binding"] != binding:\n            continue\n        if row.get("stream_direction") and payload.get("stream_direction") != row["stream_direction"]:\n            continue\n        if any(not _has_capability(scope, gate) for gate in row.get("capability_gates", [])):\n            continue\n        rows.append(EventClassification(**row))\n    return rows\n\n\ndef classify_event(scope: Any, channel: str, event_type: str, payload: dict | None = None) -> EventClassification:\n    rows = event_classification_candidates(scope, channel, event_type, payload)\n    if not rows:\n        raise ValueError(f"No event classification for {channel}:{event_type}")\n    return rows[0]\n\n\ndef validate_event_classification(scope: Any, channel: str, event_type: str, payload: dict | None = None) -> bool:\n    try:\n        classify_event(scope, channel, event_type, payload)\n    except ValueError:\n        return False\n    return True\n\n\ndef validate_framing_for_classification(framing: str | None, classification: EventClassification | dict) -> bool:\n    if framing is None:\n        return True\n    if framing not in FRAMINGS:\n        return False\n    allowed = classification.allowed_framings if isinstance(classification, EventClassification) else classification.get("allowed_framings", [])\n    return framing in allowed\n\n\ndef validate_event_payload(event_type: str, payload: dict, classification: EventClassification | dict | None = None) -> bool:\n    if not isinstance(payload, dict) or "subsurface" in payload:\n        return False\n    if event_type == "http.response.pathsend" and not (isinstance(payload.get("path"), str) and payload["path"]):\n        return False\n    if ".stream." in event_type and "stream_id" not in payload:\n        return False\n    if ".datagram." in event_type and "datagram_id" not in payload:\n        return False\n    if classification is not None:\n        required = classification.required_payload_fields if isinstance(classification, EventClassification) else classification.get("required_payload_fields", [])\n        if any(field not in payload for field in required):\n            return False\n        framing = payload.get("framing")\n        if framing is not None and not validate_framing_for_classification(framing, classification):\n            return False\n        if framing == "jsonrpc" and not payload.get("jsonrpc_complete", False):\n            return False\n        if framing == "ndjson" and payload.get("jsonrpc_complete", False):\n            return False\n    return True\n\n\ndef validate_automata_sequence(family: str, subevents: list[str]) -> bool:\n    automaton = AUTOMATA[family]\n    state = automaton["initial"]\n    transitions = {(row["from"], row["event"]): row["to"] for row in automaton["transitions"]}\n    for subevent in subevents:\n        next_state = transitions.get((state, subevent))\n        if next_state is None:\n            return False\n        state = next_state\n    return state in set(automaton["terminal"]) or bool(subevents)\n')
    validators_path = OUT / "validators.py"
    write(validators_path, validators_path.read_text(encoding="utf-8") + UNSUPPORTED_VALIDATORS_TEXT)
    init_text = 'from .version import CONTRACT_VERSION, CONTRACT_SERDE_VERSION\nfrom .scope_types import ScopeType\nfrom .channels import Channel\nfrom .directions import Direction\nfrom .framing import Framing\nfrom .bindings import Binding\nfrom .protocols import Protocol\nfrom .exchanges import Exchange\nfrom .families import Family\nfrom .subevents import Subevent\nfrom .frames import Frame\nfrom .completion import EmitCompletionLevel\nfrom .semantics import SemanticState\nfrom .capabilities import FamilyCapabilities\nfrom .compatibility import Compatibility\nfrom .ids import UnitIds\nfrom .models import TlsMetadata, TransportMetadata, WebSocketScopeExt, SseScopeExt, WebTransportScopeExt, ScopeExt, DerivedEvent, EventClassification\nfrom .scope import ContractScope\nfrom .events import TransportEventType, ContractEvent\nfrom .validators import LEGALITY_ALLOWED_CODES, LEGALITY_CODES, UNSUPPORTED_FEATURE_CATEGORIES, binding_supports_family, family_supports_subevent, binding_supports_subevent, binding_family_legality, family_subevent_legality, binding_subevent_legality, is_required_legality, is_optional_legality, is_derived_legality, is_forbidden_legality, validate_binding_family, validate_family_subevent, validate_binding_subevent, legality_matrix_errors, validate_legality_matrices, protocol_binding, event_classification_candidates, classify_event, validate_event_classification, validate_framing_for_classification, validate_automata_sequence, validate_event_payload, semantic_domain, semantic_states, semantic_events, semantic_capabilities, semantic_transition_target, validate_semantic_transition, validate_semantic_sequence, unsupported_feature_category, validate_unsupported_feature_runtime, unsupported_feature_declaration_errors, validate_unsupported_feature_declaration\nfrom .schema_registry import CONTRACT_ARTIFACT_SCHEMA_PATHS, EVENT_PAYLOAD_SCHEMA_PATHS, FRAME_PAYLOAD_SCHEMA_PATHS, EVENT_SCHEMA_IDS, FRAME_SCHEMA_IDS, contract_artifact_schema_path, contract_artifact_has_schema, event_payload_schema_path, frame_payload_schema_path, event_has_payload_schema, frame_has_payload_schema, event_payload_schema_path_for_payload, frame_payload_schema_path_for_payload, validate_event_payload_discriminator, validate_frame_payload_discriminator, event_payload_schema_errors, frame_payload_schema_errors, validate_event_payload_schema, validate_frame_payload_schema, validate_event_payload_schema_strict, validate_frame_payload_schema_strict\n\n__all__ = [\n    "CONTRACT_VERSION", "CONTRACT_SERDE_VERSION", "ScopeType", "Channel", "Direction", "Framing", "Binding", "Protocol", "Exchange", "Family", "Subevent", "Frame",\n    "EmitCompletionLevel", "SemanticState", "FamilyCapabilities", "Compatibility", "UnitIds", "TlsMetadata", "TransportMetadata",\n    "WebSocketScopeExt", "SseScopeExt", "WebTransportScopeExt", "ScopeExt", "DerivedEvent", "EventClassification", "ContractScope",\n    "TransportEventType", "ContractEvent", "binding_supports_family", "family_supports_subevent",\n    "binding_supports_subevent", "LEGALITY_CODES", "LEGALITY_ALLOWED_CODES", "UNSUPPORTED_FEATURE_CATEGORIES", "binding_family_legality",\n    "family_subevent_legality", "binding_subevent_legality", "is_required_legality", "is_optional_legality",\n    "is_derived_legality", "is_forbidden_legality", "validate_binding_family", "validate_family_subevent",\n    "validate_binding_subevent", "legality_matrix_errors", "validate_legality_matrices", "protocol_binding",\n    "event_classification_candidates", "classify_event", "validate_event_classification", "validate_framing_for_classification",\n    "validate_automata_sequence", "validate_event_payload", "semantic_domain", "semantic_states", "semantic_events",\n    "semantic_capabilities", "semantic_transition_target", "validate_semantic_transition", "validate_semantic_sequence",\n    "unsupported_feature_category", "validate_unsupported_feature_runtime",\n    "unsupported_feature_declaration_errors", "validate_unsupported_feature_declaration",\n    "CONTRACT_ARTIFACT_SCHEMA_PATHS", "EVENT_PAYLOAD_SCHEMA_PATHS", "FRAME_PAYLOAD_SCHEMA_PATHS", "EVENT_SCHEMA_IDS", "FRAME_SCHEMA_IDS",\n    "contract_artifact_schema_path", "contract_artifact_has_schema", "event_payload_schema_path", "frame_payload_schema_path",\n    "event_has_payload_schema", "frame_has_payload_schema", "event_payload_schema_path_for_payload", "frame_payload_schema_path_for_payload",\n    "validate_event_payload_discriminator", "validate_frame_payload_discriminator",\n    "event_payload_schema_errors", "frame_payload_schema_errors", "validate_event_payload_schema", "validate_frame_payload_schema",\n    "validate_event_payload_schema_strict", "validate_frame_payload_schema_strict",\n]\n'
    write(OUT / "__init__.py", init_text)

if __name__ == "__main__":
    main()

