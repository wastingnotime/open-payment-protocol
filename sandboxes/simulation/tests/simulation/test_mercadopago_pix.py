from copy import deepcopy
import json

from app.simulation.mercadopago import MercadoPagoNativeError, MercadoPagoPixProvider
from app.simulation.mercadopago_scenarios import BASE_REQUEST, run_all


def test_mercado_pago_scenarios_complete():
    results = run_all()
    assert set(results) == {f"MP-PIX-{number:03d}" for number in range(1, 18)}
    assert results["MP-PIX-001"]["projection"]


def test_order_preserves_decimal_strings_and_native_statuses():
    provider = MercadoPagoPixProvider()
    order = provider.create_order(deepcopy(BASE_REQUEST), idempotency_key="test-mp-1")
    assert order["total_amount"] == "50.00"
    assert order["status"] == "action_required"
    assert order["status_detail"] == "waiting_transfer"
    assert order["transactions"]["payments"][0]["payment_method"]["qr_code"]


def test_reused_key_is_documented_conflict():
    provider = MercadoPagoPixProvider()
    provider.create_order(deepcopy(BASE_REQUEST), idempotency_key="test-mp-2")
    try:
        provider.create_order(deepcopy(BASE_REQUEST), idempotency_key="test-mp-2")
    except MercadoPagoNativeError as exc:
        assert exc.error.status == 409
        assert exc.error.code == "idempotency_key_already_used"
    else:
        raise AssertionError("expected Mercado Pago idempotency conflict")


def test_mercado_pago_scenarios_expose_native_events():
    results = run_all()
    assert results["MP-PIX-001"]["observations"][0]["payload"]["type"] == "order.created"
    assert results["MP-PIX-002"]["observations"][0]["payload"]["type"] == "order.rejected"
    assert results["MP-PIX-003"]["observations"][0]["payload"]["type"] == "order.idempotency_conflict"


def test_documented_async_variant_preserves_processing_without_payments():
    result = run_all()["MP-PIX-004"]
    observation = next(item for item in result["observations"] if item["name"] == "native_async_result")
    assert observation["payload"]["status"] == "processing"
    assert observation["payload"]["payments_present"] is False


def test_async_reconciliation_get_preserves_processing_boundary():
    result = run_all()["MP-PIX-005"]
    query = result["observations"][0]["payload"]
    assert query["reconciliation"] == "get"
    assert query["status"] == "processing"
    assert query["payments_present"] is False


def test_unknown_order_retrieval_is_native_not_found_boundary():
    result = run_all()["MP-PIX-006"]
    error = result["observations"][0]["payload"]
    assert error["status"] == 404
    assert error["code"] == "order_not_found"


def test_non_pix_payment_method_is_native_property_value_boundary():
    result = run_all()["MP-PIX-007"]
    error = result["observations"][0]["payload"]
    assert error["status"] == 400
    assert error["code"] == "property_value"


def test_missing_payer_is_native_required_properties_boundary():
    result = run_all()["MP-PIX-008"]
    error = result["observations"][0]["payload"]
    assert error["status"] == 400
    assert error["code"] == "required_properties"


def test_multiple_payments_are_native_property_value_boundary():
    result = run_all()["MP-PIX-009"]
    error = result["observations"][0]["payload"]
    assert error["status"] == 400
    assert error["code"] == "property_value"


def test_missing_idempotency_key_is_native_required_properties_boundary():
    result = run_all()["MP-PIX-010"]
    error = result["observations"][0]["payload"]
    assert error["status"] == 400
    assert error["code"] == "required_properties"


def test_processing_order_notification_preserves_signature_boundary():
    result = run_all()["MP-PIX-011"]
    notification = result["observations"][0]["payload"]
    assert notification["transport"] == "https_post_json"
    assert notification["topic"] == "order"
    assert notification["authoritative_reconciliation"] == "get"
    assert notification["signature_verified"] is True


def test_mismatched_order_notification_signature_is_discarded():
    result = run_all()["MP-PIX-012"]
    notification = result["observations"][0]["payload"]
    assert notification["signature_verified"] is False
    assert notification["action"] == "discard"


def test_mercado_pago_notification_report_does_not_expose_webhook_secret():
    result = run_all()["MP-PIX-011"]
    assert "WEBHOOK_SECRET_DOCUMENTATION" not in json.dumps(result, sort_keys=True)


def test_signature_canonicalizes_data_id_to_lowercase():
    token = MercadoPagoPixProvider.signature("secret", data_id="ORD_MixedCase", request_id="request", timestamp="1700000000")
    assert MercadoPagoPixProvider.verify_signature("secret", data_id="ord_mixedcase", request_id="request", timestamp="1700000000", received=token)


def test_order_notification_points_to_authoritative_order_id():
    result = run_all()["MP-PIX-011"]
    notification = result["observations"][0]["payload"]
    assert notification["authoritative_reconciliation"] == "get"
    assert notification["order_id"].startswith("ORD_ASYNC_DOCUMENTATION_")


def test_partial_refund_scenario_preserves_provider_native_return_boundary():
    result = run_all()["MP-PIX-013"]
    refund = result["observations"][-1]["payload"]
    assert refund["status"] == "partially_refunded"
    assert refund["funds_returned_to"] == "payer_account"


def test_total_refund_scenario_preserves_provider_native_status():
    result = run_all()["MP-PIX-014"]
    refund = result["observations"][0]["payload"]
    assert refund["status"] == "refunded"


def test_refund_preserves_decimal_amounts_and_partial_status():
    provider = MercadoPagoPixProvider()
    order = provider.create_order(deepcopy(BASE_REQUEST), idempotency_key="refund-001")
    provider.mark_pix_approved(order["id"])

    refunded = provider.refund_order(order["id"], amount="20.00")

    payment = refunded["transactions"]["payments"][0]
    assert payment["status"] == "partially_refunded"
    assert payment["refunded_amount"] == "20.00"
    assert refunded["status"] == "partially_refunded"


def test_refund_without_amount_refunds_remaining_total():
    provider = MercadoPagoPixProvider()
    order = provider.create_order(deepcopy(BASE_REQUEST), idempotency_key="refund-002")
    provider.mark_pix_approved(order["id"])

    refunded = provider.refund_order(order["id"])

    assert refunded["status"] == "refunded"
    assert refunded["transactions"]["payments"][0]["refunded_amount"] == "50.00"


def test_refund_over_total_is_native_invalid_amount_boundary():
    provider = MercadoPagoPixProvider()
    order = provider.create_order(deepcopy(BASE_REQUEST), idempotency_key="refund-003")
    provider.mark_pix_approved(order["id"])
    try:
        provider.refund_order(order["id"], amount="50.01")
    except MercadoPagoNativeError as exc:
        assert exc.error.code == "invalid_refund_amount"
    else:
        raise AssertionError("expected Mercado Pago refund amount rejection")


def test_unpaid_cancellation_preserves_native_canceled_status():
    provider = MercadoPagoPixProvider()
    order = provider.create_order(deepcopy(BASE_REQUEST), idempotency_key="expiry-001")

    canceled = provider.cancel_unpaid_order(order["id"])

    assert canceled["status"] == "canceled"
    assert canceled["transactions"]["payments"][0]["status"] == "canceled"


def test_expiration_preserves_documented_status_alternative():
    provider = MercadoPagoPixProvider()
    order = provider.create_order(deepcopy(BASE_REQUEST), idempotency_key="expiry-002")

    expired = provider.resolve_unpaid_expiration(order["id"], outcome="expired")

    assert expired["status"] == "expired"
    assert expired["status_detail"] == "expired"


def test_expiration_scenarios_keep_both_documented_outcomes_visible():
    results = run_all()
    assert results["MP-PIX-016"]["observations"][0]["payload"]["status"] == "expired"
    assert results["MP-PIX-017"]["observations"][0]["payload"]["status"] == "canceled"
