import pytest

from tigr_asgi_contract.transport_stacks import (
    H2_WS,
    H3_WS,
    H3_WT,
    H3_WT_WS,
    TRANSPORT_STACK_CONTRACTS,
    TransportStackError,
    classify_transport_stack,
    compose_h3_listener_carriers,
    require_valid_transport_stack,
)


def test_stack_normalization_is_case_and_whitespace_tolerant():
    assert classify_transport_stack(" H3 + WT ").stack == H3_WT
    assert classify_transport_stack("H2+WS").stack == H2_WS


def test_unknown_and_non_string_stack_inputs_fail_closed():
    for stack in ("h4", "ws-over-wt", ""):
        with pytest.raises(TransportStackError):
            classify_transport_stack(stack)
    with pytest.raises(TransportStackError):
        classify_transport_stack(3)  # type: ignore[arg-type]


def test_contract_registry_view_is_immutable():
    with pytest.raises(TypeError):
        TRANSPORT_STACK_CONTRACTS["local"] = TRANSPORT_STACK_CONTRACTS[H3_WT]  # type: ignore[index]


def test_h3_listener_rejects_duplicate_and_cross_protocol_carriers():
    with pytest.raises(TransportStackError):
        compose_h3_listener_carriers(H3_WT, H3_WT)
    with pytest.raises(TransportStackError):
        compose_h3_listener_carriers(H3_WT, "h2+wt")


def test_invalid_nested_stack_cannot_be_required_even_after_normalization():
    with pytest.raises(TransportStackError):
        require_valid_transport_stack(f" {H3_WT_WS.upper()} ")
    assert compose_h3_listener_carriers(H3_WT, H3_WS) == (H3_WT, H3_WS)
