"""Pagar.me first native Pix scenario definitions."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from .pagarme import PagarmeNativeError, PagarmePixProvider


BASE_REQUEST = {"code": "opp-documentation-fixture", "items": [{"amount": 1000, "description": "OPP documentation fixture", "quantity": 1}], "payments": [{"payment_method": "pix", "pix": {"expires_in": 3600}}]}


def _result(name: str, provider: PagarmePixProvider, observations: list[dict[str, Any]]) -> dict[str, Any]:
    for item in observations:
        item.setdefault("payload", {})["scenario"] = name
    return {"name": name, "observations": observations, "events": deepcopy(provider.store.events), "projection": deepcopy(provider.store.orders)}


def create_and_retrieve_charge() -> dict[str, Any]:
    provider, observations = PagarmePixProvider(), []
    order = provider.create_order(deepcopy(BASE_REQUEST))
    charge = order["charges"][0]
    observations.append({"type": "semantic_observation", "name": "native_event", "source": "pagarme", "payload": {"type": "order.created", "order_id": order["id"], "charge_id": charge["id"]}})
    observations.append({"type": "semantic_observation", "name": "native_order_created", "source": "pagarme", "payload": {"order_id": order["id"], "charge_id": charge["id"], "transaction_id": charge["last_transaction"]["id"], "status": charge["status"]}})
    retrieved = provider.retrieve_charge(charge["id"])
    observations.append({"type": "semantic_observation", "name": "native_charge_retrieved", "source": "pagarme", "payload": {"charge_id": retrieved["id"], "qr_code": retrieved["last_transaction"]["qr_code"]}})
    return _result("PG-PIX-001", provider, observations)


def invalid_request() -> dict[str, Any]:
    provider, observations = PagarmePixProvider(), []
    try:
        provider.create_order({"items": []})
    except PagarmeNativeError as exc:
        observations.append({"type": "semantic_observation", "name": "native_error", "source": "pagarme", "payload": {"status": exc.error.status, "code": exc.error.code}})
    return _result("PG-PIX-002", provider, observations)


def simulator_success() -> dict[str, Any]:
    provider, observations = PagarmePixProvider(), []
    order = provider.create_order(deepcopy(BASE_REQUEST))
    charge = provider.simulate_pix_outcome(order["charges"][0]["id"])
    observations.append({"type": "semantic_observation", "name": "native_event", "source": "pagarme", "payload": {"type": "charge.paid", "charge_id": charge["id"], "evidence": "research/pagarme/lifecycle.md"}})
    observations.append({"type": "semantic_observation", "name": "native_transition", "source": "pagarme", "payload": {"order_status": provider.store.orders[order["id"]]["status"], "charge_status": charge["status"], "transaction_status": charge["last_transaction"]["status"]}})
    return _result("PG-PIX-003", provider, observations)


def simulator_failure() -> dict[str, Any]:
    provider, observations = PagarmePixProvider(), []
    request = deepcopy(BASE_REQUEST)
    request["items"][0]["amount"] = 60000
    order = provider.create_order(request)
    charge = provider.simulate_pix_outcome(order["charges"][0]["id"])
    observations.append({"type": "semantic_observation", "name": "native_event", "source": "pagarme", "payload": {"type": "charge.payment_failed", "charge_id": charge["id"], "evidence": "research/pagarme/lifecycle.md"}})
    observations.append({"type": "semantic_observation", "name": "native_transition", "source": "pagarme", "payload": {"order_status": provider.store.orders[order["id"]]["status"], "charge_status": charge["status"], "transaction_status": charge["last_transaction"]["status"]}})
    return _result("PG-PIX-004", provider, observations)


def unknown_charge_retrieval() -> dict[str, Any]:
    provider, observations = PagarmePixProvider(), []
    try:
        provider.retrieve_charge("ch_UNKNOWN_DOCUMENTATION")
    except PagarmeNativeError as exc:
        observations.append({"type": "semantic_observation", "name": "native_error", "source": "pagarme", "payload": {"status": exc.error.status, "code": exc.error.code}})
    return _result("PG-PIX-005", provider, observations)


def invalid_payment_method() -> dict[str, Any]:
    provider, observations = PagarmePixProvider(), []
    request = deepcopy(BASE_REQUEST)
    request["payments"][0]["payment_method"] = "credit_card"
    try:
        provider.create_order(request)
    except PagarmeNativeError as exc:
        observations.append({"type": "semantic_observation", "name": "native_error", "source": "pagarme", "payload": {"status": exc.error.status, "code": exc.error.code}})
    return _result("PG-PIX-006", provider, observations)


def missing_payments() -> dict[str, Any]:
    provider, observations = PagarmePixProvider(), []
    request = deepcopy(BASE_REQUEST)
    request.pop("payments")
    try:
        provider.create_order(request)
    except PagarmeNativeError as exc:
        observations.append({"type": "semantic_observation", "name": "native_error", "source": "pagarme", "payload": {"status": exc.error.status, "code": exc.error.code}})
    return _result("PG-PIX-007", provider, observations)


def exact_threshold_success() -> dict[str, Any]:
    provider, observations = PagarmePixProvider(), []
    request = deepcopy(BASE_REQUEST)
    request["items"][0]["amount"] = 50000
    order = provider.create_order(request)
    charge = provider.simulate_pix_outcome(order["charges"][0]["id"])
    observations.append({"type": "semantic_observation", "name": "native_transition", "source": "pagarme", "payload": {"order_status": provider.store.orders[order["id"]]["status"], "charge_status": charge["status"], "transaction_status": charge["last_transaction"]["status"]}})
    return _result("PG-PIX-008", provider, observations)


def oversized_order_code() -> dict[str, Any]:
    provider, observations = PagarmePixProvider(), []
    request = deepcopy(BASE_REQUEST)
    request["code"] = "x" * 53
    try:
        provider.create_order(request)
    except PagarmeNativeError as exc:
        observations.append({"type": "semantic_observation", "name": "native_error", "source": "pagarme", "payload": {"status": exc.error.status, "code": exc.error.code}})
    return _result("PG-PIX-009", provider, observations)


def paid_webhook_delivery() -> dict[str, Any]:
    provider, observations = PagarmePixProvider(), []
    order = provider.create_order(deepcopy(BASE_REQUEST))
    charge = provider.simulate_pix_outcome(order["charges"][0]["id"])
    delivery = provider.deliver_webhook(
        "charge.paid",
        {"charge_id": charge["id"], "order_id": order["id"], "status": charge["status"]},
    )
    observations.append({"type": "semantic_observation", "name": "native_webhook_delivery", "source": "pagarme", "payload": {"event": delivery["event"], "webhook_id": delivery["id"], "status": delivery["status"], "attempts": delivery["attempts"], "response_status": delivery["response_status"], "evidence": "research/pagarme/webhooks.md"}})
    return _result("PG-PIX-010", provider, observations)


def failed_webhook_delivery() -> dict[str, Any]:
    provider, observations = PagarmePixProvider(), []
    request = deepcopy(BASE_REQUEST)
    request["items"][0]["amount"] = 60000
    order = provider.create_order(request)
    charge = provider.simulate_pix_outcome(order["charges"][0]["id"])
    delivery = provider.deliver_webhook(
        "charge.payment_failed",
        {"charge_id": charge["id"], "order_id": order["id"], "status": charge["status"]},
        response_status=503,
    )
    observations.append({"type": "semantic_observation", "name": "native_webhook_delivery", "source": "pagarme", "payload": {"event": delivery["event"], "webhook_id": delivery["id"], "status": delivery["status"], "attempts": delivery["attempts"], "response_status": delivery["response_status"], "evidence": "research/pagarme/webhooks.md"}})
    return _result("PG-PIX-011", provider, observations)


def resent_webhook_delivery() -> dict[str, Any]:
    provider, observations = PagarmePixProvider(), []
    request = deepcopy(BASE_REQUEST)
    request["items"][0]["amount"] = 60000
    order = provider.create_order(request)
    charge = provider.simulate_pix_outcome(order["charges"][0]["id"])
    initial = provider.deliver_webhook(
        "charge.payment_failed",
        {"charge_id": charge["id"], "order_id": order["id"], "status": charge["status"]},
        response_status=503,
    )
    delivery = provider.resend_webhook(initial["id"])
    observations.append({"type": "semantic_observation", "name": "native_webhook_resent", "source": "pagarme", "payload": {"event": delivery["event"], "webhook_id": delivery["id"], "status": delivery["status"], "attempts": delivery["attempts"], "response_status": delivery["response_status"], "evidence": "research/pagarme/webhooks.md"}})
    return _result("PG-PIX-012", provider, observations)


def queried_webhook_delivery() -> dict[str, Any]:
    provider, observations = PagarmePixProvider(), []
    order = provider.create_order(deepcopy(BASE_REQUEST))
    charge = provider.simulate_pix_outcome(order["charges"][0]["id"])
    delivery = provider.deliver_webhook(
        "charge.paid",
        {"charge_id": charge["id"], "order_id": order["id"], "status": charge["status"]},
    )
    queried = provider.query_webhook(delivery["id"])
    observations.append({"type": "semantic_observation", "name": "native_webhook_queried", "source": "pagarme", "payload": {"event": queried["event"], "webhook_id": queried["id"], "status": queried["status"], "attempts": queried["attempts"], "response_status": queried["response_status"], "evidence": "research/pagarme/webhooks.md"}})
    return _result("PG-PIX-013", provider, observations)


def paid_order_webhook_delivery() -> dict[str, Any]:
    provider, observations = PagarmePixProvider(), []
    order = provider.create_order(deepcopy(BASE_REQUEST))
    provider.simulate_pix_outcome(order["charges"][0]["id"])
    delivery = provider.deliver_webhook(
        "order.paid",
        {"order_id": order["id"], "status": provider.store.orders[order["id"]]["status"]},
    )
    observations.append({"type": "semantic_observation", "name": "native_webhook_delivery", "source": "pagarme", "payload": {"event": delivery["event"], "webhook_id": delivery["id"], "status": delivery["status"], "attempts": delivery["attempts"], "response_status": delivery["response_status"], "evidence": "research/pagarme/webhooks.md"}})
    return _result("PG-PIX-014", provider, observations)


SCENARIOS = {"PG-PIX-001": create_and_retrieve_charge, "PG-PIX-002": invalid_request, "PG-PIX-003": simulator_success, "PG-PIX-004": simulator_failure, "PG-PIX-005": unknown_charge_retrieval, "PG-PIX-006": invalid_payment_method, "PG-PIX-007": missing_payments, "PG-PIX-008": exact_threshold_success, "PG-PIX-009": oversized_order_code, "PG-PIX-010": paid_webhook_delivery, "PG-PIX-011": failed_webhook_delivery, "PG-PIX-012": resent_webhook_delivery, "PG-PIX-013": queried_webhook_delivery, "PG-PIX-014": paid_order_webhook_delivery}


def run_all() -> dict[str, dict[str, Any]]:
    return {name: factory() for name, factory in SCENARIOS.items()}
