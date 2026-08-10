from copy import deepcopy

from app.simulation.pagbank import PagBankNativeError, PagBankPixProvider
from app.simulation.pagbank_scenarios import BASE_REQUEST, run_all


def test_pagbank_scenarios_complete():
    results = run_all()
    assert set(results) == {f"PB-PIX-{number:03d}" for number in range(1, 16)}
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


def test_unknown_order_retrieval_is_native_not_found_boundary():
    result = run_all()["PB-PIX-005"]
    error = result["observations"][0]["payload"]
    assert error["status"] == 404
    assert error["code"] == "order_not_found"


def test_duplicate_pix_payment_is_native_invalid_status_boundary():
    result = run_all()["PB-PIX-006"]
    error = result["observations"][0]["payload"]
    assert error["status"] == 400
    assert error["code"] == "invalid_status"


def test_multiple_qr_codes_are_native_invalid_parameter_boundary():
    result = run_all()["PB-PIX-007"]
    error = result["observations"][0]["payload"]
    assert error["status"] == 400
    assert error["code"] == "invalid_parameter"


def test_missing_qr_codes_is_native_required_parameter_boundary():
    result = run_all()["PB-PIX-008"]
    error = result["observations"][0]["payload"]
    assert error["status"] == 400
    assert error["code"] == "required_parameter"


def test_missing_reference_id_is_native_required_parameter_boundary():
    result = run_all()["PB-PIX-009"]
    error = result["observations"][0]["payload"]
    assert error["status"] == 400
    assert error["code"] == "required_parameter"


def test_missing_idempotency_key_is_native_required_parameter_boundary():
    result = run_all()["PB-PIX-010"]
    error = result["observations"][0]["payload"]
    assert error["status"] == 400
    assert error["code"] == "required_parameter"


def test_paid_notification_preserves_full_order_and_authenticity_boundary():
    result = run_all()["PB-PIX-011"]
    notification = result["observations"][0]["payload"]
    assert notification["transport"] == "https_post"
    assert notification["charge_status"] == "PAID"
    assert notification["has_qr_code"] is True
    assert notification["authenticity_verified"] is True


def test_mismatched_notification_authenticity_is_discarded():
    result = run_all()["PB-PIX-012"]
    notification = result["observations"][0]["payload"]
    assert notification["authenticity_verified"] is False
    assert notification["action"] == "discard"


def test_authenticity_token_uses_exact_raw_bytes():
    raw_payload = b'{"status":"PAID"}'
    token = PagBankPixProvider.authenticity_token("ACCOUNT_TOKEN_DOCUMENTATION", raw_payload)
    assert PagBankPixProvider.verify_authenticity("ACCOUNT_TOKEN_DOCUMENTATION", raw_payload, token)
    assert not PagBankPixProvider.verify_authenticity("ACCOUNT_TOKEN_DOCUMENTATION", raw_payload + b" ", token)


def test_notification_url_is_preserved_on_native_order_projection():
    result = run_all()["PB-PIX-013"]
    configuration = result["observations"][0]["payload"]
    assert configuration["notification_urls"] == ["https://example.invalid/webhooks/pagbank"]
    assert configuration["transport"] == "https_post"


def test_multiple_notification_urls_are_native_invalid_parameter_boundary():
    result = run_all()["PB-PIX-014"]
    error = result["observations"][0]["payload"]
    assert error["status"] == 400
    assert error["code"] == "invalid_parameter"


def test_insecure_notification_url_is_native_invalid_parameter_boundary():
    result = run_all()["PB-PIX-015"]
    error = result["observations"][0]["payload"]
    assert error["status"] == 400
    assert error["code"] == "invalid_parameter"
