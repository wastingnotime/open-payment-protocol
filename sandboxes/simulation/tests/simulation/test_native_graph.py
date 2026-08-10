from app.simulation.native_graph import DEFERRED_EDGES, GRAPH, KNOWN_EDGES
from app.simulation.scenario_registry import run_all_providers


def test_known_graph_edges_reference_executable_scenarios():
    registries = run_all_providers()
    assert GRAPH.nodes
    for edge in KNOWN_EDGES:
        assert edge.provider in registries
        assert edge.source in GRAPH.node_ids
        assert edge.target in GRAPH.node_ids
        assert edge.source in registries[edge.provider]
        assert edge.target in registries[edge.provider]
        assert edge.evidence.startswith("research/")


def test_deferred_graph_edges_remain_explicit_and_non_executable():
    registries = run_all_providers()
    for edge in DEFERRED_EDGES:
        assert edge.source in registries[edge.provider]
        assert edge.source in GRAPH.node_ids
        assert edge.target in GRAPH.node_ids
        assert edge.target not in registries[edge.provider]
        assert edge.reason
        assert edge.evidence.startswith("research/")


def test_graph_snapshot_exposes_executable_and_deferred_nodes():
    snapshot = GRAPH.snapshot()
    assert len(snapshot["nodes"]) == 20
    assert sum(node["kind"] == "deferred" for node in snapshot["nodes"]) == 2
    assert len(snapshot["known_edges"]) == 13
    assert len(snapshot["deferred_edges"]) == 2


def test_graph_observations_emit_every_node_and_edge():
    observations = GRAPH.observations()
    nodes = [item for item in observations if item["type"] == "graph_node"]
    edges = [item for item in observations if item["type"] == "graph_edge"]
    assert len(nodes) == 20
    assert len(edges) == 15
    assert {item["payload"]["id"] for item in nodes} == GRAPH.node_ids
