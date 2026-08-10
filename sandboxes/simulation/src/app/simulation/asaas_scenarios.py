"""Asaas first native Pix scenario definitions."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from .asaas import AsaasNativeError, AsaasPixProvider


BASE_REQUEST = {"customer": "cus_documentation_fixture", "billingType": "PIX", "value": 100.90, "dueDate": "2099-12-31", "externalReference": "opp-documentation-fixture"}


def _result(name: str, provider: AsaasPixProvider, observations: list[dict[str, Any]]) -> dict[str, Any]:
    for item in observations:
        item.setdefault("payload", {})["scenario"] = name
    return {"name": name, "observations": observations, "events": deepcopy(provider.store.events), "projection": deepcopy(provider.store.payments)}


def create_retrieve_and_qr() -> dict[str, Any]:
    provider, observations = AsaasPixProvider(), []
    payment = provider.create_payment(deepcopy(BASE_REQUEST))
    observations.append({"type": "semantic_observation", "name": "native_event", "source": "asaas", "payload": {"type": "payment.created", "payment_id": payment["id"]}})
    observations.append({"type": "semantic_observation", "name": "native_payment_created", "source": "asaas", "payload": {"id": payment["id"], "status": payment["status"], "value": payment["value"]}})
    retrieved = provider.retrieve_payment(payment["id"])
    qr = provider.retrieve_pix_qr(payment["id"])
    observations.append({"type": "semantic_observation", "name": "native_payment_retrieved", "source": "asaas", "payload": {"id": retrieved["id"], "status": retrieved["status"]}})
    observations.append({"type": "semantic_observation", "name": "native_pix_qr_retrieved", "source": "asaas", "payload": {"payment_id": payment["id"], "payload_present": bool(qr["payload"])}})
    return _result("AS-PIX-001", provider, observations)


def invalid_request() -> dict[str, Any]:
    provider, observations = AsaasPixProvider(), []
    try:
        provider.create_payment({"customer": "cus_documentation_fixture", "billingType": "PIX", "value": 0})
    except AsaasNativeError as exc:
        observations.append({"type": "semantic_observation", "name": "native_error", "source": "asaas", "payload": {"status": exc.error.status, "code": exc.error.code}})
    return _result("AS-PIX-002", provider, observations)


def unknown_payment_retrieval() -> dict[str, Any]:
    provider, observations = AsaasPixProvider(), []
    try:
        provider.retrieve_payment("pay_unknown_documentation")
    except AsaasNativeError as exc:
        observations.append({"type": "semantic_observation", "name": "native_error", "source": "asaas", "payload": {"status": exc.error.status, "code": exc.error.code, "evidence": "research/asaas/contract.md"}})
    return _result("AS-PIX-003", provider, observations)


def unknown_qr_retrieval() -> dict[str, Any]:
    provider, observations = AsaasPixProvider(), []
    try:
        provider.retrieve_pix_qr("pay_unknown_documentation")
    except AsaasNativeError as exc:
        observations.append({"type": "semantic_observation", "name": "native_error", "source": "asaas", "payload": {"status": exc.error.status, "code": exc.error.code, "operation": "pix_qr_retrieval"}})
    return _result("AS-PIX-004", provider, observations)


def invalid_billing_type() -> dict[str, Any]:
    provider, observations = AsaasPixProvider(), []
    request = deepcopy(BASE_REQUEST)
    request["billingType"] = "CREDIT_CARD"
    try:
        provider.create_payment(request)
    except AsaasNativeError as exc:
        observations.append({"type": "semantic_observation", "name": "native_error", "source": "asaas", "payload": {"status": exc.error.status, "code": exc.error.code}})
    return _result("AS-PIX-005", provider, observations)


def non_positive_value() -> dict[str, Any]:
    provider, observations = AsaasPixProvider(), []
    request = deepcopy(BASE_REQUEST)
    request["value"] = 0
    try:
        provider.create_payment(request)
    except AsaasNativeError as exc:
        observations.append({"type": "semantic_observation", "name": "native_error", "source": "asaas", "payload": {"status": exc.error.status, "code": exc.error.code}})
    return _result("AS-PIX-006", provider, observations)


def missing_due_date() -> dict[str, Any]:
    provider, observations = AsaasPixProvider(), []
    request = deepcopy(BASE_REQUEST)
    request.pop("dueDate")
    try:
        provider.create_payment(request)
    except AsaasNativeError as exc:
        observations.append({"type": "semantic_observation", "name": "native_error", "source": "asaas", "payload": {"status": exc.error.status, "code": exc.error.code}})
    return _result("AS-PIX-007", provider, observations)


def missing_customer() -> dict[str, Any]:
    provider, observations = AsaasPixProvider(), []
    request = deepcopy(BASE_REQUEST)
    request.pop("customer")
    try:
        provider.create_payment(request)
    except AsaasNativeError as exc:
        observations.append({"type": "semantic_observation", "name": "native_error", "source": "asaas", "payload": {"status": exc.error.status, "code": exc.error.code}})
    return _result("AS-PIX-008", provider, observations)


def received_payment_notification() -> dict[str, Any]:
    provider, observations = AsaasPixProvider(), []
    payment = provider.create_payment(deepcopy(BASE_REQUEST))
    notification = provider.notification_payload(payment["id"], event_id="evt_DOCUMENTATION_RECEIVED", event="PAYMENT_RECEIVED")
    observations.append({"type": "semantic_observation", "name": "native_webhook_notification", "source": "asaas", "payload": {"transport": "https_post_json", "event_id": notification["id"], "event": notification["event"], "payment_id": notification["payment"]["id"], "persist_before_ack": True, "evidence": "research/asaas/webhooks.md"}})
    return _result("AS-PIX-009", provider, observations)


def redelivered_payment_notification() -> dict[str, Any]:
    provider, observations = AsaasPixProvider(), []
    payment = provider.create_payment(deepcopy(BASE_REQUEST))
    first = provider.notification_payload(payment["id"], event_id="evt_DOCUMENTATION_DUPLICATE", event="PAYMENT_RECEIVED")
    second = provider.notification_payload(payment["id"], event_id="evt_DOCUMENTATION_DUPLICATE", event="PAYMENT_RECEIVED")
    observations.append({"type": "semantic_observation", "name": "native_webhook_redelivery", "source": "asaas", "payload": {"event_id": first["id"], "duplicate_event_id": second["id"], "same_event_id": first["id"] == second["id"], "delivery_count": 2, "evidence": "research/asaas/webhooks.md"}})
    return _result("AS-PIX-010", provider, observations)


def overdue_payment_notification() -> dict[str, Any]:
    provider, observations = AsaasPixProvider(), []
    payment = provider.create_payment(deepcopy(BASE_REQUEST))
    notification = provider.notification_payload(payment["id"], event_id="evt_DOCUMENTATION_OVERDUE", event="PAYMENT_OVERDUE")
    observations.append({"type": "semantic_observation", "name": "native_webhook_notification", "source": "asaas", "payload": {"event_id": notification["id"], "event": notification["event"], "payment_id": notification["payment"]["id"], "payment_response_status": notification["payment"]["status"], "status_relationship": "documented_event_sequence_only", "evidence": "research/asaas/lifecycle.md"}})
    return _result("AS-PIX-011", provider, observations)


def invalid_notification_envelope() -> dict[str, Any]:
    provider, observations = AsaasPixProvider(), []
    payment = provider.create_payment(deepcopy(BASE_REQUEST))
    try:
        provider.notification_payload(payment["id"], event_id="", event="")
    except AsaasNativeError as exc:
        observations.append({"type": "semantic_observation", "name": "native_error", "source": "asaas", "payload": {"status": exc.error.status, "code": exc.error.code}})
    return _result("AS-PIX-012", provider, observations)


SCENARIOS = {"AS-PIX-001": create_retrieve_and_qr, "AS-PIX-002": invalid_request, "AS-PIX-003": unknown_payment_retrieval, "AS-PIX-004": unknown_qr_retrieval, "AS-PIX-005": invalid_billing_type, "AS-PIX-006": non_positive_value, "AS-PIX-007": missing_due_date, "AS-PIX-008": missing_customer, "AS-PIX-009": received_payment_notification, "AS-PIX-010": redelivered_payment_notification, "AS-PIX-011": overdue_payment_notification, "AS-PIX-012": invalid_notification_envelope}


def run_all() -> dict[str, dict[str, Any]]:
    return {name: factory() for name, factory in SCENARIOS.items()}
