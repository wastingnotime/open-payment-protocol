"""Pagar.me Core API native Pix order simulation."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class PagarmeError:
    status: int
    code: str
    message: str
    evidence: str = "research/pagarme/contract.md"


class PagarmeNativeError(Exception):
    def __init__(self, error: PagarmeError) -> None:
        super().__init__(error.message)
        self.error = error


@dataclass
class PagarmeStore:
    orders: dict[str, dict[str, Any]] = field(default_factory=dict)
    charges: dict[str, dict[str, Any]] = field(default_factory=dict)
    events: list[dict[str, Any]] = field(default_factory=list)
    next_id: int = 1


class PagarmePixProvider:
    def __init__(self, store: PagarmeStore | None = None) -> None:
        self.store = store or PagarmeStore()

    def create_order(self, request: dict[str, Any]) -> dict[str, Any]:
        self._validate(request)
        number = self.store.next_id
        self.store.next_id += 1
        order_id, charge_id, transaction_id = (f"{prefix}_DOCUMENTATION_{number:06d}" for prefix in ("or", "ch", "txn"))
        item = request["items"][0]
        transaction = {
            "id": transaction_id,
            "amount": item["amount"],
            "status": "pending",
            "qr_code": "SANITIZED_PIX_COPY_AND_PASTE_VALUE",
            "qr_code_url": "https://example.invalid/pix/qr-code",
            "expires_at": "2030-01-01T12:00:00Z",
        }
        charge = {"id": charge_id, "status": "pending", "amount": item["amount"], "last_transaction": transaction}
        order = {"id": order_id, "code": request.get("code"), "status": "pending", "items": deepcopy(request["items"]), "charges": [charge]}
        self.store.orders[order_id] = deepcopy(order)
        self.store.charges[charge_id] = deepcopy(charge)
        self.store.events.append({"type": "order_created", "payload": {"order_id": order_id, "charge_id": charge_id, "transaction_id": transaction_id}})
        return deepcopy(order)

    def retrieve_charge(self, charge_id: str) -> dict[str, Any]:
        charge = self.store.charges.get(charge_id)
        if charge is None:
            raise PagarmeNativeError(PagarmeError(404, "charge_not_found", "The charge was not found."))
        self.store.events.append({"type": "charge_retrieved", "payload": {"charge_id": charge_id}})
        return deepcopy(charge)

    def _validate(self, request: dict[str, Any]) -> None:
        if not request.get("items") or not request.get("payments"):
            raise PagarmeNativeError(PagarmeError(400, "required_parameter", "items and payments are required."))
        if request["payments"][0].get("payment_method") != "pix":
            raise PagarmeNativeError(PagarmeError(400, "invalid_parameter", "Pix payment is required."))
