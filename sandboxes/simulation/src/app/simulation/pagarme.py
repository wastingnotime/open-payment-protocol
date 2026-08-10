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
    webhooks: dict[str, dict[str, Any]] = field(default_factory=dict)
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

    def simulate_pix_outcome(self, charge_id: str) -> dict[str, Any]:
        """Apply the documented Pix simulator amount threshold."""
        charge = self.store.charges.get(charge_id)
        if charge is None:
            raise PagarmeNativeError(PagarmeError(404, "charge_not_found", "The charge was not found."))
        amount = int(charge["amount"])
        outcome = "paid" if amount <= 50000 else "failed"
        charge["status"] = outcome
        charge["last_transaction"]["status"] = outcome
        for order in self.store.orders.values():
            for index, item in enumerate(order["charges"]):
                if item["id"] == charge_id:
                    order["status"] = outcome
                    order["charges"][index] = deepcopy(charge)
        self.store.events.append({"type": "charge_status_changed", "payload": {"charge_id": charge_id, "status": outcome, "evidence": "research/pagarme/lifecycle.md"}})
        return deepcopy(charge)

    def deliver_webhook(
        self,
        event: str,
        data: dict[str, Any],
        *,
        target_url: str = "https://example.invalid/opp/webhooks/pagarme",
        response_status: int = 200,
    ) -> dict[str, Any]:
        """Record one documented webhook delivery attempt.

        Retry timing, authentication, ordering, and duplicate semantics are
        intentionally not modeled because the reviewed evidence leaves them
        unknown.
        """
        status = "sent" if 200 <= response_status < 300 else "failed"
        delivery = {
            "id": f"hook_DOCUMENTATION_{len(self.store.events) + 1:06d}",
            "url": target_url,
            "event": event,
            "status": status,
            "attempts": 1,
            "last_attempt": "2030-01-01T12:00:00Z",
            "response_status": response_status,
            "response_raw": "SANITIZED_WEBHOOK_RESPONSE",
            "account": "acc_DOCUMENTATION",
            "data": deepcopy(data),
        }
        self.store.webhooks[delivery["id"]] = deepcopy(delivery)
        self.store.events.append({"type": "webhook_delivery", "payload": {"webhook_id": delivery["id"], "event": event, "status": status, "response_status": response_status, "evidence": "research/pagarme/webhooks.md"}})
        return deepcopy(delivery)

    def resend_webhook(self, webhook_id: str, *, response_status: int = 200) -> dict[str, Any]:
        """Manually resend a recorded webhook delivery."""
        delivery = self.store.webhooks.get(webhook_id)
        if delivery is None:
            raise PagarmeNativeError(PagarmeError(404, "webhook_not_found", "The webhook was not found.", "research/pagarme/webhooks.md"))
        delivery["attempts"] += 1
        delivery["status"] = "sent" if 200 <= response_status < 300 else "failed"
        delivery["last_attempt"] = "2030-01-01T12:00:01Z"
        delivery["response_status"] = response_status
        self.store.events.append({"type": "webhook_resent", "payload": {"webhook_id": webhook_id, "status": delivery["status"], "attempts": delivery["attempts"], "response_status": response_status, "evidence": "research/pagarme/webhooks.md"}})
        return deepcopy(delivery)

    def _validate(self, request: dict[str, Any]) -> None:
        if not request.get("items") or not request.get("payments"):
            raise PagarmeNativeError(PagarmeError(400, "required_parameter", "items and payments are required."))
        if request.get("code") is not None and len(request["code"]) > 52:
            raise PagarmeNativeError(PagarmeError(400, "invalid_parameter", "Order code must be at most 52 characters."))
        if request["payments"][0].get("payment_method") != "pix":
            raise PagarmeNativeError(PagarmeError(400, "invalid_parameter", "Pix payment is required."))
