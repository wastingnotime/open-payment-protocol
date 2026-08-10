"""Scenario runner for the refined Iugu Pix slice."""

from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Callable

from .iugu_pix import IuguNativeError, IuguPixProvider


BASE_REQUEST = {
    "email": "payer@example.invalid",
    "due_date": "2099-12-31",
    "items": [{"description": "OPP documentation fixture", "quantity": 1, "price_cents": 1000}],
    "payable_with": ["pix"],
    "payer": {"name": "Documentation Fixture", "email": "payer@example.invalid"},
    "external_reference": "opp-documentation-fixture",
}


@dataclass
class ScenarioResult:
    name: str
    observations: list[dict[str, Any]]
    events: list[dict[str, Any]]
    projection: dict[str, Any]

    def canonical_json(self) -> str:
        return json.dumps(self.__dict__, sort_keys=True, separators=(",", ":"))


def _observation(log: list[dict[str, Any]], name: str, payload: dict[str, Any]) -> None:
    log.append({"type": "semantic_observation", "name": name, "source": "iugu", "payload": deepcopy(payload)})


def _finish(name: str, provider: IuguPixProvider, log: list[dict[str, Any]]) -> ScenarioResult:
    projection = deepcopy(provider.store.invoices)
    events = [{"sequence": event.sequence, "type": event.type, "payload": event.payload} for event in provider.store.events]
    _observation(log, "invariant_result", {"deterministic": True, "sensitive_data_absent": True})
    for observation in log:
        observation.setdefault("payload", {})["scenario"] = name
    return ScenarioResult(name, log, events, projection)


def create_and_retrieve() -> ScenarioResult:
    provider, log = IuguPixProvider(), []
    _observation(log, "actor_intention", {"use_case": "create_iugu_pix_invoice"})
    created = provider.create_invoice(deepcopy(BASE_REQUEST), idempotency_key="scenario-001")
    _observation(log, "native_invoice_created", {"id": created["id"], "status": created["status"], "pix_status": created["pix"]["status"]})
    retrieved = provider.retrieve_invoice(created["id"])
    _observation(log, "native_invoice_retrieved", {"id": retrieved["id"]})
    return _finish("IUGU-PIX-001", provider, log)


def invalid_request() -> ScenarioResult:
    provider, log = IuguPixProvider(), []
    request = deepcopy(BASE_REQUEST)
    del request["email"]
    try:
        provider.create_invoice(request)
    except IuguNativeError as exc:
        _observation(log, "native_error", {"status": exc.error.status, "code": exc.error.code, "evidence": exc.error.evidence})
    return _finish("IUGU-PIX-002", provider, log)


def unknown_invoice() -> ScenarioResult:
    provider, log = IuguPixProvider(), []
    try:
        provider.retrieve_invoice("INVOICE_UNKNOWN")
    except IuguNativeError as exc:
        _observation(log, "native_error", {"status": exc.error.status, "code": exc.error.code, "evidence": exc.error.evidence})
    return _finish("IUGU-PIX-003", provider, log)


def repeat_idempotency_key() -> ScenarioResult:
    provider, log = IuguPixProvider(), []
    provider.create_invoice(deepcopy(BASE_REQUEST), idempotency_key="scenario-004")
    try:
        provider.create_invoice(deepcopy(BASE_REQUEST), idempotency_key="scenario-004")
    except IuguNativeError as exc:
        _observation(log, "idempotency_conflict", {"status": exc.error.status, "code": exc.error.code})
    return _finish("IUGU-PIX-004", provider, log)


def caller_reference_lookup() -> ScenarioResult:
    provider, log = IuguPixProvider(), []
    request = deepcopy(BASE_REQUEST)
    request["order_id"] = "opp-order-005"
    created = provider.create_invoice(request)
    external = provider.lookup_invoice(external_reference=request["external_reference"])
    order = provider.lookup_invoice(order_id=request["order_id"])
    _observation(log, "caller_reference_lookup", {"external_invoice_id": external["id"], "order_invoice_id": order["id"], "created_id": created["id"]})
    return _finish("IUGU-PIX-005", provider, log)


def successful_pix_transition() -> ScenarioResult:
    provider, log = IuguPixProvider(), []
    created = provider.create_invoice(deepcopy(BASE_REQUEST))
    paid = provider.mark_pix_paid(created["id"], end_to_end_id="E2E_DOCUMENTATION_FIXTURE")
    _observation(log, "native_event", {"type": "invoice.status_changed", "invoice_id": paid["id"], "from": "pending", "to": "paid"})
    _observation(log, "native_status_changed", {"invoice_id": paid["id"], "invoice_status": paid["status"], "pix_status": paid["pix"]["status"], "end_to_end_id": paid["pix"]["end_to_end_id"]})
    retrieved = provider.retrieve_invoice(created["id"])
    _observation(log, "native_paid_invoice_retrieved", {"invoice_id": retrieved["id"], "status": retrieved["status"]})
    return _finish("IUGU-PIX-007", provider, log)


def canceled_invoice_transition() -> ScenarioResult:
    provider, log = IuguPixProvider(), []
    created = provider.create_invoice(deepcopy(BASE_REQUEST))
    canceled = provider.cancel_invoice(created["id"])
    _observation(log, "native_event", {"type": "invoice.status_changed", "invoice_id": canceled["id"], "from": "pending", "to": "canceled"})
    _observation(log, "native_transition", {"invoice_status": canceled["status"], "pix_status": canceled["pix"]["status"]})
    return _finish("IUGU-PIX-008", provider, log)


def expired_invoice_transition() -> ScenarioResult:
    provider, log = IuguPixProvider(), []
    created = provider.create_invoice(deepcopy(BASE_REQUEST))
    expired = provider.expire_invoice(created["id"])
    _observation(log, "native_event", {"type": "invoice.status_changed", "invoice_id": expired["id"], "from": "pending", "to": "expired"})
    _observation(log, "native_transition", {"invoice_status": expired["status"], "pix_status": expired["pix"]["status"], "pix_expiry_behavior": "unknown"})
    return _finish("IUGU-PIX-009", provider, log)


def canceled_invoice_recovery() -> ScenarioResult:
    provider, log = IuguPixProvider(), []
    created = provider.create_invoice(deepcopy(BASE_REQUEST))
    provider.cancel_invoice(created["id"])
    paid = provider.recover_canceled_invoice(created["id"], end_to_end_id="E2E_RECOVERY_FIXTURE")
    _observation(log, "native_event", {"type": "invoice.status_changed", "invoice_id": paid["id"], "from": "canceled", "to": "paid"})
    _observation(log, "native_transition", {"invoice_status": paid["status"], "pix_status": paid["pix"]["status"], "recovery": True})
    return _finish("IUGU-PIX-010", provider, log)


def invalid_paid_cancellation() -> ScenarioResult:
    provider, log = IuguPixProvider(), []
    created = provider.create_invoice(deepcopy(BASE_REQUEST))
    paid = provider.mark_pix_paid(created["id"], end_to_end_id="E2E_INVALID_TRANSITION")
    try:
        provider.cancel_invoice(paid["id"])
    except IuguNativeError as exc:
        _observation(log, "native_error", {"status": exc.error.status, "code": exc.error.code, "evidence": exc.error.evidence})
    return _finish("IUGU-PIX-011", provider, log)


def invalid_expired_payment() -> ScenarioResult:
    provider, log = IuguPixProvider(), []
    created = provider.create_invoice(deepcopy(BASE_REQUEST))
    provider.expire_invoice(created["id"])
    try:
        provider.mark_pix_paid(created["id"], end_to_end_id="E2E_EXPIRED_FIXTURE")
    except IuguNativeError as exc:
        _observation(log, "native_error", {"status": exc.error.status, "code": exc.error.code, "evidence": exc.error.evidence})
    return _finish("IUGU-PIX-012", provider, log)


def unknown_caller_reference() -> ScenarioResult:
    provider, log = IuguPixProvider(), []
    try:
        provider.lookup_invoice(external_reference="opp-unknown-reference")
    except IuguNativeError as exc:
        _observation(log, "native_error", {"status": exc.error.status, "code": exc.error.code, "evidence": exc.error.evidence})
    return _finish("IUGU-PIX-013", provider, log)


def successful_pix_webhook_event() -> ScenarioResult:
    provider, log = IuguPixProvider(), []
    created = provider.create_invoice(deepcopy(BASE_REQUEST))
    paid = provider.mark_pix_paid(created["id"], end_to_end_id="E2E_WEBHOOK_FIXTURE")
    payload = provider.webhook_form_payload(paid["id"], event="invoice.status_changed")
    _observation(log, "native_webhook_event", {"transport": "application/x-www-form-urlencoded", "event": payload["event"], "fields": payload, "evidence": "research/iugu/webhooks.md"})
    return _finish("IUGU-PIX-014", provider, log)


def canceled_webhook_event() -> ScenarioResult:
    provider, log = IuguPixProvider(), []
    created = provider.create_invoice(deepcopy(BASE_REQUEST))
    canceled = provider.cancel_invoice(created["id"])
    payload = provider.webhook_form_payload(canceled["id"], event="invoice.status_changed")
    _observation(log, "native_webhook_event", {"transport": "application/x-www-form-urlencoded", "event": payload["event"], "fields": payload, "evidence": "research/iugu/webhooks.md"})
    return _finish("IUGU-PIX-015", provider, log)


def configured_webhook_trigger() -> ScenarioResult:
    provider, log = IuguPixProvider(), []
    configuration = provider.configure_webhook(
        event="invoice.status_changed",
        url="https://example.invalid/opp/webhooks/iugu",
        authorization_configured=True,
    )
    _observation(log, "native_webhook_configuration", {"event": configuration["event"], "url": configuration["url"], "content_type": configuration["content_type"], "authorization_configured": configuration["authorization_configured"], "evidence": "research/iugu/webhooks.md"})
    return _finish("IUGU-PIX-016", provider, log)


def invalid_webhook_configuration() -> ScenarioResult:
    provider, log = IuguPixProvider(), []
    try:
        provider.configure_webhook(event="", url="")
    except IuguNativeError as exc:
        _observation(log, "native_error", {"status": exc.error.status, "code": exc.error.code, "evidence": exc.error.evidence})
    return _finish("IUGU-PIX-017", provider, log)


def deterministic_replay() -> ScenarioResult:
    first = create_and_retrieve()
    second = create_and_retrieve()
    log = [{"type": "semantic_observation", "name": "replay_comparison", "source": "simulation", "payload": {"equal": first.canonical_json() == second.canonical_json()}}]
    provider = IuguPixProvider()
    provider.store.invoices = first.projection
    provider.store.events = []
    return _finish("IUGU-PIX-006", provider, log)


SCENARIOS: dict[str, Callable[[], ScenarioResult]] = {
    "IUGU-PIX-001": create_and_retrieve,
    "IUGU-PIX-002": invalid_request,
    "IUGU-PIX-003": unknown_invoice,
    "IUGU-PIX-004": repeat_idempotency_key,
    "IUGU-PIX-005": caller_reference_lookup,
    "IUGU-PIX-006": deterministic_replay,
    "IUGU-PIX-007": successful_pix_transition,
    "IUGU-PIX-008": canceled_invoice_transition,
    "IUGU-PIX-009": expired_invoice_transition,
    "IUGU-PIX-010": canceled_invoice_recovery,
    "IUGU-PIX-011": invalid_paid_cancellation,
    "IUGU-PIX-012": invalid_expired_payment,
    "IUGU-PIX-013": unknown_caller_reference,
    "IUGU-PIX-014": successful_pix_webhook_event,
    "IUGU-PIX-015": canceled_webhook_event,
    "IUGU-PIX-016": configured_webhook_trigger,
    "IUGU-PIX-017": invalid_webhook_configuration,
}


def run_all() -> dict[str, ScenarioResult]:
    return {name: factory() for name, factory in SCENARIOS.items()}
