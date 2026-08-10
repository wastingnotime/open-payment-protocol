from copy import deepcopy

from app.simulation.pagarme import PagarmePixProvider
from app.simulation.pagarme_scenarios import BASE_REQUEST, run_all


def test_pagarme_scenarios_complete():
    results = run_all()
    assert set(results) == {"PG-PIX-001", "PG-PIX-002", "PG-PIX-003", "PG-PIX-004", "PG-PIX-005"}


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
