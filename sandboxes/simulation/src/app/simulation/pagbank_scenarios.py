"""Scenario definitions for PagBank's first native Pix increment."""

from __future__ import annotations

from copy import deepcopy
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


SCENARIOS = {"PB-PIX-001": create_and_retrieve, "PB-PIX-002": invalid_amount, "PB-PIX-003": idempotency_conflict}


def run_all() -> dict[str, dict[str, Any]]:
    return {name: factory() for name, factory in SCENARIOS.items()}
