from copy import deepcopy
import json

from app.simulation.asaas import AsaasNativeError, AsaasPixProvider
from app.simulation.asaas_scenarios import BASE_REQUEST, run_all


def test_asaas_scenarios_complete():
    results = run_all()
    assert set(results) == {f"AS-PIX-{number:03d}" for number in range(1, 13)}


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


def test_unknown_qr_retrieval_keeps_operation_boundary():
    result = run_all()["AS-PIX-004"]
    error = result["observations"][0]["payload"]
    assert error["status"] == 404
    assert error["operation"] == "pix_qr_retrieval"


def test_non_pix_billing_type_is_native_invalid_boundary():
    result = run_all()["AS-PIX-005"]
    error = result["observations"][0]["payload"]
    assert error["status"] == 400
    assert error["code"] == "invalid_billing_type"


def test_non_positive_value_is_native_invalid_value_boundary():
    result = run_all()["AS-PIX-006"]
    error = result["observations"][0]["payload"]
    assert error["status"] == 400
    assert error["code"] == "invalid_value"


def test_missing_due_date_is_native_required_parameter_boundary():
    result = run_all()["AS-PIX-007"]
    error = result["observations"][0]["payload"]
    assert error["status"] == 400
    assert error["code"] == "required_parameter"


def test_missing_customer_is_native_required_parameter_boundary():
    result = run_all()["AS-PIX-008"]
    error = result["observations"][0]["payload"]
    assert error["status"] == 400
    assert error["code"] == "required_parameter"


def test_received_payment_notification_preserves_event_identity_and_ack_boundary():
    result = run_all()["AS-PIX-009"]
    notification = result["observations"][0]["payload"]
    assert notification["event"] == "PAYMENT_RECEIVED"
    assert notification["event_id"] == "evt_DOCUMENTATION_RECEIVED"
    assert notification["persist_before_ack"] is True


def test_asaas_redelivery_preserves_same_event_identity():
    result = run_all()["AS-PIX-010"]
    notification = result["observations"][0]["payload"]
    assert notification["same_event_id"] is True
    assert notification["delivery_count"] == 2


def test_overdue_notification_does_not_infer_response_status_transition():
    result = run_all()["AS-PIX-011"]
    notification = result["observations"][0]["payload"]
    assert notification["event"] == "PAYMENT_OVERDUE"
    assert notification["status_relationship"] == "documented_event_sequence_only"


def test_notification_envelope_requires_event_identity_fields():
    result = run_all()["AS-PIX-012"]
    error = result["observations"][0]["payload"]
    assert error["status"] == 400
    assert error["code"] == "required_parameter"


def test_asaas_notification_envelope_contains_complete_payment_object():
    provider = AsaasPixProvider()
    payment = provider.create_payment(deepcopy(BASE_REQUEST))
    notification = provider.notification_payload(payment["id"], event_id="evt_COMPLETE", event="PAYMENT_RECEIVED")
    assert notification["payment"]["id"] == payment["id"]
    assert notification["payment"]["billingType"] == "PIX"


def test_asaas_notification_report_does_not_expose_account_identity_secret():
    result = run_all()["AS-PIX-009"]
    assert "ACCOUNT_DOCUMENTATION" not in json.dumps(result, sort_keys=True)


def test_asaas_authentication_accepts_sanitized_documentation_token():
    assert AsaasPixProvider.authenticate("ACCESS_TOKEN_DOCUMENTATION")["status"] == "authenticated"


def test_asaas_authentication_preserves_missing_token_code():
    try:
        AsaasPixProvider.authenticate(None)
    except AsaasNativeError as exc:
        assert exc.error.status == 401
        assert exc.error.code == "access_token_not_found"
    else:
        raise AssertionError("expected missing token rejection")


def test_asaas_authentication_preserves_invalid_environment_code():
    try:
        AsaasPixProvider.authenticate("ACCESS_TOKEN_DOCUMENTATION", environment="unknown")
    except AsaasNativeError as exc:
        assert exc.error.code == "invalid_environment"
    else:
        raise AssertionError("expected invalid environment rejection")
