from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType


STABLE_RFC = "stable-rfc"
ACTIVE_DRAFT = "active-draft"
INVALID_LOCAL = "invalid-local"

H11 = "h11"
H2 = "h2"
H3 = "h3"
H2_WS = "h2+ws"
H3_WS = "h3+ws"
H2_WT = "h2+wt"
H3_WT = "h3+wt"
H3_WT_WS = "h3+wt+ws"

_H3_LISTENER_CARRIERS = frozenset({H3, H3_WS, H3_WT})


class TransportStackError(ValueError):
    """Raised when a requested transport stack is not contract-valid."""


@dataclass(frozen=True)
class TransportStackContract:
    stack: str
    valid: bool
    maturity: str
    source: str
    carriers: tuple[str, ...]
    notes: tuple[str, ...] = ()

    @property
    def is_stable_rfc(self) -> bool:
        return self.valid and self.maturity == STABLE_RFC

    @property
    def is_active_draft(self) -> bool:
        return self.valid and self.maturity == ACTIVE_DRAFT


_TRANSPORT_STACKS = {
    H11: TransportStackContract(
        stack=H11,
        valid=True,
        maturity=STABLE_RFC,
        source="RFC 9112",
        carriers=(H11,),
        notes=("HTTP/1.1 has message-body streaming, not multiplexed streams.",),
    ),
    H2: TransportStackContract(
        stack=H2,
        valid=True,
        maturity=STABLE_RFC,
        source="RFC 9113",
        carriers=(H2,),
        notes=("HTTP/2 streams are first-class multiplexed streams.",),
    ),
    H3: TransportStackContract(
        stack=H3,
        valid=True,
        maturity=STABLE_RFC,
        source="RFC 9114 over RFC 9000",
        carriers=(H3,),
        notes=("HTTP/3 is specified over QUIC bidirectional and unidirectional streams.",),
    ),
    H2_WS: TransportStackContract(
        stack=H2_WS,
        valid=True,
        maturity=STABLE_RFC,
        source="RFC 8441",
        carriers=(H2_WS,),
        notes=("WebSocket over HTTP/2 uses Extended CONNECT and :protocol.",),
    ),
    H3_WS: TransportStackContract(
        stack=H3_WS,
        valid=True,
        maturity=STABLE_RFC,
        source="RFC 9220",
        carriers=(H3_WS,),
        notes=("WebSocket over HTTP/3 adapts the RFC 8441 Extended CONNECT model.",),
    ),
    H3_WT: TransportStackContract(
        stack=H3_WT,
        valid=True,
        maturity=ACTIVE_DRAFT,
        source="draft-ietf-webtrans-http3-15",
        carriers=(H3_WT,),
        notes=("WebTransport over HTTP/3 is draft-specified, not an RFC.",),
    ),
    H2_WT: TransportStackContract(
        stack=H2_WT,
        valid=True,
        maturity=ACTIVE_DRAFT,
        source="draft-ietf-webtrans-http2-14",
        carriers=(H2_WT,),
        notes=("WebTransport over HTTP/2 is a draft fallback over HTTP/2 capsules.",),
    ),
    H3_WT_WS: TransportStackContract(
        stack=H3_WT_WS,
        valid=False,
        maturity=INVALID_LOCAL,
        source="local taxonomy rejection",
        carriers=(H3_WT, H3_WS),
        notes=("Use separate H3 WebTransport and H3 WebSocket carriers, not a nested stack.",),
    ),
}

TRANSPORT_STACK_CONTRACTS = MappingProxyType(_TRANSPORT_STACKS)


def normalize_transport_stack(stack: str) -> str:
    if not isinstance(stack, str):
        raise TransportStackError("transport stack must be a string")
    return stack.strip().lower().replace(" ", "")


def classify_transport_stack(stack: str) -> TransportStackContract:
    normalized = normalize_transport_stack(stack)
    try:
        return TRANSPORT_STACK_CONTRACTS[normalized]
    except KeyError as exc:
        raise TransportStackError(f"unknown transport stack: {stack!r}") from exc


def require_valid_transport_stack(stack: str) -> TransportStackContract:
    contract = classify_transport_stack(stack)
    if not contract.valid:
        raise TransportStackError(f"invalid transport stack: {contract.stack}")
    return contract


def valid_transport_stacks() -> tuple[str, ...]:
    return tuple(stack for stack, contract in TRANSPORT_STACK_CONTRACTS.items() if contract.valid)


def compose_h3_listener_carriers(*stacks: str) -> tuple[str, ...]:
    normalized = tuple(normalize_transport_stack(stack) for stack in stacks)
    if H3_WT_WS in normalized:
        raise TransportStackError("h3+wt+ws is not a single contract stack")
    unknown = tuple(stack for stack in normalized if stack not in _H3_LISTENER_CARRIERS)
    if unknown:
        raise TransportStackError(f"not an H3 listener carrier: {unknown[0]}")
    if len(set(normalized)) != len(normalized):
        raise TransportStackError("duplicate H3 listener carriers are not allowed")
    return normalized
