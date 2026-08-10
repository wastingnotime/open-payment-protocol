"""Provider-native scenario graph for lifecycle-pressure discovery.

This graph is an internal comparison aid. Its nodes are executable scenario
IDs, and its edges preserve provider-native transitions rather than defining an
OPP status model.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class GraphNode:
    id: str
    provider: str
    kind: str
    label: str
    scenario_id: str | None = None


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


@dataclass(frozen=True)
class NativeScenarioGraph:
    nodes: tuple[GraphNode, ...]
    known_edges: tuple[GraphEdge, ...]
    deferred_edges: tuple[DeferredEdge, ...]

    @property
    def node_ids(self) -> frozenset[str]:
        return frozenset(node.id for node in self.nodes)


def _scenario_node(provider: str, scenario_id: str, label: str) -> GraphNode:
    return GraphNode(scenario_id, provider, "scenario", label, scenario_id)


NODES = (
    _scenario_node("iugu", "IUGU-PIX-001", "create/retrieve pending invoice"),
    _scenario_node("iugu", "IUGU-PIX-007", "paid invoice"),
    _scenario_node("iugu", "IUGU-PIX-008", "canceled invoice"),
    _scenario_node("iugu", "IUGU-PIX-009", "expired invoice"),
    _scenario_node("iugu", "IUGU-PIX-010", "canceled invoice recovered to paid"),
    _scenario_node("iugu", "IUGU-PIX-011", "paid cancellation rejected"),
    _scenario_node("iugu", "IUGU-PIX-012", "expired payment rejected"),
    _scenario_node("mercadopago", "MP-PIX-001", "create/retrieve order"),
    _scenario_node("mercadopago", "MP-PIX-004", "processing order"),
    _scenario_node("mercadopago", "MP-PIX-005", "processing order retrieved"),
    _scenario_node("pagbank", "PB-PIX-001", "QR order without charge"),
    _scenario_node("pagbank", "PB-PIX-004", "paid charge emerges"),
    _scenario_node("pagbank", "PB-PIX-006", "duplicate payment rejected"),
    _scenario_node("pagarme", "PG-PIX-001", "pending order/charge/transaction"),
    _scenario_node("pagarme", "PG-PIX-003", "paid threshold outcome"),
    _scenario_node("pagarme", "PG-PIX-004", "failed threshold outcome"),
    _scenario_node("pagarme", "PG-PIX-008", "exact threshold paid outcome"),
    _scenario_node("asaas", "AS-PIX-001", "payment with separate QR"),
    GraphNode("AS-PIX-DEFERRED-SUCCESS", "asaas", "deferred", "Pix success transition unknown"),
    GraphNode("MP-PIX-DEFERRED-FINALIZATION", "mercadopago", "deferred", "async finalization unknown"),
)


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
    DeferredEdge("asaas", "AS-PIX-001", "AS-PIX-DEFERRED-SUCCESS", "initial Pix transition is unknown", "research/asaas/lifecycle.md"),
    DeferredEdge("mercadopago", "MP-PIX-004", "MP-PIX-DEFERRED-FINALIZATION", "async finalization is not established", "research/mercadopago/lifecycle.md"),
)

GRAPH = NativeScenarioGraph(NODES, KNOWN_EDGES, DEFERRED_EDGES)
