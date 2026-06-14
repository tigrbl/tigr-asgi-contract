from __future__ import annotations

import pytest

from tigr_asgi_contract import (
    SemanticState,
    semantic_capabilities,
    semantic_domain,
    semantic_states,
    semantic_transition_target,
    validate_semantic_sequence,
    validate_semantic_transition,
)


def test_t0_channel_lifecycle_domain_is_contract_owned() -> None:
    domain = semantic_domain("channel_lifecycle")

    assert domain["owner"] == "tigr-asgi-contract"
    assert domain["initial"] == "initialized"
    assert set(semantic_states("channel_lifecycle")) == {
        "initialized",
        "opening",
        "open",
        "read_closed",
        "write_closed",
        "closing",
        "closed",
        "failed",
        "lost",
    }
    assert "half_open" not in semantic_states("channel_lifecycle")
    assert SemanticState.READ_CLOSED.value == "read_closed"
    assert SemanticState.WRITE_CLOSED.value == "write_closed"


def test_t1_channel_lifecycle_transitions_are_directional() -> None:
    assert validate_semantic_sequence(
        "channel_lifecycle",
        [
            "channel.opening",
            "channel.opened",
            "channel.read_closed",
            "channel.write_closed",
        ],
    )
    assert validate_semantic_sequence(
        "channel_lifecycle",
        [
            "channel.opening",
            "channel.opened",
            "channel.write_closed",
            "channel.read_closed",
        ],
    )
    assert semantic_transition_target("channel_lifecycle", "open", "channel.read_closed") == "read_closed"
    assert semantic_transition_target("channel_lifecycle", "open", "channel.write_closed") == "write_closed"


@pytest.mark.parametrize(
    ("state", "event"),
    [
        ("initialized", "channel.read_closed"),
        ("read_closed", "channel.read_closed"),
        ("write_closed", "channel.write_closed"),
        ("closed", "channel.opened"),
        ("failed", "channel.closed"),
        ("lost", "channel.closed"),
    ],
)
def test_t2_channel_lifecycle_rejects_illegal_or_terminal_transitions(
    state: str,
    event: str,
) -> None:
    assert not validate_semantic_transition("channel_lifecycle", state, event)


def test_t2_channel_lifecycle_capability_effects_and_compatibility_are_canonical() -> None:
    domain = semantic_domain("channel_lifecycle")

    assert "can_report_read_closed" in semantic_capabilities("channel_lifecycle")
    assert "can_report_write_closed" in semantic_capabilities("channel_lifecycle")
    assert domain["capability_effects"]["read_closed"] == {
        "can_drain": True,
        "can_read": False,
        "can_write": True,
        "terminal": False,
    }
    assert domain["capability_effects"]["write_closed"] == {
        "can_drain": True,
        "can_read": True,
        "can_write": False,
        "terminal": False,
    }
    assert domain["capability_effects"]["lost"]["terminal"] is True
    assert any(
        row["state"] == "write_closed" and "completion" in row["rule"]
        for row in domain["compatibility"]
    )
