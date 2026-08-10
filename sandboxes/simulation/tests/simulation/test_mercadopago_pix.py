from copy import deepcopy

from app.simulation.mercadopago import MercadoPagoNativeError, MercadoPagoPixProvider
from app.simulation.mercadopago_scenarios import BASE_REQUEST, run_all


def test_mercado_pago_scenarios_complete():
    results = run_all()
    assert set(results) == {"MP-PIX-001", "MP-PIX-002", "MP-PIX-003", "MP-PIX-004", "MP-PIX-005", "MP-PIX-006", "MP-PIX-007", "MP-PIX-008", "MP-PIX-009", "MP-PIX-010"}
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
