"""PagBank Orders API native Pix QR simulation."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class PagBankError:
    status: int
    code: str
    message: str
    evidence: str = "research/pagbank/contract.md"


class PagBankNativeError(Exception):
    def __init__(self, error: PagBankError) -> None:
        super().__init__(error.message)
        self.error = error


@dataclass
class PagBankStore:
    orders: dict[str, dict[str, Any]] = field(default_factory=dict)
    events: list[dict[str, Any]] = field(default_factory=list)
    idempotency: dict[str, str] = field(default_factory=dict)
    next_id: int = 1


class PagBankPixProvider:
    """Preserves a QR-first order with an empty charge collection."""

    def __init__(self, store: PagBankStore | None = None) -> None:
        self.store = store or PagBankStore()

    def create_order(self, request: dict[str, Any], *, idempotency_key: str) -> dict[str, Any]:
        if idempotency_key in self.store.idempotency:
            self._event("order_create_rejected", {"code": "idempotency_key_in_use"})
            raise PagBankNativeError(PagBankError(409, "idempotency_key_in_use", "The idempotency key is already in use."))
        self._validate(request)
        number = self.store.next_id
        self.store.next_id += 1
        order_id = f"ORDE_DOCUMENTATION_{number:06d}"
        qr_id = f"QRCO_DOCUMENTATION_{number:06d}"
        value = request["qr_codes"][0]["amount"]["value"]
        order = {
            "id": order_id,
            "reference_id": request["reference_id"],
            "items": deepcopy(request["items"]),
            "qr_codes": [{
                "id": qr_id,
                "expiration_date": request["qr_codes"][0].get("expiration_date"),
                "amount": {"value": value},
                "text": "SANITIZED_PIX_COPY_AND_PASTE_VALUE",
                "links": [
                    {"rel": "QRCODE.PNG", "href": f"https://example.invalid/qrcode/{qr_id}/png", "media": "image/png", "type": "GET"},
                    {"rel": "QRCODE.BASE64", "href": f"https://example.invalid/qrcode/{qr_id}/base64", "media": "text/plain", "type": "GET"},
                ],
            }],
            "charges": [],
        }
        self.store.orders[order_id] = deepcopy(order)
        self.store.idempotency[idempotency_key] = order_id
        self._event("order_created", {"order_id": order_id, "charges": 0})
        return deepcopy(order)

    def retrieve_order(self, order_id: str) -> dict[str, Any]:
        order = self.store.orders.get(order_id)
        if order is None:
            self._event("order_retrieve_rejected", {"order_id": order_id})
            raise PagBankNativeError(PagBankError(404, "order_not_found", "The order was not found."))
        self._event("order_retrieved", {"order_id": order_id})
        return deepcopy(order)

    def _validate(self, request: dict[str, Any]) -> None:
        required = ("reference_id", "items", "qr_codes")
        missing = [key for key in required if not request.get(key)]
        if missing:
            raise PagBankNativeError(PagBankError(400, "required_parameter", f"Missing: {', '.join(missing)}"))
        if len(request["qr_codes"]) != 1:
            raise PagBankNativeError(PagBankError(400, "invalid_parameter", "Only one QR Code is supported per order."))
        qr = request["qr_codes"][0]
        value = qr.get("amount", {}).get("value", 0)
        item_total = sum(int(item.get("unit_amount", 0)) * int(item.get("quantity", 1)) for item in request["items"])
        if int(value) <= 0 or int(value) != item_total:
            raise PagBankNativeError(PagBankError(400, "invalid_amount", "QR amount must match positive item total."))

    def _event(self, event_type: str, payload: dict[str, Any]) -> None:
        self.store.events.append({"type": event_type, "payload": deepcopy(payload)})
