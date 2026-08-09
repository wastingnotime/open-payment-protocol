from copy import deepcopy

from app.simulation.pagarme import PagarmePixProvider
from app.simulation.pagarme_scenarios import BASE_REQUEST, run_all


def test_pagarme_scenarios_complete():
    results = run_all()
    assert set(results) == {"PG-PIX-001", "PG-PIX-002"}


def test_order_charge_transaction_hierarchy_is_preserved():
    order = PagarmePixProvider().create_order(deepcopy(BASE_REQUEST))
    charge = order["charges"][0]
    assert order["id"].startswith("or_")
    assert charge["id"].startswith("ch_")
    assert charge["last_transaction"]["id"].startswith("txn_")
    assert charge["last_transaction"]["qr_code"]
