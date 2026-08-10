"""WNT MRL Runtime boundary for the repository simulation.

The pure simulation is importable without the optional runtime package. The
factory deliberately fails with an actionable message when the local WNT MRL
Runtime is not installed, instead of shipping a second incompatible runtime.
"""

from __future__ import annotations

from datetime import datetime, timezone

from .scenarios import run_all
from .mercadopago_scenarios import run_all as run_mercadopago
from .pagbank_scenarios import run_all as run_pagbank
from .pagarme_scenarios import run_all as run_pagarme
from .asaas_scenarios import run_all as run_asaas
from .native_graph import GRAPH


def create_simulation():
    try:
        from mrl_simulation_runtime.scenario import Scenario
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Install the WNT MRL Runtime before supervision: "
            "wnt install --target mrl_runtime_user --target mrl_user_bin --user --force"
        ) from exc

    from mrl_simulation_runtime.actors import Actor
    from mrl_simulation_runtime.scenario import InitialScheduledAction, ObservatoryEdge, ObservatoryNode

    initial_time = datetime(2026, 8, 9, 12, 0, tzinfo=timezone.utc)
    graph_spec = GRAPH.observatory_spec()

    def emit_slice_results(context) -> None:
        for observation in GRAPH.observations():
            context.emit(
                observation["type"],
                observation["name"],
                source=observation["source"],
                payload=observation["payload"],
            )
        for observation in GRAPH.beam_observations():
            context.emit(
                observation["type"],
                observation["name"],
                source=observation["source"],
                correlation_id="provider-discovery-graph",
                payload=observation["payload"],
            )
        all_results = {**run_all(), **run_mercadopago(), **run_pagbank(), **run_pagarme(), **run_asaas()}
        for result in all_results.values():
            observations = result.observations if hasattr(result, "observations") else result["observations"]
            for observation in observations:
                context.emit(
                    observation["type"],
                    observation["name"],
                    source=observation.get("source"),
                    payload=observation.get("payload", {}),
                )

    return Scenario(
        name="opp-payment-provider-discovery",
        run_id="payment-provider-discovery",
        seed=1,
        initial_time=initial_time,
        actors=[Actor("IuguScenarioActor")],
        observatory_nodes=[ObservatoryNode(**node) for node in graph_spec["nodes"]],
        observatory_edges=[ObservatoryEdge(**edge) for edge in graph_spec["edges"]],
        scheduled_actions=[
            InitialScheduledAction(
                when=initial_time,
                action=emit_slice_results,
                name="RunIuguPixScenarios",
                source="IuguScenarioActor",
                correlation_id="payment-provider-discovery",
            )
        ],
    )
