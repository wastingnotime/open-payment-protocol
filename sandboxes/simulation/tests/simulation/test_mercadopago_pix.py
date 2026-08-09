from copy import deepcopy

from app.simulation.mercadopago import MercadoPagoNativeError, MercadoPagoPixProvider
from app.simulation.mercadopago_scenarios import BASE_REQUEST, run_all


def test_mercado_pago_scenarios_complete():
    results = run_all()
    assert set(results) == {"MP-PIX-001", "MP-PIX-002", "MP-PIX-003"}
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
