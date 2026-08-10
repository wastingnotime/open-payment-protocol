from app.simulation.scenario_registry import PROVIDER_RUNNERS, run_all_providers
from app.simulation.report_contract import REPORT_FIELDS, PROVIDER_SCENARIO_COUNTS, assert_sanitized, canonical_snapshot, field, validate_report
import json


def test_all_provider_scenarios_preserve_comparable_report_shape():
    assert tuple(PROVIDER_RUNNERS) == ("asaas", "iugu", "mercadopago", "pagarme", "pagbank")
    registries = run_all_providers()
    assert {provider: len(scenarios) for provider, scenarios in registries.items()} == PROVIDER_SCENARIO_COUNTS
    assert sum(len(scenarios) for scenarios in registries.values()) == 50
    for provider, scenarios in registries.items():
        assert scenarios
        for scenario_id, report in scenarios.items():
            validate_report(provider, scenario_id, report)


def test_all_provider_scenario_reports_exclude_cardholder_data_markers():
    registries = tuple(run_all_providers().values())
    reports = []
    for scenarios in registries:
        for report in scenarios.values():
            reports.append({name: field(report, name) for name in REPORT_FIELDS})
    assert_sanitized(json.dumps(reports))


def test_all_provider_scenario_registries_are_deterministically_replayable():
    first_run = [canonical_snapshot(reports) for reports in run_all_providers().values()]
    second_run = [canonical_snapshot(reports) for reports in run_all_providers().values()]
    assert first_run == second_run


def test_canonical_snapshot_ignores_registry_insertion_order():
    reports = {
        "second": {"name": "B", "observations": [], "events": [], "projection": {}},
        "first": {"name": "A", "observations": [], "events": [], "projection": {}},
    }
    reversed_reports = dict(reversed(list(reports.items())))
    assert canonical_snapshot(reports) == canonical_snapshot(reversed_reports)
