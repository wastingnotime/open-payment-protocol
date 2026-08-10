from copy import deepcopy

from app.simulation.asaas import AsaasPixProvider
from app.simulation.asaas_scenarios import BASE_REQUEST, run_all


def test_asaas_scenarios_complete():
    results = run_all()
    assert set(results) == {"AS-PIX-001", "AS-PIX-002", "AS-PIX-003"}


def test_payment_and_separate_qr_retrieval_are_preserved():
    provider = AsaasPixProvider()
    payment = provider.create_payment(deepcopy(BASE_REQUEST))
    assert payment["id"].startswith("pay_")
    assert payment["billingType"] == "PIX"
    qr = provider.retrieve_pix_qr(payment["id"])
    assert qr["payload"]


def test_unknown_payment_retrieval_is_native_not_found_boundary():
    result = run_all()["AS-PIX-003"]
    error = result["observations"][0]["payload"]
    assert error["status"] == 404
    assert error["code"] == "payment_not_found"
