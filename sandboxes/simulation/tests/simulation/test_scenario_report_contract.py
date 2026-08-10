import json
import math

import pytest

from app.simulation.scenario_registry import PROVIDER_RUNNERS, run_all_providers
from app.simulation.report_contract import PROVIDER_ORDER, PROVIDER_PREFIXES, PROVIDER_SCENARIO_COUNTS, REPORT_FIELDS, allowed_sources, assert_sanitized, canonical_snapshot, field, validate_report


def test_all_provider_scenarios_preserve_comparable_report_shape():
    assert tuple(PROVIDER_RUNNERS) == PROVIDER_ORDER
    registries = run_all_providers()
    assert isinstance(registries, dict)
    assert tuple(registries) == PROVIDER_ORDER
    assert all(isinstance(reports, dict) for reports in registries.values())
    assert {provider: len(scenarios) for provider, scenarios in registries.items()} == PROVIDER_SCENARIO_COUNTS
    assert sum(len(scenarios) for scenarios in registries.values()) == 70
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


def test_canonical_snapshot_rejects_nonstandard_numbers():
    reports = {"one": {"name": "A", "observations": [], "events": [], "projection": {"value": math.nan}}}
    with pytest.raises(ValueError, match="Out of range float values"):
        canonical_snapshot(reports)


def test_contract_mappings_are_immutable():
    with pytest.raises(TypeError):
        PROVIDER_PREFIXES["new"] = "NEW-"
    with pytest.raises(TypeError):
        PROVIDER_SCENARIO_COUNTS["new"] = 0
    with pytest.raises(TypeError):
        PROVIDER_RUNNERS["new"] = lambda: {}
    assert isinstance(allowed_sources("iugu"), frozenset)


def test_unknown_provider_has_contextual_validation_error():
    with pytest.raises(AssertionError, match="unknown provider"):
        validate_report("unknown", "XX-001", {})


def test_malformed_observation_has_contextual_validation_error():
    report = {"name": "AS-001", "events": [], "projection": {}, "observations": [{"type": "event", "name": "broken", "source": "asaas", "payload": None}]}
    with pytest.raises(AssertionError, match="asaas/AS-001"):
        validate_report("asaas", "AS-001", report)


def test_observations_must_be_a_list():
    report = {"name": "AS-001", "events": [], "projection": {}, "observations": {}}
    with pytest.raises(AssertionError, match="observations must be a non-empty list"):
        validate_report("asaas", "AS-001", report)


def test_observation_items_must_be_mappings():
    report = {"name": "AS-001", "events": [], "projection": {}, "observations": ["broken"]}
    with pytest.raises(AssertionError, match="observation must be a mapping"):
        validate_report("asaas", "AS-001", report)


def test_event_items_must_be_mappings():
    report = {"name": "AS-001", "events": ["broken"], "projection": {}, "observations": []}
    with pytest.raises(AssertionError, match="event items must be mappings"):
        validate_report("asaas", "AS-001", report)


def test_missing_report_field_has_named_contract_error():
    with pytest.raises(AssertionError, match="missing required field: name"):
        field({}, "name")
    with pytest.raises(AssertionError, match="missing required field: name"):
        field(None, "name")


def test_repeated_provider_runs_return_independent_projections():
    first_run = run_all_providers()
    second_run = run_all_providers()
    first_run["asaas"]["AS-PIX-001"]["projection"].clear()
    assert second_run["asaas"]["AS-PIX-001"]["projection"]
