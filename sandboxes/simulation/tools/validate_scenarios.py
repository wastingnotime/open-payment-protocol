"""Validate the minimum report shape across provider scenario registries."""

from __future__ import annotations

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app.simulation.scenario_registry import run_all_providers
from app.simulation.native_graph import GRAPH
from app.simulation.report_contract import PROVIDER_ORDER, REPORT_FIELDS, PROVIDER_SCENARIO_COUNTS, TOTAL_SCENARIO_COUNT, assert_sanitized, canonical_snapshot, error_inventory, field, observation_inventory, unknown_result_inventory, validate_report


def main() -> int:
    runners = run_all_providers()
    second_run = run_all_providers()
    assert tuple(runners) == PROVIDER_ORDER
    total = 0
    assert {provider: len(reports) for provider, reports in runners.items()} == PROVIDER_SCENARIO_COUNTS
    serialized_reports = []
    for provider, reports in runners.items():
        for scenario_id, report in reports.items():
            validate_report(provider, scenario_id, report)
            serialized_reports.append({name: field(report, name) for name in REPORT_FIELDS})
            total += 1
        print(f"{provider}: {len(reports)} scenarios validated")
    assert_sanitized(json.dumps(serialized_reports))
    assert total == TOTAL_SCENARIO_COUNT
    assert {provider: canonical_snapshot(reports) for provider, reports in runners.items()} == {
        provider: canonical_snapshot(reports) for provider, reports in second_run.items()
    }
    print(f"validated {total} scenarios")
    print(f"native observations: {observation_inventory(runners)}")
    print(f"native errors: {error_inventory(runners)}")
    print(f"unknown results: {unknown_result_inventory(runners)}")
    iugu_events = {
        observation["payload"]["event"]
        for report in runners["iugu"].values()
        for observation in field(report, "observations")
        if observation["name"] == "native_webhook_event"
    }
    assert {"invoice.due", "invoice.payment_failed", "invoice.refund", "invoice.rejected"} <= iugu_events
    print(f"iugu webhook events: {sorted(iugu_events)}")
    graph = GRAPH.snapshot()
    assert GRAPH.validation_errors() == []
    assert len(GRAPH.scenario_ids) == 60
    expiration_scenarios = {"MP-PIX-015", "MP-PIX-016", "MP-PIX-017"}
    assert expiration_scenarios <= set(GRAPH.scenario_ids)
    print(f"expiration slice: {sorted(expiration_scenarios)}")
    print(f"graph: {len(graph['nodes'])} nodes, {len(graph['topology_edges'])} topology edges, {len(graph['known_edges'])} known edges, {len(graph['deferred_edges'])} deferred edges")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
