import pytest

from tigr_asgi_contract.transport_stacks import (
    ACTIVE_DRAFT,
    H2_WT,
    H3_WS,
    H3_WT,
    H3_WT_WS,
    STABLE_RFC,
    TransportStackError,
    classify_transport_stack,
    compose_h3_listener_carriers,
    require_valid_transport_stack,
    valid_transport_stacks,
)


def test_classifies_stable_and_draft_contract_stacks():
    assert classify_transport_stack("h2").maturity == STABLE_RFC
    assert classify_transport_stack(H3_WS).source == "RFC 9220"
    assert classify_transport_stack(H3_WT).maturity == ACTIVE_DRAFT
    assert classify_transport_stack(H2_WT).source == "draft-ietf-webtrans-http2-14"


def test_rejects_invalid_nested_h3_webtransport_websocket_stack():
    invalid = classify_transport_stack(H3_WT_WS)
    assert invalid.valid is False
    assert invalid.maturity == "invalid-local"
    with pytest.raises(TransportStackError):
        require_valid_transport_stack(H3_WT_WS)


def test_h3_listener_uses_separate_carriers_for_webtransport_and_websocket():
    assert compose_h3_listener_carriers("h3", H3_WT, H3_WS) == ("h3", H3_WT, H3_WS)
    with pytest.raises(TransportStackError):
        compose_h3_listener_carriers(H3_WT_WS)


def test_valid_contract_stack_inventory_excludes_invalid_local_composition():
    assert H3_WT_WS not in valid_transport_stacks()
    assert {H3_WT, H3_WS}.issubset(valid_transport_stacks())
