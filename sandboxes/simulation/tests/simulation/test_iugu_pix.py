from app.simulation.iugu_pix import IuguNativeError, IuguPixProvider
from app.simulation.scenarios import BASE_REQUEST, SCENARIOS, run_all
from copy import deepcopy


def test_all_selected_scenarios_complete_with_native_observations():
    results = run_all()
    assert set(results) == set(SCENARIOS)
    for name, result in results.items():
        assert result.name == name
        assert result.observations[-1]["name"] == "invariant_result"
        assert result.events is not None


def test_create_and_retrieve_preserves_iugu_invoice_shape():
    provider = IuguPixProvider()
    invoice = provider.create_invoice(deepcopy(BASE_REQUEST), idempotency_key="test-1")
    assert invoice["id"].startswith("INVOICE_")
    assert invoice["total_cents"] == 1000
    assert invoice["payable_with"] == "pix"
    assert invoice["pix"]["status"] == "qr_code_created"
    assert provider.retrieve_invoice(invoice["id"]) == invoice


def test_reused_idempotency_key_is_native_conflict():
    provider = IuguPixProvider()
    provider.create_invoice(deepcopy(BASE_REQUEST), idempotency_key="test-2")
    try:
        provider.create_invoice(deepcopy(BASE_REQUEST), idempotency_key="test-2")
    except IuguNativeError as exc:
        assert exc.error.status == 409
        assert exc.error.code == "idempotency_key_reused"
    else:
        raise AssertionError("expected native idempotency conflict")


def test_replay_is_byte_stable():
    first = SCENARIOS["IUGU-PIX-001"]()
    second = SCENARIOS["IUGU-PIX-001"]()
    assert first.canonical_json() == second.canonical_json()


def test_cardholder_data_is_not_in_fixture_or_projection():
    results = run_all()
    serialized = " ".join(result.canonical_json() for result in results.values()).lower()
    assert "pan" not in serialized
    assert "cvv" not in serialized
