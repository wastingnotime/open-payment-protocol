"""Asaas v3 native Pix payment simulation."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class AsaasError:
    status: int
    code: str
    message: str
    evidence: str = "research/asaas/contract.md"


class AsaasNativeError(Exception):
    def __init__(self, error: AsaasError) -> None:
        super().__init__(error.message)
        self.error = error


@dataclass
class AsaasStore:
    payments: dict[str, dict[str, Any]] = field(default_factory=dict)
    events: list[dict[str, Any]] = field(default_factory=list)
    next_id: int = 1


class AsaasPixProvider:
    def __init__(self, store: AsaasStore | None = None) -> None:
        self.store = store or AsaasStore()

    def create_payment(self, request: dict[str, Any]) -> dict[str, Any]:
        self._validate(request)
        payment_id = f"pay_documentation_{self.store.next_id:06d}"
        self.store.next_id += 1
        payment = {
            "object": "payment", "id": payment_id, "customer": request["customer"],
            "value": request["value"], "billingType": "PIX", "status": "PENDING",
            "dueDate": request["dueDate"], "originalDueDate": request["dueDate"],
            "externalReference": request.get("externalReference"), "deleted": False,
        }
        self.store.payments[payment_id] = deepcopy(payment)
        self.store.events.append({"type": "payment_created", "payload": {"payment_id": payment_id, "status": "PENDING"}})
        return deepcopy(payment)

    def retrieve_payment(self, payment_id: str) -> dict[str, Any]:
        payment = self.store.payments.get(payment_id)
        if payment is None:
            raise AsaasNativeError(AsaasError(404, "payment_not_found", "The payment was not found."))
        self.store.events.append({"type": "payment_retrieved", "payload": {"payment_id": payment_id}})
        return deepcopy(payment)

    def retrieve_pix_qr(self, payment_id: str) -> dict[str, Any]:
        if payment_id not in self.store.payments:
            raise AsaasNativeError(AsaasError(404, "payment_not_found", "The payment was not found."))
        self.store.events.append({"type": "pix_qr_retrieved", "payload": {"payment_id": payment_id}})
        return {"encodedImage": "BASE64_DOCUMENTATION_FIXTURE_REMOVED", "payload": "PIX_COPY_AND_PASTE_DOCUMENTATION_FIXTURE", "expirationDate": "2099-12-31 23:59:59", "description": "OPP documentation fixture"}

    def notification_payload(self, payment_id: str, *, event_id: str, event: str) -> dict[str, Any]:
        payment = self.store.payments.get(payment_id)
        if payment is None:
            raise AsaasNativeError(AsaasError(404, "payment_not_found", "The payment was not found."))
        return {"id": event_id, "event": event, "dateCreated": "2030-01-01T12:00:00Z", "account": "ACCOUNT_DOCUMENTATION", "payment": deepcopy(payment)}

    def _validate(self, request: dict[str, Any]) -> None:
        required = ("customer", "billingType", "value", "dueDate")
        missing = [key for key in required if request.get(key) in (None, "")]
        if missing:
            raise AsaasNativeError(AsaasError(400, "required_parameter", f"Missing: {', '.join(missing)}"))
        if request["billingType"] != "PIX":
            raise AsaasNativeError(AsaasError(400, "invalid_billing_type", "PIX billingType is required."))
        if float(request["value"]) <= 0:
            raise AsaasNativeError(AsaasError(400, "invalid_value", "Payment value must be positive."))
