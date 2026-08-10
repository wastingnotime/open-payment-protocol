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
