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


SCENARIOS = {"AS-PIX-001": create_retrieve_and_qr, "AS-PIX-002": invalid_request, "AS-PIX-003": unknown_payment_retrieval, "AS-PIX-004": unknown_qr_retrieval}


def run_all() -> dict[str, dict[str, Any]]:
    return {name: factory() for name, factory in SCENARIOS.items()}
