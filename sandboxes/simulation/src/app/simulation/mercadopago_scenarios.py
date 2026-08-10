"""Scenario definitions for Mercado Pago's first native Pix increment."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from .mercadopago import MercadoPagoNativeError, MercadoPagoPixProvider


BASE_REQUEST = {
    "type": "online",
    "total_amount": "50.00",
    "external_reference": "opp_documentation_fixture",
    "processing_mode": "automatic",
    "transactions": {"payments": [{"amount": "50.00", "payment_method": {"id": "pix", "type": "bank_transfer"}, "expiration_time": "PT1H"}]},
    "payer": {"email": "payer@example.invalid"},
}


def _result(name: str, provider: MercadoPagoPixProvider, observations: list[dict[str, Any]]) -> dict[str, Any]:
    for item in observations:
        item.setdefault("payload", {})["scenario"] = name
    return {"name": name, "observations": observations, "events": deepcopy(provider.store.events), "projection": deepcopy(provider.store.orders)}


def create_and_retrieve() -> dict[str, Any]:
    provider, observations = MercadoPagoPixProvider(), []
    order = provider.create_order(deepcopy(BASE_REQUEST), idempotency_key="mp-scenario-001")
    observations.append({"type": "semantic_observation", "name": "native_event", "source": "mercadopago", "payload": {"type": "order.created", "order_id": order["id"]}})
    observations.append({"type": "semantic_observation", "name": "native_order_created", "source": "mercadopago", "payload": {"id": order["id"], "status": order["status"], "status_detail": order["status_detail"], "amount": order["total_amount"]}})
    retrieved = provider.retrieve_order(order["id"])
    observations.append({"type": "semantic_observation", "name": "native_order_retrieved", "source": "mercadopago", "payload": {"id": retrieved["id"], "payment_id": retrieved["transactions"]["payments"][0]["id"]}})
    return _result("MP-PIX-001", provider, observations)


def invalid_total() -> dict[str, Any]:
    provider, observations = MercadoPagoPixProvider(), []
    request = deepcopy(BASE_REQUEST)
    request["transactions"]["payments"][0]["amount"] = "40.00"
    try:
        provider.create_order(request, idempotency_key="mp-scenario-002")
    except MercadoPagoNativeError as exc:
        observations.append({"type": "semantic_observation", "name": "native_event", "source": "mercadopago", "payload": {"type": "order.rejected", "code": exc.error.code}})
        observations.append({"type": "semantic_observation", "name": "native_error", "source": "mercadopago", "payload": {"status": exc.error.status, "code": exc.error.code}})
    return _result("MP-PIX-002", provider, observations)


def idempotency_conflict() -> dict[str, Any]:
    provider, observations = MercadoPagoPixProvider(), []
    provider.create_order(deepcopy(BASE_REQUEST), idempotency_key="mp-scenario-003")
    try:
        provider.create_order(deepcopy(BASE_REQUEST), idempotency_key="mp-scenario-003")
    except MercadoPagoNativeError as exc:
        observations.append({"type": "semantic_observation", "name": "native_event", "source": "mercadopago", "payload": {"type": "order.idempotency_conflict", "code": exc.error.code}})
        observations.append({"type": "semantic_observation", "name": "idempotency_conflict", "source": "mercadopago", "payload": {"status": exc.error.status, "code": exc.error.code}})
    return _result("MP-PIX-003", provider, observations)


def asynchronous_processing_variant() -> dict[str, Any]:
    provider, observations = MercadoPagoPixProvider(), []
    order = provider.create_async_order_variant(deepcopy(BASE_REQUEST))
    observations.append({"type": "semantic_observation", "name": "native_event", "source": "mercadopago", "payload": {"type": "order.processing", "order_id": order["id"], "evidence": "research/mercadopago/contract.md"}})
    observations.append({"type": "semantic_observation", "name": "native_async_result", "source": "mercadopago", "payload": {"order_id": order["id"], "status": order["status"], "payments_present": bool(order["transactions"]["payments"]), "reconciliation": "webhook_or_get"}})
    return _result("MP-PIX-004", provider, observations)


def asynchronous_reconciliation_get() -> dict[str, Any]:
    provider, observations = MercadoPagoPixProvider(), []
    created = provider.create_async_order_variant(deepcopy(BASE_REQUEST))
    retrieved = provider.retrieve_order(created["id"])
    observations.append({"type": "semantic_observation", "name": "native_reconciliation_query", "source": "mercadopago", "payload": {"order_id": retrieved["id"], "status": retrieved["status"], "payments_present": bool(retrieved["transactions"]["payments"]), "reconciliation": "get"}})
    return _result("MP-PIX-005", provider, observations)


def unknown_order_retrieval() -> dict[str, Any]:
    provider, observations = MercadoPagoPixProvider(), []
    try:
        provider.retrieve_order("ORD_UNKNOWN_DOCUMENTATION")
    except MercadoPagoNativeError as exc:
        observations.append({"type": "semantic_observation", "name": "native_error", "source": "mercadopago", "payload": {"status": exc.error.status, "code": exc.error.code}})
    return _result("MP-PIX-006", provider, observations)


def non_pix_payment_method() -> dict[str, Any]:
    provider, observations = MercadoPagoPixProvider(), []
    request = deepcopy(BASE_REQUEST)
    request["transactions"]["payments"][0]["payment_method"]["id"] = "card"
    try:
        provider.create_order(request, idempotency_key="mp-scenario-007")
    except MercadoPagoNativeError as exc:
        observations.append({"type": "semantic_observation", "name": "native_error", "source": "mercadopago", "payload": {"status": exc.error.status, "code": exc.error.code}})
    return _result("MP-PIX-007", provider, observations)


def missing_payer() -> dict[str, Any]:
    provider, observations = MercadoPagoPixProvider(), []
    request = deepcopy(BASE_REQUEST)
    request.pop("payer")
    try:
        provider.create_order(request, idempotency_key="mp-scenario-008")
    except MercadoPagoNativeError as exc:
        observations.append({"type": "semantic_observation", "name": "native_error", "source": "mercadopago", "payload": {"status": exc.error.status, "code": exc.error.code}})
    return _result("MP-PIX-008", provider, observations)


def multiple_payments() -> dict[str, Any]:
    provider, observations = MercadoPagoPixProvider(), []
    request = deepcopy(BASE_REQUEST)
    request["transactions"]["payments"].append(deepcopy(BASE_REQUEST["transactions"]["payments"][0]))
    try:
        provider.create_order(request, idempotency_key="mp-scenario-009")
    except MercadoPagoNativeError as exc:
        observations.append({"type": "semantic_observation", "name": "native_error", "source": "mercadopago", "payload": {"status": exc.error.status, "code": exc.error.code}})
    return _result("MP-PIX-009", provider, observations)


SCENARIOS = {"MP-PIX-001": create_and_retrieve, "MP-PIX-002": invalid_total, "MP-PIX-003": idempotency_conflict, "MP-PIX-004": asynchronous_processing_variant, "MP-PIX-005": asynchronous_reconciliation_get, "MP-PIX-006": unknown_order_retrieval, "MP-PIX-007": non_pix_payment_method, "MP-PIX-008": missing_payer, "MP-PIX-009": multiple_payments}


def run_all() -> dict[str, dict[str, Any]]:
    return {name: factory() for name, factory in SCENARIOS.items()}
