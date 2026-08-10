"""Mercado Pago Orders API native Pix simulation."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from decimal import Decimal
import hashlib
import hmac
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
        if not idempotency_key:
            raise MercadoPagoNativeError(MercadoPagoError(400, "required_properties", "An idempotency key is required."))
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

    def mark_pix_approved(self, order_id: str) -> dict[str, Any]:
        order = self.store.orders.get(order_id)
        if order is None:
            raise MercadoPagoNativeError(MercadoPagoError(404, "order_not_found", "The order was not found."))
        payment = order["transactions"]["payments"][0]
        if payment["status"] != "action_required":
            raise MercadoPagoNativeError(MercadoPagoError(400, "invalid_status", "The payment is not awaiting approval."))
        order["status"] = payment["status"] = "processed"
        order["status_detail"] = payment["status_detail"] = "accredited"
        payment["paid_amount"] = payment["amount"]
        self._event("payment_approved", {"order_id": order_id, "payment_id": payment["id"], "status": payment["status"]})
        return deepcopy(order)

    def cancel_unpaid_order(self, order_id: str) -> dict[str, Any]:
        order = self.store.orders.get(order_id)
        if order is None:
            raise MercadoPagoNativeError(MercadoPagoError(404, "order_not_found", "The order was not found."))
        payment = order["transactions"]["payments"][0]
        if payment["status"] != "action_required":
            raise MercadoPagoNativeError(MercadoPagoError(400, "invalid_status", "Only unpaid action-required Pix payments can be canceled."))
        order["status"] = payment["status"] = "canceled"
        order["status_detail"] = payment["status_detail"] = "canceled"
        self._event("payment_canceled", {"order_id": order_id, "payment_id": payment["id"], "status": payment["status"], "reason": "unpaid_action_required"})
        return deepcopy(order)

    def resolve_unpaid_expiration(self, order_id: str, *, outcome: str) -> dict[str, Any]:
        if outcome not in {"canceled", "expired"}:
            raise MercadoPagoNativeError(MercadoPagoError(400, "invalid_expiration_outcome", "Expiration outcome must be canceled or expired."))
        order = self.store.orders.get(order_id)
        if order is None:
            raise MercadoPagoNativeError(MercadoPagoError(404, "order_not_found", "The order was not found."))
        payment = order["transactions"]["payments"][0]
        if payment["status"] != "action_required":
            raise MercadoPagoNativeError(MercadoPagoError(400, "invalid_status", "Only unpaid action-required Pix payments can expire."))
        order["status"] = payment["status"] = outcome
        order["status_detail"] = payment["status_detail"] = "expired"
        self._event("payment_expired", {"order_id": order_id, "payment_id": payment["id"], "status": payment["status"], "documented_alternatives": ["canceled", "expired"], "manual_cancellation_available": False})
        return deepcopy(order)

    def refund_order(self, order_id: str, *, amount: str | None = None) -> dict[str, Any]:
        order = self.store.orders.get(order_id)
        if order is None:
            raise MercadoPagoNativeError(MercadoPagoError(404, "order_not_found", "The order was not found."))
        payment = order["transactions"]["payments"][0]
        if payment["status"] != "processed":
            raise MercadoPagoNativeError(MercadoPagoError(400, "invalid_status", "Only processed Pix payments can be refunded."))
        total = Decimal(payment["amount"])
        refunded = Decimal(payment.get("refunded_amount", "0.00"))
        refund_amount = total - refunded if amount is None else Decimal(amount)
        if refund_amount <= 0 or refunded + refund_amount > total:
            raise MercadoPagoNativeError(MercadoPagoError(400, "invalid_refund_amount", "Refund amount exceeds the refundable payment amount."))
        payment["refunded_amount"] = f"{refunded + refund_amount:.2f}"
        payment["status"] = "refunded" if refunded + refund_amount == total else "partially_refunded"
        order["status"] = payment["status"]
        self._event("payment_refunded", {"order_id": order_id, "payment_id": payment["id"], "amount": f"{refund_amount:.2f}", "status": payment["status"], "funds_returned_to": "payer_account", "refund_window_days": 180})
        return deepcopy(order)

    def create_async_order_variant(self, request: dict[str, Any]) -> dict[str, Any]:
        """Represent the documented asynchronous creation result variant."""
        self._validate(request)
        order_id = f"ORD_ASYNC_DOCUMENTATION_{self.store.next_id:06d}"
        self.store.next_id += 1
        order = {"id": order_id, "type": "online", "total_amount": request["total_amount"], "external_reference": request["external_reference"], "status": "processing", "transactions": {"payments": []}}
        self.store.orders[order_id] = deepcopy(order)
        self._event("order_processing", {"order_id": order_id})
        return deepcopy(order)

    def notification_payload(self, order_id: str, *, action: str = "updated") -> dict[str, Any]:
        if order_id not in self.store.orders:
            raise MercadoPagoNativeError(MercadoPagoError(404, "order_not_found", "The order was not found."))
        return {"action": action, "api_version": "v1", "application_id": "APPLICATION_DOCUMENTATION", "date_created": "2030-01-01T12:00:00Z", "id": "NOTIFICATION_DOCUMENTATION", "live_mode": False, "type": "order", "user_id": "USER_DOCUMENTATION", "data": {"id": order_id}}

    @staticmethod
    def signature(secret: str, *, data_id: str, request_id: str, timestamp: str) -> str:
        message = f"id:{data_id.lower()};request-id:{request_id};ts:{timestamp};"
        return hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()

    @classmethod
    def verify_signature(cls, secret: str, *, data_id: str, request_id: str, timestamp: str, received: str) -> bool:
        return hmac.compare_digest(received, cls.signature(secret, data_id=data_id, request_id=request_id, timestamp=timestamp))

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
