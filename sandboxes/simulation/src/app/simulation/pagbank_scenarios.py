"""Scenario definitions for PagBank's first native Pix increment."""

from __future__ import annotations

from copy import deepcopy
import json
from typing import Any

from .pagbank import PagBankNativeError, PagBankPixProvider


BASE_REQUEST = {
    "reference_id": "opp-documentation-fixture",
    "items": [{"name": "OPP documentation fixture", "quantity": 1, "unit_amount": 1000}],
    "qr_codes": [{"amount": {"value": 1000}, "expiration_date": "2030-01-01T12:00:00-03:00"}],
    "notification_urls": ["https://example.invalid/webhooks/pagbank"],
}


def _result(name: str, provider: PagBankPixProvider, observations: list[dict[str, Any]]) -> dict[str, Any]:
    for item in observations:
        item.setdefault("payload", {})["scenario"] = name
    return {"name": name, "observations": observations, "events": deepcopy(provider.store.events), "projection": deepcopy(provider.store.orders)}


def create_and_retrieve() -> dict[str, Any]:
    provider, observations = PagBankPixProvider(), []
    order = provider.create_order(deepcopy(BASE_REQUEST), idempotency_key="pagbank-scenario-001")
    observations.append({"type": "semantic_observation", "name": "native_event", "source": "pagbank", "payload": {"type": "order.created", "order_id": order["id"]}})
    observations.append({"type": "semantic_observation", "name": "native_order_created", "source": "pagbank", "payload": {"id": order["id"], "qr_id": order["qr_codes"][0]["id"], "charges": order["charges"]}})
    retrieved = provider.retrieve_order(order["id"])
    observations.append({"type": "semantic_observation", "name": "native_order_retrieved", "source": "pagbank", "payload": {"id": retrieved["id"], "qr_text": retrieved["qr_codes"][0]["text"]}})
    return _result("PB-PIX-001", provider, observations)


def invalid_amount() -> dict[str, Any]:
    provider, observations = PagBankPixProvider(), []
    request = deepcopy(BASE_REQUEST)
    request["qr_codes"][0]["amount"]["value"] = 900
    try:
        provider.create_order(request, idempotency_key="pagbank-scenario-002")
    except PagBankNativeError as exc:
        observations.append({"type": "semantic_observation", "name": "native_event", "source": "pagbank", "payload": {"type": "order.rejected", "code": exc.error.code}})
        observations.append({"type": "semantic_observation", "name": "native_error", "source": "pagbank", "payload": {"status": exc.error.status, "code": exc.error.code}})
    return _result("PB-PIX-002", provider, observations)


def idempotency_conflict() -> dict[str, Any]:
    provider, observations = PagBankPixProvider(), []
    provider.create_order(deepcopy(BASE_REQUEST), idempotency_key="pagbank-scenario-003")
    try:
        provider.create_order(deepcopy(BASE_REQUEST), idempotency_key="pagbank-scenario-003")
    except PagBankNativeError as exc:
        observations.append({"type": "semantic_observation", "name": "native_event", "source": "pagbank", "payload": {"type": "order.idempotency_conflict", "code": exc.error.code}})
        observations.append({"type": "semantic_observation", "name": "idempotency_conflict", "source": "pagbank", "payload": {"status": exc.error.status, "code": exc.error.code}})
    return _result("PB-PIX-003", provider, observations)


def charge_emerges_after_pix_payment() -> dict[str, Any]:
    provider, observations = PagBankPixProvider(), []
    order = provider.create_order(deepcopy(BASE_REQUEST), idempotency_key="pagbank-scenario-004")
    paid = provider.mark_pix_paid(order["id"], end_to_end_id="E2E_DOCUMENTATION_FIXTURE")
    charge = paid["charges"][0]
    observations.append({"type": "semantic_observation", "name": "native_event", "source": "pagbank", "payload": {"type": "charge.created", "order_id": paid["id"], "charge_id": charge["id"]}})
    observations.append({"type": "semantic_observation", "name": "native_charge_emerged", "source": "pagbank", "payload": {"charge_id": charge["id"], "status": charge["status"], "pix_end_to_end_id": charge["payment_method"]["pix"]["end_to_end_id"], "qr_still_present": bool(paid["qr_codes"])}})
    return _result("PB-PIX-004", provider, observations)


def unknown_order_retrieval() -> dict[str, Any]:
    provider, observations = PagBankPixProvider(), []
    try:
        provider.retrieve_order("ORDE_UNKNOWN_DOCUMENTATION")
    except PagBankNativeError as exc:
        observations.append({"type": "semantic_observation", "name": "native_error", "source": "pagbank", "payload": {"status": exc.error.status, "code": exc.error.code}})
    return _result("PB-PIX-005", provider, observations)


def duplicate_pix_payment() -> dict[str, Any]:
    provider, observations = PagBankPixProvider(), []
    order = provider.create_order(deepcopy(BASE_REQUEST), idempotency_key="pagbank-scenario-006")
    provider.mark_pix_paid(order["id"], end_to_end_id="E2E_DOCUMENTATION_FIXTURE")
    try:
        provider.mark_pix_paid(order["id"], end_to_end_id="E2E_DUPLICATE_FIXTURE")
    except PagBankNativeError as exc:
        observations.append({"type": "semantic_observation", "name": "native_error", "source": "pagbank", "payload": {"status": exc.error.status, "code": exc.error.code}})
    return _result("PB-PIX-006", provider, observations)


def multiple_qr_codes() -> dict[str, Any]:
    provider, observations = PagBankPixProvider(), []
    request = deepcopy(BASE_REQUEST)
    request["qr_codes"].append(deepcopy(BASE_REQUEST["qr_codes"][0]))
    try:
        provider.create_order(request, idempotency_key="pagbank-scenario-007")
    except PagBankNativeError as exc:
        observations.append({"type": "semantic_observation", "name": "native_error", "source": "pagbank", "payload": {"status": exc.error.status, "code": exc.error.code}})
    return _result("PB-PIX-007", provider, observations)


def missing_qr_codes() -> dict[str, Any]:
    provider, observations = PagBankPixProvider(), []
    request = deepcopy(BASE_REQUEST)
    request.pop("qr_codes")
    try:
        provider.create_order(request, idempotency_key="pagbank-scenario-008")
    except PagBankNativeError as exc:
        observations.append({"type": "semantic_observation", "name": "native_error", "source": "pagbank", "payload": {"status": exc.error.status, "code": exc.error.code}})
    return _result("PB-PIX-008", provider, observations)


def missing_reference_id() -> dict[str, Any]:
    provider, observations = PagBankPixProvider(), []
    request = deepcopy(BASE_REQUEST)
    request.pop("reference_id")
    try:
        provider.create_order(request, idempotency_key="pagbank-scenario-009")
    except PagBankNativeError as exc:
        observations.append({"type": "semantic_observation", "name": "native_error", "source": "pagbank", "payload": {"status": exc.error.status, "code": exc.error.code}})
    return _result("PB-PIX-009", provider, observations)


def missing_idempotency_key() -> dict[str, Any]:
    provider, observations = PagBankPixProvider(), []
    try:
        provider.create_order(deepcopy(BASE_REQUEST), idempotency_key="")
    except PagBankNativeError as exc:
        observations.append({"type": "semantic_observation", "name": "native_error", "source": "pagbank", "payload": {"status": exc.error.status, "code": exc.error.code}})
    return _result("PB-PIX-010", provider, observations)


def paid_notification_with_authenticity() -> dict[str, Any]:
    provider, observations = PagBankPixProvider(), []
    order = provider.create_order(deepcopy(BASE_REQUEST), idempotency_key="pagbank-scenario-011")
    paid = provider.mark_pix_paid(order["id"], end_to_end_id="E2E_NOTIFICATION_FIXTURE")
    payload = provider.notification_payload(paid["id"])
    raw_payload = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    token = provider.authenticity_token("ACCOUNT_TOKEN_DOCUMENTATION", raw_payload)
    observations.append({"type": "semantic_observation", "name": "native_webhook_notification", "source": "pagbank", "payload": {"transport": "https_post", "order_id": paid["id"], "charge_status": payload["charges"][0]["status"], "has_qr_code": bool(payload["qr_codes"]), "authenticity_verified": provider.verify_authenticity("ACCOUNT_TOKEN_DOCUMENTATION", raw_payload, token), "evidence": "research/pagbank/webhooks.md"}})
    return _result("PB-PIX-011", provider, observations)


def mismatched_notification_authenticity() -> dict[str, Any]:
    provider, observations = PagBankPixProvider(), []
    order = provider.create_order(deepcopy(BASE_REQUEST), idempotency_key="pagbank-scenario-012")
    paid = provider.mark_pix_paid(order["id"], end_to_end_id="E2E_NOTIFICATION_MISMATCH")
    payload = provider.notification_payload(paid["id"])
    raw_payload = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    token = provider.authenticity_token("ACCOUNT_TOKEN_DOCUMENTATION", raw_payload)
    observations.append({"type": "semantic_observation", "name": "native_webhook_rejected", "source": "pagbank", "payload": {"transport": "https_post", "order_id": paid["id"], "authenticity_verified": provider.verify_authenticity("ACCOUNT_TOKEN_DOCUMENTATION", raw_payload + " ", token), "action": "discard", "evidence": "research/pagbank/webhooks.md"}})
    return _result("PB-PIX-012", provider, observations)


def notification_url_is_preserved() -> dict[str, Any]:
    provider, observations = PagBankPixProvider(), []
    order = provider.create_order(deepcopy(BASE_REQUEST), idempotency_key="pagbank-scenario-013")
    observations.append({"type": "semantic_observation", "name": "native_notification_configuration", "source": "pagbank", "payload": {"order_id": order["id"], "notification_urls": order["notification_urls"], "transport": "https_post", "evidence": "research/pagbank/webhooks.md"}})
    return _result("PB-PIX-013", provider, observations)


def multiple_notification_urls_rejected() -> dict[str, Any]:
    provider, observations = PagBankPixProvider(), []
    request = deepcopy(BASE_REQUEST)
    request["notification_urls"].append("https://example.invalid/webhooks/pagbank-duplicate")
    try:
        provider.create_order(request, idempotency_key="pagbank-scenario-014")
    except PagBankNativeError as exc:
        observations.append({"type": "semantic_observation", "name": "native_error", "source": "pagbank", "payload": {"status": exc.error.status, "code": exc.error.code}})
    return _result("PB-PIX-014", provider, observations)


def insecure_notification_url_rejected() -> dict[str, Any]:
    provider, observations = PagBankPixProvider(), []
    request = deepcopy(BASE_REQUEST)
    request["notification_urls"] = ["http://example.invalid/webhooks/pagbank"]
    try:
        provider.create_order(request, idempotency_key="pagbank-scenario-015")
    except PagBankNativeError as exc:
        observations.append({"type": "semantic_observation", "name": "native_error", "source": "pagbank", "payload": {"status": exc.error.status, "code": exc.error.code}})
    return _result("PB-PIX-015", provider, observations)


def partial_charge_cancellation() -> dict[str, Any]:
    provider, observations = PagBankPixProvider(), []
    order = provider.create_order(deepcopy(BASE_REQUEST), idempotency_key="pagbank-scenario-016")
    paid = provider.mark_pix_paid(order["id"], end_to_end_id="E2E_PARTIAL_CANCEL")
    canceled = provider.cancel_charge(paid["id"], amount=400)
    charge = canceled["charges"][0]
    observations.append({"type": "semantic_observation", "name": "native_partial_cancellation", "source": "pagbank", "payload": {"order_id": canceled["id"], "charge_id": charge["id"], "status": charge["status"], "refunded": charge["amount"]["summary"]["refunded"], "evidence": "research/pagbank/contract.md"}})
    return _result("PB-PIX-016", provider, observations)


def full_charge_cancellation() -> dict[str, Any]:
    provider, observations = PagBankPixProvider(), []
    order = provider.create_order(deepcopy(BASE_REQUEST), idempotency_key="pagbank-scenario-017")
    paid = provider.mark_pix_paid(order["id"], end_to_end_id="E2E_FULL_CANCEL")
    canceled = provider.cancel_charge(paid["id"])
    charge = canceled["charges"][0]
    observations.append({"type": "semantic_observation", "name": "native_full_cancellation", "source": "pagbank", "payload": {"order_id": canceled["id"], "charge_id": charge["id"], "status": charge["status"], "refunded": charge["amount"]["summary"]["refunded"], "evidence": "research/pagbank/contract.md"}})
    return _result("PB-PIX-017", provider, observations)


SCENARIOS = {"PB-PIX-001": create_and_retrieve, "PB-PIX-002": invalid_amount, "PB-PIX-003": idempotency_conflict, "PB-PIX-004": charge_emerges_after_pix_payment, "PB-PIX-005": unknown_order_retrieval, "PB-PIX-006": duplicate_pix_payment, "PB-PIX-007": multiple_qr_codes, "PB-PIX-008": missing_qr_codes, "PB-PIX-009": missing_reference_id, "PB-PIX-010": missing_idempotency_key, "PB-PIX-011": paid_notification_with_authenticity, "PB-PIX-012": mismatched_notification_authenticity, "PB-PIX-013": notification_url_is_preserved, "PB-PIX-014": multiple_notification_urls_rejected, "PB-PIX-015": insecure_notification_url_rejected, "PB-PIX-016": partial_charge_cancellation, "PB-PIX-017": full_charge_cancellation}


def run_all() -> dict[str, dict[str, Any]]:
    return {name: factory() for name, factory in SCENARIOS.items()}
