from copy import deepcopy

from app.simulation.pagbank import PagBankNativeError, PagBankPixProvider
from app.simulation.pagbank_scenarios import BASE_REQUEST, run_all


def test_pagbank_scenarios_complete():
    results = run_all()
    assert set(results) == {"PB-PIX-001", "PB-PIX-002", "PB-PIX-003", "PB-PIX-004"}
    assert results["PB-PIX-001"]["projection"]


def test_order_starts_with_qr_and_no_charge():
    provider = PagBankPixProvider()
    order = provider.create_order(deepcopy(BASE_REQUEST), idempotency_key="test-pb-1")
    assert order["qr_codes"][0]["amount"]["value"] == 1000
    assert order["charges"] == []
    assert order["qr_codes"][0]["links"][0]["rel"] == "QRCODE.PNG"


def test_reused_key_is_documented_conflict():
    provider = PagBankPixProvider()
    provider.create_order(deepcopy(BASE_REQUEST), idempotency_key="test-pb-2")
    try:
        provider.create_order(deepcopy(BASE_REQUEST), idempotency_key="test-pb-2")
    except PagBankNativeError as exc:
        assert exc.error.status == 409
        assert exc.error.code == "idempotency_key_in_use"
    else:
        raise AssertionError("expected PagBank idempotency conflict")


def test_paid_pix_creates_charge_while_qr_remains_on_order():
    result = run_all()["PB-PIX-004"]
    order = next(iter(result["projection"].values()))
    assert order["charges"][0]["status"] == "PAID"
    assert order["charges"][0]["payment_method"]["pix"]["end_to_end_id"]
    assert order["qr_codes"]
