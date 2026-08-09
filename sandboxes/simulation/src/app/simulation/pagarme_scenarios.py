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


SCENARIOS = {"PG-PIX-001": create_and_retrieve_charge, "PG-PIX-002": invalid_request}


def run_all() -> dict[str, dict[str, Any]]:
    return {name: factory() for name, factory in SCENARIOS.items()}
