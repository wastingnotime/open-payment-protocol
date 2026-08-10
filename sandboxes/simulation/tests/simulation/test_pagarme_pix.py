from copy import deepcopy

from app.simulation.pagarme import PagarmePixProvider
from app.simulation.pagarme_scenarios import BASE_REQUEST, run_all


def test_pagarme_scenarios_complete():
    results = run_all()
    assert set(results) == {f"PG-PIX-{number:03d}" for number in range(1, 12)}


def test_order_charge_transaction_hierarchy_is_preserved():
    order = PagarmePixProvider().create_order(deepcopy(BASE_REQUEST))
    charge = order["charges"][0]
    assert order["id"].startswith("or_")
    assert charge["id"].startswith("ch_")
    assert charge["last_transaction"]["id"].startswith("txn_")
    assert charge["last_transaction"]["qr_code"]


def test_documented_simulator_success_updates_all_native_levels():
    result = run_all()["PG-PIX-003"]
    order = next(iter(result["projection"].values()))
    charge = order["charges"][0]
    assert order["status"] == charge["status"] == charge["last_transaction"]["status"] == "paid"


def test_documented_simulator_failure_is_distinct_outcome():
    result = run_all()["PG-PIX-004"]
    order = next(iter(result["projection"].values()))
    assert order["status"] == "failed"


def test_unknown_charge_retrieval_is_native_not_found_boundary():
    result = run_all()["PG-PIX-005"]
    error = result["observations"][0]["payload"]
    assert error["status"] == 404
    assert error["code"] == "charge_not_found"


def test_non_pix_payment_method_is_native_invalid_parameter_boundary():
    result = run_all()["PG-PIX-006"]
    error = result["observations"][0]["payload"]
    assert error["status"] == 400
    assert error["code"] == "invalid_parameter"


def test_missing_payments_is_native_required_parameter_boundary():
    result = run_all()["PG-PIX-007"]
    error = result["observations"][0]["payload"]
    assert error["status"] == 400
    assert error["code"] == "required_parameter"


def test_exact_threshold_is_paid_across_native_statuses():
    result = run_all()["PG-PIX-008"]
    transition = result["observations"][0]["payload"]
    assert transition["order_status"] == "paid"
    assert transition["charge_status"] == "paid"
    assert transition["transaction_status"] == "paid"


def test_oversized_order_code_is_native_invalid_parameter_boundary():
    result = run_all()["PG-PIX-009"]
    error = result["observations"][0]["payload"]
    assert error["status"] == 400
    assert error["code"] == "invalid_parameter"


def test_paid_outcome_emits_documented_sent_webhook_delivery():
    result = run_all()["PG-PIX-010"]
    delivery = result["observations"][0]["payload"]
    assert delivery["event"] == "charge.paid"
    assert delivery["status"] == "sent"
    assert delivery["attempts"] == 1
    assert delivery["response_status"] == 200


def test_failed_webhook_delivery_preserves_native_failed_state():
    result = run_all()["PG-PIX-011"]
    delivery = result["observations"][0]["payload"]
    assert delivery["event"] == "charge.payment_failed"
    assert delivery["status"] == "failed"
    assert delivery["response_status"] == 503
