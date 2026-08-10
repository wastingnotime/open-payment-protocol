"""Iugu-native Pix invoice simulation.

This module intentionally models an Iugu invoice, not a normalized payment.
The behavior is limited to the documented first slice in
``research/iugu/contract.md``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from copy import deepcopy
from typing import Any


@dataclass(frozen=True)
class NativeError:
    status: int
    code: str
    message: str
    evidence: str


class IuguNativeError(Exception):
    def __init__(self, error: NativeError) -> None:
        super().__init__(error.message)
        self.error = error


@dataclass(frozen=True)
class Event:
    sequence: int
    type: str
    payload: dict[str, Any]


@dataclass
class IuguInvoiceStore:
    invoices: dict[str, dict[str, Any]] = field(default_factory=dict)
    events: list[Event] = field(default_factory=list)
    idempotency: dict[str, str] = field(default_factory=dict)
    webhook_configurations: list[dict[str, Any]] = field(default_factory=list)
    next_id: int = 1

    def append(self, event_type: str, payload: dict[str, Any]) -> Event:
        event = Event(len(self.events) + 1, event_type, deepcopy(payload))
        self.events.append(event)
        return event


class IuguPixProvider:
    """A deterministic fake preserving the documented Iugu native shape."""

    evidence = "research/iugu/contract.md"

    def __init__(self, store: IuguInvoiceStore | None = None) -> None:
        self.store = store or IuguInvoiceStore()

    def create_invoice(
        self, request: dict[str, Any], *, idempotency_key: str | None = None
    ) -> dict[str, Any]:
        if idempotency_key is not None and idempotency_key in self.store.idempotency:
            error = NativeError(
                409,
                "idempotency_key_reused",
                "The Idempotency-Key was already processed.",
                "research/iugu/contract.md#idempotency",
            )
            self.store.append("invoice_create_rejected", {"reason": error.code})
            raise IuguNativeError(error)

        self._validate(request)
        invoice_id = f"INVOICE_{self.store.next_id:06d}"
        self.store.next_id += 1
        item = request["items"][0]
        price_cents = sum(
            int(entry["price_cents"]) * int(entry.get("quantity", 1))
            for entry in request["items"]
        )
        external_reference = request.get("external_reference")
        order_id = request.get("order_id")
        response = {
            "id": invoice_id,
            "due_date": request["due_date"],
            "currency": "BRL",
            "email": request["email"],
            "items_total_cents": price_cents,
            "status": "pending",
            "total_cents": price_cents,
            "total_paid_cents": 0,
            "payable_with": "pix",
            "external_reference": external_reference,
            "order_id": order_id,
            "secure_id": f"{invoice_id.lower()}-secure-id",
            "secure_url": f"https://checkout.iugu.com/invoices/{invoice_id.lower()}",
            "pix": {
                "qrcode": f"https://faturas.iugu.com/qr_code/{invoice_id.lower()}",
                "qrcode_text": f"PIX_COPY_AND_PASTE_{invoice_id}",
                "status": "qr_code_created",
                "payer_cpf_cnpj": None,
                "payer_name": None,
                "end_to_end_id": None,
                "end_to_end_refund_id": None,
                "account_number_last_digits": None,
            },
            "items": [
                {
                    "id": f"ITEM_{self.store.next_id - 1:06d}_{index}",
                    "description": entry["description"],
                    "price_cents": int(entry["price_cents"]),
                    "quantity": int(entry.get("quantity", 1)),
                }
                for index, entry in enumerate(request["items"], start=1)
            ],
        }
        self.store.invoices[invoice_id] = deepcopy(response)
        if idempotency_key is not None:
            self.store.idempotency[idempotency_key] = invoice_id
        self.store.append("invoice_created", {"invoice_id": invoice_id, "status": "pending"})
        return deepcopy(response)

    def retrieve_invoice(self, invoice_id: str) -> dict[str, Any]:
        response = self.store.invoices.get(invoice_id)
        if response is None:
            error = NativeError(
                404,
                "invoice_not_found",
                "The invoice was not found.",
                "research/iugu/contract.md#retrieval",
            )
            self.store.append("invoice_retrieve_rejected", {"invoice_id": invoice_id})
            raise IuguNativeError(error)
        self.store.append("invoice_retrieved", {"invoice_id": invoice_id})
        return deepcopy(response)

    def lookup_invoice(self, *, external_reference: str | None = None, order_id: str | None = None) -> dict[str, Any]:
        matches = [
            invoice
            for invoice in self.store.invoices.values()
            if (external_reference is not None and invoice.get("external_reference") == external_reference)
            or (order_id is not None and invoice.get("order_id") == order_id)
        ]
        if not matches:
            error = NativeError(
                404,
                "invoice_not_found",
                "No invoice matched the caller reference.",
                "research/iugu/contract.md#caller-references",
            )
            self.store.append("invoice_lookup_rejected", {"external_reference": external_reference, "order_id": order_id})
            raise IuguNativeError(error)
        self.store.append("invoice_lookup_succeeded", {"invoice_id": matches[0]["id"]})
        return deepcopy(matches[0])

    def mark_pix_paid(self, invoice_id: str, *, end_to_end_id: str) -> dict[str, Any]:
        """Apply the documented Pix success transition and emit its event."""
        response = self.store.invoices.get(invoice_id)
        if response is None:
            raise IuguNativeError(NativeError(404, "invoice_not_found", "The invoice was not found.", self.evidence))
        if response["status"] != "pending" or response["pix"]["status"] != "qr_code_created":
            raise IuguNativeError(NativeError(422, "invalid_transition", "Invoice is not pending Pix payment.", "research/iugu/lifecycle.md"))
        response["status"] = "paid"
        response["total_paid_cents"] = response["total_cents"]
        response["pix"]["status"] = "paid"
        response["pix"]["payment_method"] = "iugu_pix"
        response["pix"]["end_to_end_id"] = end_to_end_id
        self.store.append("invoice_status_changed", {"invoice_id": invoice_id, "from": "pending", "to": "paid"})
        return deepcopy(response)

    def cancel_invoice(self, invoice_id: str) -> dict[str, Any]:
        response = self.store.invoices.get(invoice_id)
        if response is None:
            raise IuguNativeError(NativeError(404, "invoice_not_found", "The invoice was not found.", self.evidence))
        if response["status"] != "pending":
            raise IuguNativeError(NativeError(422, "invalid_transition", "Invoice is not pending.", "research/iugu/lifecycle.md"))
        response["status"] = "canceled"
        self.store.append("invoice_status_changed", {"invoice_id": invoice_id, "from": "pending", "to": "canceled"})
        return deepcopy(response)

    def expire_invoice(self, invoice_id: str) -> dict[str, Any]:
        response = self.store.invoices.get(invoice_id)
        if response is None:
            raise IuguNativeError(NativeError(404, "invoice_not_found", "The invoice was not found.", self.evidence))
        if response["status"] != "pending":
            raise IuguNativeError(NativeError(422, "invalid_transition", "Invoice is not pending.", "research/iugu/lifecycle.md"))
        response["status"] = "expired"
        self.store.append("invoice_status_changed", {"invoice_id": invoice_id, "from": "pending", "to": "expired"})
        return deepcopy(response)

    def recover_canceled_invoice(self, invoice_id: str, *, end_to_end_id: str) -> dict[str, Any]:
        response = self.store.invoices.get(invoice_id)
        if response is None:
            raise IuguNativeError(NativeError(404, "invoice_not_found", "The invoice was not found.", self.evidence))
        if response["status"] != "canceled":
            raise IuguNativeError(NativeError(422, "invalid_transition", "Invoice is not canceled.", "research/iugu/lifecycle.md"))
        response["status"] = "paid"
        response["total_paid_cents"] = response["total_cents"]
        response["pix"]["status"] = "paid"
        response["pix"]["payment_method"] = "iugu_pix"
        response["pix"]["end_to_end_id"] = end_to_end_id
        self.store.append("invoice_status_changed", {"invoice_id": invoice_id, "from": "canceled", "to": "paid"})
        return deepcopy(response)

    def webhook_form_payload(self, invoice_id: str, *, event: str) -> dict[str, str]:
        """Build the documented form-urlencoded invoice event fields."""
        invoice = self.store.invoices.get(invoice_id)
        if invoice is None:
            raise IuguNativeError(NativeError(404, "invoice_not_found", "The invoice was not found.", self.evidence))
        payload = {
            "event": event,
            "invoice_id": invoice["id"],
            "account_id": "ACCOUNT_DOCUMENTATION",
            "status": invoice["status"],
            "source": "API",
            "order_id": invoice.get("order_id") or "",
            "external_reference": invoice.get("external_reference") or "",
            "payment_method": invoice.get("payable_with") or "",
        }
        if invoice["status"] == "paid":
            payload["paid_cents"] = str(invoice["total_paid_cents"])
            payload["pix_end_to_end_id"] = invoice["pix"].get("end_to_end_id") or ""
        self.store.append("webhook_payload_built", {"invoice_id": invoice_id, "event": event})
        return payload

    def configure_webhook(
        self,
        *,
        event: str,
        url: str,
        authorization_configured: bool = False,
    ) -> dict[str, Any]:
        """Record the documented Iugu trigger configuration boundary."""
        configuration = {
            "event": event,
            "url": url,
            "content_type": "application/x-www-form-urlencoded",
            "authorization_configured": authorization_configured,
        }
        self.store.webhook_configurations.append(deepcopy(configuration))
        self.store.append("webhook_configured", {"event": event, "url": url, "authorization_configured": authorization_configured})
        return deepcopy(configuration)

    def _validate(self, request: dict[str, Any]) -> None:
        required = ("email", "due_date", "items", "payable_with")
        missing = [key for key in required if not request.get(key)]
        if missing:
            raise IuguNativeError(
                NativeError(422, "required_parameter", f"Missing: {', '.join(missing)}", self.evidence)
            )
        if "pix" not in request["payable_with"]:
            raise IuguNativeError(NativeError(422, "invalid_payment_method", "Pix is not enabled.", self.evidence))
        if not isinstance(request["items"], list) or not request["items"]:
            raise IuguNativeError(NativeError(422, "required_parameter", "items must not be empty.", self.evidence))
        for item in request["items"]:
            if not item.get("description") or int(item.get("price_cents", 0)) < 100:
                raise IuguNativeError(NativeError(422, "invalid_parameter", "Invalid item price or description.", self.evidence))
