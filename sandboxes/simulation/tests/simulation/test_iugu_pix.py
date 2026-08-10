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


def test_documented_pix_success_transition_preserves_distinct_statuses():
    provider = IuguPixProvider()
    invoice = provider.create_invoice(deepcopy(BASE_REQUEST))
    paid = provider.mark_pix_paid(invoice["id"], end_to_end_id="E2E_DOCUMENTATION_FIXTURE")
    assert paid["status"] == "paid"
    assert paid["pix"]["status"] == "paid"
    assert paid["pix"]["payment_method"] == "iugu_pix"
    assert paid["total_paid_cents"] == 1000


def test_success_scenario_exposes_native_status_changed_event():
    result = SCENARIOS["IUGU-PIX-007"]()
    events = [item for item in result.observations if item["name"] == "native_event"]
    assert events == [
        {
            "type": "semantic_observation",
            "name": "native_event",
            "source": "iugu",
            "payload": {
                "type": "invoice.status_changed",
                "invoice_id": "INVOICE_000001",
                "from": "pending",
                "to": "paid",
                "scenario": "IUGU-PIX-007",
            },
        }
    ]


def test_documented_pending_to_canceled_transition_preserves_pix_state():
    result = SCENARIOS["IUGU-PIX-008"]()
    transition = next(item for item in result.observations if item["name"] == "native_transition")
    assert transition["payload"]["invoice_status"] == "canceled"
    assert transition["payload"]["pix_status"] == "qr_code_created"


def test_documented_pending_to_expired_keeps_pix_expiry_unknown():
    result = SCENARIOS["IUGU-PIX-009"]()
    transition = next(item for item in result.observations if item["name"] == "native_transition")
    assert transition["payload"]["invoice_status"] == "expired"
    assert transition["payload"]["pix_expiry_behavior"] == "unknown"


def test_documented_canceled_to_paid_recovery_is_preserved():
    result = SCENARIOS["IUGU-PIX-010"]()
    transition = next(item for item in result.observations if item["name"] == "native_transition")
    assert transition["payload"]["invoice_status"] == "paid"
    assert transition["payload"]["recovery"] is True


def test_paid_invoice_cancellation_is_native_invalid_transition():
    result = SCENARIOS["IUGU-PIX-011"]()
    error = next(item for item in result.observations if item["name"] == "native_error")
    assert error["payload"]["status"] == 422
    assert error["payload"]["code"] == "invalid_transition"


def test_expired_invoice_payment_is_native_invalid_transition():
    result = SCENARIOS["IUGU-PIX-012"]()
    error = next(item for item in result.observations if item["name"] == "native_error")
    assert error["payload"]["status"] == 422
    assert error["payload"]["code"] == "invalid_transition"


def test_unknown_caller_reference_is_native_not_found_boundary():
    result = SCENARIOS["IUGU-PIX-013"]()
    error = next(item for item in result.observations if item["name"] == "native_error")
    assert error["payload"]["status"] == 404
    assert error["payload"]["code"] == "invoice_not_found"
