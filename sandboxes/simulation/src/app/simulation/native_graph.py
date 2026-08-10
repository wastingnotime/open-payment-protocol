"""Provider-native scenario graph for lifecycle-pressure discovery.

This graph is an internal comparison aid. Its nodes are executable scenario
IDs, and its edges preserve provider-native transitions rather than defining an
OPP status model.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GraphEdge:
    provider: str
    source: str
    target: str
    relation: str
    evidence: str


@dataclass(frozen=True)
class DeferredEdge:
    provider: str
    source: str
    target: str
    reason: str
    evidence: str


KNOWN_EDGES = (
    GraphEdge("iugu", "IUGU-PIX-001", "IUGU-PIX-007", "pending_to_paid", "research/iugu/lifecycle.md"),
    GraphEdge("iugu", "IUGU-PIX-001", "IUGU-PIX-008", "pending_to_canceled", "research/iugu/lifecycle.md"),
    GraphEdge("iugu", "IUGU-PIX-001", "IUGU-PIX-009", "pending_to_expired", "research/iugu/lifecycle.md"),
    GraphEdge("iugu", "IUGU-PIX-008", "IUGU-PIX-010", "canceled_to_paid", "research/iugu/lifecycle.md"),
    GraphEdge("iugu", "IUGU-PIX-007", "IUGU-PIX-011", "paid_cancel_rejected", "research/iugu/lifecycle.md"),
    GraphEdge("iugu", "IUGU-PIX-009", "IUGU-PIX-012", "expired_payment_rejected", "research/iugu/lifecycle.md"),
    GraphEdge("mercadopago", "MP-PIX-001", "MP-PIX-004", "async_processing_variant", "research/mercadopago/lifecycle.md"),
    GraphEdge("mercadopago", "MP-PIX-004", "MP-PIX-005", "processing_retrieval", "research/mercadopago/lifecycle.md"),
    GraphEdge("pagbank", "PB-PIX-001", "PB-PIX-004", "charge_emerges_after_pix", "research/pagbank/lifecycle.md"),
    GraphEdge("pagbank", "PB-PIX-004", "PB-PIX-006", "duplicate_payment_rejected", "research/pagbank/lifecycle.md"),
    GraphEdge("pagarme", "PG-PIX-001", "PG-PIX-003", "simulator_paid_threshold", "research/pagarme/lifecycle.md"),
    GraphEdge("pagarme", "PG-PIX-001", "PG-PIX-004", "simulator_failed_threshold", "research/pagarme/lifecycle.md"),
    GraphEdge("pagarme", "PG-PIX-001", "PG-PIX-008", "simulator_exact_threshold_paid", "research/pagarme/lifecycle.md"),
)

DEFERRED_EDGES = (
    DeferredEdge("asaas", "AS-PIX-001", "pix_success", "initial Pix transition is unknown", "research/asaas/lifecycle.md"),
    DeferredEdge("mercadopago", "MP-PIX-004", "payment_success", "async finalization is not established", "research/mercadopago/lifecycle.md"),
)
