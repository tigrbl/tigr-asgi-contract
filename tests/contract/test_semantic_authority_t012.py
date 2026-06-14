from __future__ import annotations

import pytest

from tigr_asgi_contract import (
    EmitCompletionLevel,
    semantic_capabilities,
    semantic_states,
    semantic_transition_target,
    validate_semantic_sequence,
    validate_semantic_transition,
)
from tigr_asgi_contract.registry import SEMANTIC_DOMAINS


def test_t0_semantic_domains_are_canonical_and_owned_by_contract() -> None:
    assert set(SEMANTIC_DOMAINS) == {
        "backpressure",
        "cancellation",
        "channel_lifecycle",
        "completion",
        "disconnect",
    }
    assert all(domain["owner"] == "tigr-asgi-contract" for domain in SEMANTIC_DOMAINS.values())
    assert set(semantic_states("completion")) == {
        "accepted_by_runtime",
        "queued_for_transport",
        "flushed_to_transport",
        "peer_acknowledged",
        "failed_during_emit",
        "aborted_by_peer",
    }
    assert {item.value for item in EmitCompletionLevel} == set(semantic_states("completion"))


def test_t1_semantic_transition_validation_accepts_legal_sequences() -> None:
    assert validate_semantic_sequence(
        "completion",
        [
            "completion.queued",
            "completion.flushed",
            "completion.peer_acknowledged",
        ],
    )
    assert validate_semantic_sequence(
        "backpressure",
        [
            "backpressure.congested",
            "backpressure.saturated",
            "backpressure.draining",
            "backpressure.resumed",
            "backpressure.writable",
        ],
    )
    assert validate_semantic_sequence(
        "cancellation",
        [
            "cancellation.propagated",
            "cancellation.acknowledged",
            "cancellation.completed",
        ],
    )
    assert semantic_transition_target("disconnect", "graceful", "disconnect.peer_reset") == "peer_reset"


@pytest.mark.parametrize(
    ("domain", "state", "event"),
    [
        ("completion", "accepted_by_runtime", "backpressure.saturated"),
        ("backpressure", "writable", "cancellation.propagated"),
        ("cancellation", "requested", "completion.flushed"),
        ("disconnect", "peer_reset", "disconnect.timeout"),
    ],
)
def test_t2_semantic_transition_validation_rejects_cross_domain_or_terminal_misuse(
    domain: str,
    state: str,
    event: str,
) -> None:
    assert not validate_semantic_transition(domain, state, event)


def test_t2_semantic_capabilities_express_required_runtime_observability() -> None:
    assert "can_report_peer_acknowledgement" in semantic_capabilities("completion")
    assert "can_apply_flow_control" in semantic_capabilities("backpressure")
    assert "can_signal_application_cancellation" in semantic_capabilities("cancellation")
    assert "can_detect_stream_reset" in semantic_capabilities("disconnect")
