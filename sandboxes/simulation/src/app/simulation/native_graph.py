"""Provider-native scenario graph for lifecycle-pressure discovery.

This graph is an internal comparison aid. Its nodes are executable scenario
IDs, and its edges preserve provider-native transitions rather than defining an
OPP status model.
"""

from __future__ import annotations

from dataclasses import dataclass


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
class TopologyEdge:
    source: str
    target: str
    relation: str
    kind: str


@dataclass(frozen=True)
class NativeScenarioGraph:
    nodes: tuple[GraphNode, ...]
    topology_edges: tuple[TopologyEdge, ...]
    known_edges: tuple[GraphEdge, ...]
    deferred_edges: tuple[DeferredEdge, ...]

    @property
    def node_ids(self) -> frozenset[str]:
        return frozenset(node.id for node in self.nodes)

    @property
    def actor_ids(self) -> tuple[str, ...]:
        return tuple(node.id for node in self.nodes if node.kind == "actor")

    @property
    def scenario_ids(self) -> tuple[str, ...]:
        return tuple(node.id for node in self.nodes if node.kind == "scenario")

    def snapshot(self) -> dict[str, object]:
        return {
            "nodes": [node.__dict__.copy() for node in self.nodes],
            "topology_edges": [edge.__dict__.copy() for edge in self.topology_edges],
            "known_edges": [edge.__dict__.copy() for edge in self.known_edges],
            "deferred_edges": [edge.__dict__.copy() for edge in self.deferred_edges],
        }

    def validation_errors(self) -> list[str]:
        """Return structural graph defects without normalizing provider facts."""
        errors: list[str] = []
        if len(self.node_ids) != len(self.nodes):
            errors.append("duplicate graph node IDs")
        edges = (*self.topology_edges, *self.known_edges, *self.deferred_edges)
        for edge in edges:
            if edge.source not in self.node_ids:
                errors.append(f"edge source is undeclared: {edge.source}")
            if edge.target not in self.node_ids:
                errors.append(f"edge target is undeclared: {edge.target}")
        reachable = {"ACTOR-SIMULATION-COORDINATOR"}
        while True:
            expanded = reachable | {
                edge.target for edge in edges if edge.source in reachable
            }
            if expanded == reachable:
                break
            reachable = expanded
        errors.extend(
            f"node is unreachable from coordinator: {node.id}"
            for node in self.nodes
            if node.id not in reachable
        )
        return errors

    def observations(self) -> list[dict[str, object]]:
        observations = [
            {"type": "graph_node", "name": "simulation_graph_node", "source": "simulation", "payload": node.__dict__.copy()}
            for node in self.nodes
        ]
        observations.extend(
            {"type": "graph_edge", "name": "simulation_graph_edge", "source": "simulation", "payload": edge.__dict__.copy()}
            for edge in (*self.topology_edges, *self.known_edges, *self.deferred_edges)
        )
        return observations

    def beam_observations(self) -> list[dict[str, object]]:
        """Encode graph traversals in the observatory runtime's route contract."""
        edges = (*self.topology_edges, *self.known_edges, *self.deferred_edges)
        return [
            {
                "type": "graph_route",
                "name": edge.target,
                "source": edge.source,
                "payload": {
                    "sequence": sequence,
                    "relation": edge.relation if isinstance(edge, (GraphEdge, TopologyEdge)) else edge.reason,
                    "edge_kind": edge.kind if isinstance(edge, TopologyEdge) else ("deferred" if isinstance(edge, DeferredEdge) else "lifecycle"),
                    "provider": getattr(edge, "provider", "simulation"),
                    "status": "deferred" if isinstance(edge, DeferredEdge) else "observed",
                },
            }
            for sequence, edge in enumerate(edges)
        ]

    def observatory_spec(self) -> dict[str, list[dict[str, object]]]:
        runtime_kind = {
            "actor": "actor",
            "use_case": "use_case",
            "resource": "aggregate",
            "scenario": "projection",
            "deferred": "external_provider",
        }
        runtime_layer = {"actor": -8, "use_case": 0, "resource": 4, "scenario": 6, "deferred": 10}
        return {
            "nodes": [
                {
                    "id": node.id,
                    "label": node.label,
                    "kind": runtime_kind[node.kind],
                    "layer": runtime_layer[node.kind],
                    "realm": node.provider,
                    "domain": "payment-provider-discovery",
                    "description": f"{node.provider} provider-native {node.kind} in the Pix discovery slice",
                    "badge": "deferred" if node.kind == "deferred" else ("Pix" if node.kind in {"resource", "scenario"} else node.kind),
                }
                for node in self.nodes
            ],
            "edges": [
                {"from_node": edge.source, "to_node": edge.target, "label": edge.relation if isinstance(edge, (GraphEdge, TopologyEdge)) else edge.reason, "kind": edge.kind if isinstance(edge, TopologyEdge) else ("deferred" if isinstance(edge, DeferredEdge) else "flow")}
                for edge in (*self.topology_edges, *self.known_edges, *self.deferred_edges)
            ],
        }


def _scenario_node(provider: str, scenario_id: str, label: str) -> GraphNode:
    return GraphNode(scenario_id, provider, "scenario", label, scenario_id)


TOPOLOGY_NODES = (
    GraphNode("ACTOR-SIMULATION-COORDINATOR", "simulation", "actor", "Simulation coordinator"),
    GraphNode("ACTOR-ASAAS", "asaas", "actor", "Asaas scenario actor"),
    GraphNode("ACTOR-IUGU", "iugu", "actor", "Iugu scenario actor"),
    GraphNode("ACTOR-MERCADOPAGO", "mercadopago", "actor", "Mercado Pago scenario actor"),
    GraphNode("ACTOR-PAGBANK", "pagbank", "actor", "PagBank scenario actor"),
    GraphNode("ACTOR-PAGARME", "pagarme", "actor", "Pagar.me scenario actor"),
    GraphNode("UC-ASAAS-CREATE-RETRIEVE", "asaas", "use_case", "Create, retrieve, and inspect Pix QR"),
    GraphNode("UC-IUGU-CREATE-RETRIEVE", "iugu", "use_case", "Create, retrieve, and reconcile invoice"),
    GraphNode("UC-IUGU-LIFECYCLE", "iugu", "use_case", "Advance invoice lifecycle"),
    GraphNode("UC-MERCADOPAGO-CREATE-RECONCILE", "mercadopago", "use_case", "Create and reconcile order"),
    GraphNode("UC-PAGBANK-CREATE-CHARGE", "pagbank", "use_case", "Create QR order and observe charge"),
    GraphNode("UC-PAGARME-CREATE-OUTCOME", "pagarme", "use_case", "Create order and simulate Pix outcome"),
    GraphNode("RESOURCE-ASAAS-PAYMENT", "asaas", "resource", "Asaas payment"),
    GraphNode("RESOURCE-IUGU-INVOICE", "iugu", "resource", "Iugu invoice"),
    GraphNode("RESOURCE-IUGU-PIX", "iugu", "resource", "Iugu embedded Pix"),
    GraphNode("RESOURCE-MERCADOPAGO-ORDER", "mercadopago", "resource", "Mercado Pago order"),
    GraphNode("RESOURCE-MERCADOPAGO-PAYMENT", "mercadopago", "resource", "Mercado Pago payment"),
    GraphNode("RESOURCE-PAGBANK-ORDER", "pagbank", "resource", "PagBank order"),
    GraphNode("RESOURCE-PAGBANK-QR", "pagbank", "resource", "PagBank QR Code"),
    GraphNode("RESOURCE-PAGBANK-CHARGE", "pagbank", "resource", "PagBank charge"),
    GraphNode("RESOURCE-PAGARME-ORDER", "pagarme", "resource", "Pagar.me order"),
    GraphNode("RESOURCE-PAGARME-CHARGE", "pagarme", "resource", "Pagar.me charge"),
    GraphNode("RESOURCE-PAGARME-TRANSACTION", "pagarme", "resource", "Pagar.me Pix transaction"),
)

NODES = TOPOLOGY_NODES + (
    _scenario_node("iugu", "IUGU-PIX-001", "create/retrieve pending invoice"),
    _scenario_node("iugu", "IUGU-PIX-007", "paid invoice"),
    _scenario_node("iugu", "IUGU-PIX-008", "canceled invoice"),
    _scenario_node("iugu", "IUGU-PIX-009", "expired invoice"),
    _scenario_node("iugu", "IUGU-PIX-010", "canceled invoice recovered to paid"),
    _scenario_node("iugu", "IUGU-PIX-011", "paid cancellation rejected"),
    _scenario_node("iugu", "IUGU-PIX-012", "expired payment rejected"),
    _scenario_node("iugu", "IUGU-PIX-014", "paid invoice status webhook"),
    _scenario_node("iugu", "IUGU-PIX-015", "canceled invoice status webhook"),
    _scenario_node("iugu", "IUGU-PIX-016", "invoice status webhook configured"),
    _scenario_node("iugu", "IUGU-PIX-017", "invalid webhook configuration rejected"),
    _scenario_node("mercadopago", "MP-PIX-001", "create/retrieve order"),
    _scenario_node("mercadopago", "MP-PIX-004", "processing order"),
    _scenario_node("mercadopago", "MP-PIX-005", "processing order retrieved"),
    _scenario_node("pagbank", "PB-PIX-001", "QR order without charge"),
    _scenario_node("pagbank", "PB-PIX-004", "paid charge emerges"),
    _scenario_node("pagbank", "PB-PIX-006", "duplicate payment rejected"),
    _scenario_node("pagbank", "PB-PIX-011", "paid order webhook notification"),
    _scenario_node("pagbank", "PB-PIX-012", "mismatched notification discarded"),
    _scenario_node("pagbank", "PB-PIX-013", "notification URL preserved"),
    _scenario_node("pagbank", "PB-PIX-014", "multiple notification URLs rejected"),
    _scenario_node("pagbank", "PB-PIX-015", "insecure notification URL rejected"),
    _scenario_node("pagarme", "PG-PIX-001", "pending order/charge/transaction"),
    _scenario_node("pagarme", "PG-PIX-003", "paid threshold outcome"),
    _scenario_node("pagarme", "PG-PIX-004", "failed threshold outcome"),
    _scenario_node("pagarme", "PG-PIX-008", "exact threshold paid outcome"),
    _scenario_node("pagarme", "PG-PIX-010", "paid outcome webhook sent"),
    _scenario_node("pagarme", "PG-PIX-011", "failed outcome webhook delivery failed"),
    _scenario_node("pagarme", "PG-PIX-012", "failed webhook manually resent"),
    _scenario_node("pagarme", "PG-PIX-013", "webhook delivery queried"),
    _scenario_node("pagarme", "PG-PIX-014", "paid order webhook sent"),
    _scenario_node("asaas", "AS-PIX-001", "payment with separate QR"),
    GraphNode("AS-PIX-DEFERRED-SUCCESS", "asaas", "deferred", "Pix success transition unknown"),
    GraphNode("MP-PIX-DEFERRED-FINALIZATION", "mercadopago", "deferred", "async finalization unknown"),
)

TOPOLOGY_EDGES = (
    TopologyEdge("ACTOR-SIMULATION-COORDINATOR", "ACTOR-ASAAS", "coordinates", "actor_flow"),
    TopologyEdge("ACTOR-SIMULATION-COORDINATOR", "ACTOR-IUGU", "coordinates", "actor_flow"),
    TopologyEdge("ACTOR-SIMULATION-COORDINATOR", "ACTOR-MERCADOPAGO", "coordinates", "actor_flow"),
    TopologyEdge("ACTOR-SIMULATION-COORDINATOR", "ACTOR-PAGBANK", "coordinates", "actor_flow"),
    TopologyEdge("ACTOR-SIMULATION-COORDINATOR", "ACTOR-PAGARME", "coordinates", "actor_flow"),
    TopologyEdge("ACTOR-ASAAS", "UC-ASAAS-CREATE-RETRIEVE", "drives", "actor_use_case"),
    TopologyEdge("ACTOR-IUGU", "UC-IUGU-CREATE-RETRIEVE", "drives", "actor_use_case"),
    TopologyEdge("ACTOR-IUGU", "UC-IUGU-LIFECYCLE", "drives", "actor_use_case"),
    TopologyEdge("ACTOR-MERCADOPAGO", "UC-MERCADOPAGO-CREATE-RECONCILE", "drives", "actor_use_case"),
    TopologyEdge("ACTOR-PAGBANK", "UC-PAGBANK-CREATE-CHARGE", "drives", "actor_use_case"),
    TopologyEdge("ACTOR-PAGARME", "UC-PAGARME-CREATE-OUTCOME", "drives", "actor_use_case"),
    TopologyEdge("UC-ASAAS-CREATE-RETRIEVE", "RESOURCE-ASAAS-PAYMENT", "operates_on", "use_case_resource"),
    TopologyEdge("UC-IUGU-CREATE-RETRIEVE", "RESOURCE-IUGU-INVOICE", "operates_on", "use_case_resource"),
    TopologyEdge("UC-IUGU-CREATE-RETRIEVE", "RESOURCE-IUGU-PIX", "observes", "use_case_resource"),
    TopologyEdge("UC-IUGU-LIFECYCLE", "RESOURCE-IUGU-INVOICE", "transitions", "use_case_resource"),
    TopologyEdge("UC-MERCADOPAGO-CREATE-RECONCILE", "RESOURCE-MERCADOPAGO-ORDER", "operates_on", "use_case_resource"),
    TopologyEdge("UC-MERCADOPAGO-CREATE-RECONCILE", "RESOURCE-MERCADOPAGO-PAYMENT", "observes", "use_case_resource"),
    TopologyEdge("UC-PAGBANK-CREATE-CHARGE", "RESOURCE-PAGBANK-ORDER", "operates_on", "use_case_resource"),
    TopologyEdge("UC-PAGBANK-CREATE-CHARGE", "RESOURCE-PAGBANK-QR", "observes", "use_case_resource"),
    TopologyEdge("UC-PAGBANK-CREATE-CHARGE", "RESOURCE-PAGBANK-CHARGE", "observes", "use_case_resource"),
    TopologyEdge("UC-PAGARME-CREATE-OUTCOME", "RESOURCE-PAGARME-ORDER", "operates_on", "use_case_resource"),
    TopologyEdge("UC-PAGARME-CREATE-OUTCOME", "RESOURCE-PAGARME-CHARGE", "observes", "use_case_resource"),
    TopologyEdge("UC-PAGARME-CREATE-OUTCOME", "RESOURCE-PAGARME-TRANSACTION", "observes", "use_case_resource"),
    TopologyEdge("UC-IUGU-CREATE-RETRIEVE", "IUGU-PIX-001", "executes", "use_case_scenario"),
    TopologyEdge("UC-IUGU-CREATE-RETRIEVE", "IUGU-PIX-007", "executes", "use_case_scenario"),
    TopologyEdge("UC-IUGU-CREATE-RETRIEVE", "IUGU-PIX-008", "executes", "use_case_scenario"),
    TopologyEdge("UC-IUGU-CREATE-RETRIEVE", "IUGU-PIX-009", "executes", "use_case_scenario"),
    TopologyEdge("UC-IUGU-LIFECYCLE", "IUGU-PIX-010", "executes", "use_case_scenario"),
    TopologyEdge("UC-IUGU-LIFECYCLE", "IUGU-PIX-011", "executes", "use_case_scenario"),
    TopologyEdge("UC-IUGU-LIFECYCLE", "IUGU-PIX-012", "executes", "use_case_scenario"),
    TopologyEdge("UC-IUGU-LIFECYCLE", "IUGU-PIX-014", "executes", "use_case_scenario"),
    TopologyEdge("UC-IUGU-LIFECYCLE", "IUGU-PIX-015", "executes", "use_case_scenario"),
    TopologyEdge("UC-IUGU-LIFECYCLE", "IUGU-PIX-016", "executes", "use_case_scenario"),
    TopologyEdge("UC-IUGU-LIFECYCLE", "IUGU-PIX-017", "executes", "use_case_scenario"),
    TopologyEdge("UC-MERCADOPAGO-CREATE-RECONCILE", "MP-PIX-001", "executes", "use_case_scenario"),
    TopologyEdge("UC-MERCADOPAGO-CREATE-RECONCILE", "MP-PIX-004", "executes", "use_case_scenario"),
    TopologyEdge("UC-MERCADOPAGO-CREATE-RECONCILE", "MP-PIX-005", "executes", "use_case_scenario"),
    TopologyEdge("UC-PAGBANK-CREATE-CHARGE", "PB-PIX-001", "executes", "use_case_scenario"),
    TopologyEdge("UC-PAGBANK-CREATE-CHARGE", "PB-PIX-004", "executes", "use_case_scenario"),
    TopologyEdge("UC-PAGBANK-CREATE-CHARGE", "PB-PIX-006", "executes", "use_case_scenario"),
    TopologyEdge("UC-PAGBANK-CREATE-CHARGE", "PB-PIX-011", "executes", "use_case_scenario"),
    TopologyEdge("UC-PAGBANK-CREATE-CHARGE", "PB-PIX-012", "executes", "use_case_scenario"),
    TopologyEdge("UC-PAGBANK-CREATE-CHARGE", "PB-PIX-013", "executes", "use_case_scenario"),
    TopologyEdge("UC-PAGBANK-CREATE-CHARGE", "PB-PIX-014", "executes", "use_case_scenario"),
    TopologyEdge("UC-PAGBANK-CREATE-CHARGE", "PB-PIX-015", "executes", "use_case_scenario"),
    TopologyEdge("UC-PAGARME-CREATE-OUTCOME", "PG-PIX-001", "executes", "use_case_scenario"),
    TopologyEdge("UC-PAGARME-CREATE-OUTCOME", "PG-PIX-003", "executes", "use_case_scenario"),
    TopologyEdge("UC-PAGARME-CREATE-OUTCOME", "PG-PIX-004", "executes", "use_case_scenario"),
    TopologyEdge("UC-PAGARME-CREATE-OUTCOME", "PG-PIX-008", "executes", "use_case_scenario"),
    TopologyEdge("UC-PAGARME-CREATE-OUTCOME", "PG-PIX-010", "executes", "use_case_scenario"),
    TopologyEdge("UC-PAGARME-CREATE-OUTCOME", "PG-PIX-011", "executes", "use_case_scenario"),
    TopologyEdge("UC-PAGARME-CREATE-OUTCOME", "PG-PIX-012", "executes", "use_case_scenario"),
    TopologyEdge("UC-PAGARME-CREATE-OUTCOME", "PG-PIX-013", "executes", "use_case_scenario"),
    TopologyEdge("UC-PAGARME-CREATE-OUTCOME", "PG-PIX-014", "executes", "use_case_scenario"),
    TopologyEdge("UC-ASAAS-CREATE-RETRIEVE", "AS-PIX-001", "executes", "use_case_scenario"),
)


KNOWN_EDGES = (
    GraphEdge("iugu", "IUGU-PIX-001", "IUGU-PIX-007", "pending_to_paid", "research/iugu/lifecycle.md"),
    GraphEdge("iugu", "IUGU-PIX-001", "IUGU-PIX-008", "pending_to_canceled", "research/iugu/lifecycle.md"),
    GraphEdge("iugu", "IUGU-PIX-001", "IUGU-PIX-009", "pending_to_expired", "research/iugu/lifecycle.md"),
    GraphEdge("iugu", "IUGU-PIX-008", "IUGU-PIX-010", "canceled_to_paid", "research/iugu/lifecycle.md"),
    GraphEdge("iugu", "IUGU-PIX-007", "IUGU-PIX-011", "paid_cancel_rejected", "research/iugu/lifecycle.md"),
    GraphEdge("iugu", "IUGU-PIX-009", "IUGU-PIX-012", "expired_payment_rejected", "research/iugu/lifecycle.md"),
    GraphEdge("iugu", "IUGU-PIX-007", "IUGU-PIX-014", "paid_status_webhook", "research/iugu/webhooks.md"),
    GraphEdge("iugu", "IUGU-PIX-008", "IUGU-PIX-015", "canceled_status_webhook", "research/iugu/webhooks.md"),
    GraphEdge("iugu", "IUGU-PIX-014", "IUGU-PIX-016", "webhook_trigger_configured", "research/iugu/webhooks.md"),
    GraphEdge("iugu", "IUGU-PIX-016", "IUGU-PIX-017", "webhook_configuration_rejected", "research/iugu/webhooks.md"),
    GraphEdge("mercadopago", "MP-PIX-001", "MP-PIX-004", "async_processing_variant", "research/mercadopago/lifecycle.md"),
    GraphEdge("mercadopago", "MP-PIX-004", "MP-PIX-005", "processing_retrieval", "research/mercadopago/lifecycle.md"),
    GraphEdge("pagbank", "PB-PIX-001", "PB-PIX-004", "charge_emerges_after_pix", "research/pagbank/lifecycle.md"),
    GraphEdge("pagbank", "PB-PIX-004", "PB-PIX-006", "duplicate_payment_rejected", "research/pagbank/lifecycle.md"),
    GraphEdge("pagbank", "PB-PIX-004", "PB-PIX-011", "paid_order_webhook", "research/pagbank/webhooks.md"),
    GraphEdge("pagbank", "PB-PIX-011", "PB-PIX-012", "notification_authenticity_rejected", "research/pagbank/webhooks.md"),
    GraphEdge("pagbank", "PB-PIX-011", "PB-PIX-013", "notification_url_preserved", "research/pagbank/webhooks.md"),
    GraphEdge("pagbank", "PB-PIX-013", "PB-PIX-014", "notification_url_limit_rejected", "research/pagbank/webhooks.md"),
    GraphEdge("pagbank", "PB-PIX-014", "PB-PIX-015", "notification_url_transport_rejected", "research/pagbank/webhooks.md"),
    GraphEdge("pagarme", "PG-PIX-001", "PG-PIX-003", "simulator_paid_threshold", "research/pagarme/lifecycle.md"),
    GraphEdge("pagarme", "PG-PIX-001", "PG-PIX-004", "simulator_failed_threshold", "research/pagarme/lifecycle.md"),
    GraphEdge("pagarme", "PG-PIX-001", "PG-PIX-008", "simulator_exact_threshold_paid", "research/pagarme/lifecycle.md"),
    GraphEdge("pagarme", "PG-PIX-003", "PG-PIX-010", "paid_webhook_sent", "research/pagarme/webhooks.md"),
    GraphEdge("pagarme", "PG-PIX-004", "PG-PIX-011", "failed_webhook_delivery", "research/pagarme/webhooks.md"),
    GraphEdge("pagarme", "PG-PIX-011", "PG-PIX-012", "webhook_manually_resent", "research/pagarme/webhooks.md"),
    GraphEdge("pagarme", "PG-PIX-012", "PG-PIX-013", "webhook_delivery_queried", "research/pagarme/webhooks.md"),
    GraphEdge("pagarme", "PG-PIX-003", "PG-PIX-014", "paid_order_webhook_sent", "research/pagarme/webhooks.md"),
)

DEFERRED_EDGES = (
    DeferredEdge("asaas", "AS-PIX-001", "AS-PIX-DEFERRED-SUCCESS", "initial Pix transition is unknown", "research/asaas/lifecycle.md"),
    DeferredEdge("mercadopago", "MP-PIX-004", "MP-PIX-DEFERRED-FINALIZATION", "async finalization is not established", "research/mercadopago/lifecycle.md"),
)

GRAPH = NativeScenarioGraph(NODES, TOPOLOGY_EDGES, KNOWN_EDGES, DEFERRED_EDGES)
