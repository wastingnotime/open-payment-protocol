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
    assert GRAPH.validation_errors() == []
    assert len(GRAPH.scenario_ids) == 38
    assert all("-PIX-" in scenario_id for scenario_id in GRAPH.scenario_ids)
    assert GRAPH.actor_ids == (
        "ACTOR-SIMULATION-COORDINATOR",
        "ACTOR-ASAAS",
        "ACTOR-IUGU",
        "ACTOR-MERCADOPAGO",
        "ACTOR-PAGBANK",
        "ACTOR-PAGARME",
    )
    assert len(snapshot["nodes"]) == 63
    assert sum(node["kind"] == "deferred" for node in snapshot["nodes"]) == 2
    assert len(snapshot["known_edges"]) == 32
    assert len(snapshot["deferred_edges"]) == 2


def test_graph_exposes_provider_resource_nodes_separately_from_scenarios():
    assert len(GRAPH.resource_ids) == 11
    assert not set(GRAPH.resource_ids) & set(GRAPH.scenario_ids)


def test_every_executable_graph_scenario_has_a_provider_report():
    registries = run_all_providers()
    for scenario_id in GRAPH.scenario_ids:
        provider = next(node.provider for node in GRAPH.nodes if node.id == scenario_id)
        assert scenario_id in registries[provider]


def test_graph_observations_emit_every_node_and_edge():
    observations = GRAPH.observations()
    nodes = [item for item in observations if item["type"] == "graph_node"]
    edges = [item for item in observations if item["type"] == "graph_edge"]
    assert len(nodes) == 63
    assert len(edges) == 95
    assert {item["payload"]["id"] for item in nodes} == GRAPH.node_ids


def test_observatory_spec_contains_runtime_visible_nodes_and_edges():
    spec = GRAPH.observatory_spec()
    assert len(spec["nodes"]) == 63
    assert len(spec["edges"]) == 95
    assert {node["id"] for node in spec["nodes"]} == GRAPH.node_ids
    assert {node["kind"] for node in spec["nodes"]} == {"actor", "use_case", "aggregate", "projection", "external_provider"}
    assert {node["layer"] for node in spec["nodes"]} == {-8, 0, 4, 6, 10}
    assert {node["domain"] for node in spec["nodes"]} == {"payment-provider-discovery"}


def test_observatory_summary_matches_runtime_graph_contract():
    assert GRAPH.observatory_summary() == {"nodes": 63, "edges": 95, "actors": 6, "scenarios": 38, "resources": 11}


def test_beam_observations_route_between_declared_connected_nodes():
    observations = GRAPH.beam_observations()
    spec = GRAPH.observatory_spec()
    declared_edges = {(edge["from_node"], edge["to_node"]) for edge in spec["edges"]}

    assert len(observations) == 95
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


def test_beam_observations_have_stable_sequence_and_edge_kind():
    observations = GRAPH.beam_observations()

    assert [item["payload"]["sequence"] for item in observations] == list(range(95))
    assert {item["payload"]["edge_kind"] for item in observations} == {
        "actor_flow",
        "actor_use_case",
        "use_case_resource",
        "use_case_scenario",
        "lifecycle",
        "deferred",
    }


def test_beam_observations_expose_provider_and_status_for_runtime_filtering():
    for observation in GRAPH.beam_observations():
        payload = observation["payload"]
        assert payload["provider"] in {node.provider for node in GRAPH.nodes}
        assert payload["status"] in {"observed", "deferred"}
        assert observation["source"] in GRAPH.node_ids
        assert observation["name"] in GRAPH.node_ids
