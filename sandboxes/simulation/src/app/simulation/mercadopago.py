"""Mercado Pago Orders API native Pix simulation."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class MercadoPagoError:
    status: int
    code: str
    message: str
    evidence: str = "research/mercadopago/contract.md"


class MercadoPagoNativeError(Exception):
    def __init__(self, error: MercadoPagoError) -> None:
        super().__init__(error.message)
        self.error = error


@dataclass
class MercadoPagoStore:
    orders: dict[str, dict[str, Any]] = field(default_factory=dict)
    events: list[dict[str, Any]] = field(default_factory=list)
    idempotency: set[str] = field(default_factory=set)
    next_id: int = 1


class MercadoPagoPixProvider:
    """Preserves Orders API order/payment nesting and decimal-string amounts."""

    def __init__(self, store: MercadoPagoStore | None = None) -> None:
        self.store = store or MercadoPagoStore()

    def create_order(self, request: dict[str, Any], *, idempotency_key: str) -> dict[str, Any]:
        if idempotency_key in self.store.idempotency:
            self._event("order_create_rejected", {"code": "idempotency_key_already_used"})
            raise MercadoPagoNativeError(MercadoPagoError(409, "idempotency_key_already_used", "The idempotency key was already used."))
        self._validate(request)
        order_id = f"ORD_DOCUMENTATION_{self.store.next_id:06d}"
        payment_id = f"PAY_DOCUMENTATION_{self.store.next_id:06d}"
        self.store.next_id += 1
        payment = request["transactions"]["payments"][0]
        order = {
            "id": order_id,
            "type": "online",
            "total_amount": request["total_amount"],
            "external_reference": request["external_reference"],
            "country_code": "BRA",
            "status": "action_required",
            "status_detail": "waiting_transfer",
            "processing_mode": request["processing_mode"],
            "transactions": {
                "payments": [{
                    "id": payment_id,
                    "reference_id": f"reference_{self.store.next_id - 1:06d}",
                    "status": "action_required",
                    "status_detail": "waiting_transfer",
                    "amount": payment["amount"],
                    "payment_method": {
                        "id": "pix",
                        "type": "bank_transfer",
                        "ticket_url": f"https://example.invalid/pix/{order_id}",
                        "qr_code": "SANITIZED_PIX_COPY_AND_PASTE_VALUE",
                        "qr_code_base64": "SANITIZED_BASE64_VALUE",
                    },
                }]
            },
        }
        self.store.orders[order_id] = deepcopy(order)
        self.store.idempotency.add(idempotency_key)
        self._event("order_created", {"order_id": order_id, "status": order["status"]})
        return deepcopy(order)

    def retrieve_order(self, order_id: str) -> dict[str, Any]:
        order = self.store.orders.get(order_id)
        if order is None:
            self._event("order_retrieve_rejected", {"order_id": order_id})
            raise MercadoPagoNativeError(MercadoPagoError(404, "order_not_found", "The order was not found."))
        self._event("order_retrieved", {"order_id": order_id})
        return deepcopy(order)

    def _validate(self, request: dict[str, Any]) -> None:
        required = ("type", "total_amount", "external_reference", "processing_mode", "transactions", "payer")
        missing = [key for key in required if not request.get(key)]
        if missing:
            raise MercadoPagoNativeError(MercadoPagoError(400, "required_properties", f"Missing: {', '.join(missing)}"))
        payments = request["transactions"].get("payments", [])
        if len(payments) != 1 or payments[0].get("payment_method", {}).get("id") != "pix":
            raise MercadoPagoNativeError(MercadoPagoError(400, "property_value", "A single Pix payment is required."))
        if payments[0].get("amount") != request["total_amount"]:
            raise MercadoPagoNativeError(MercadoPagoError(400, "invalid_total_amount", "Total must equal payment amount."))

    def _event(self, event_type: str, payload: dict[str, Any]) -> None:
        self.store.events.append({"type": event_type, "payload": deepcopy(payload)})
