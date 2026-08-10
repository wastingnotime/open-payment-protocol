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
    assert len(snapshot["nodes"]) == 43
    assert sum(node["kind"] == "deferred" for node in snapshot["nodes"]) == 2
    assert len(snapshot["known_edges"]) == 13
    assert len(snapshot["deferred_edges"]) == 2


def test_graph_observations_emit_every_node_and_edge():
    observations = GRAPH.observations()
    nodes = [item for item in observations if item["type"] == "graph_node"]
    edges = [item for item in observations if item["type"] == "graph_edge"]
    assert len(nodes) == 43
    assert len(edges) == 56
    assert {item["payload"]["id"] for item in nodes} == GRAPH.node_ids


def test_observatory_spec_contains_runtime_visible_nodes_and_edges():
    spec = GRAPH.observatory_spec()
    assert len(spec["nodes"]) == 43
    assert len(spec["edges"]) == 56
    assert {node["id"] for node in spec["nodes"]} == GRAPH.node_ids
    assert {node["kind"] for node in spec["nodes"]} == {"actor", "use_case", "aggregate", "projection", "external_provider"}
    assert {node["layer"] for node in spec["nodes"]} == {-8, 0, 4, 6, 10}
    assert {node["domain"] for node in spec["nodes"]} == {"payment-provider-discovery"}


def test_beam_observations_route_between_declared_connected_nodes():
    observations = GRAPH.beam_observations()
    spec = GRAPH.observatory_spec()
    declared_edges = {(edge["from_node"], edge["to_node"]) for edge in spec["edges"]}

    assert len(observations) == 56
    assert {(item["source"], item["name"]) for item in observations} == declared_edges
    assert all(item["type"] == "graph_route" for item in observations)
    assert all(item["source"] in GRAPH.node_ids for item in observations)
    assert all(item["name"] in GRAPH.node_ids for item in observations)


def test_beam_observations_preserve_deferred_status():
    deferred_targets = {
        edge.target for edge in GRAPH.deferred_edges
    }
    routes = {
        item["name"]: item
        for item in GRAPH.beam_observations()
        if item["name"] in deferred_targets
    }

    assert set(routes) == deferred_targets
    assert all(item["payload"]["status"] == "deferred" for item in routes.values())
