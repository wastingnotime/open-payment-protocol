import json
import math

import pytest

from app.simulation.scenario_registry import PROVIDER_RUNNERS, run_all_providers
from app.simulation.report_contract import PROVIDER_ORDER, PROVIDER_PREFIXES, PROVIDER_SCENARIO_COUNTS, REPORT_FIELDS, TOTAL_SCENARIO_COUNT, allowed_sources, assert_sanitized, canonical_snapshot, error_inventory, field, observation_inventory, validate_report


def test_all_provider_scenarios_preserve_comparable_report_shape():
    assert tuple(PROVIDER_RUNNERS) == PROVIDER_ORDER
    registries = run_all_providers()
    assert isinstance(registries, dict)
    assert tuple(registries) == PROVIDER_ORDER
    assert all(isinstance(reports, dict) for reports in registries.values())
    assert {provider: len(scenarios) for provider, scenarios in registries.items()} == PROVIDER_SCENARIO_COUNTS
    assert sum(len(scenarios) for scenarios in registries.values()) == TOTAL_SCENARIO_COUNT
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


def test_observation_inventory_preserves_provider_native_names():
    inventory = observation_inventory(run_all_providers())
    assert tuple(inventory) == PROVIDER_ORDER
    assert inventory["asaas"]["native_webhook_notification"] == 2
    assert inventory["iugu"]["native_webhook_event"] == 2
    assert inventory["mercadopago"]["native_webhook_notification"] == 1
    assert inventory["pagarme"]["native_webhook_delivery"] == 3
    assert inventory["pagbank"]["native_webhook_notification"] == 1


def test_observation_inventory_exposes_refund_and_cancellation_names_without_normalizing_them():
    inventory = observation_inventory(run_all_providers())
    assert inventory["mercadopago"]["native_partial_refund"] == 1
    assert inventory["mercadopago"]["native_total_refund"] == 1
    assert inventory["pagbank"]["native_partial_cancellation"] == 1
    assert inventory["pagbank"]["native_full_cancellation"] == 1
    assert "native_refund" not in inventory["mercadopago"]
    assert "native_refund" not in inventory["pagbank"]


def test_observation_inventory_exposes_expiration_alternatives_as_native_evidence():
    inventory = observation_inventory(run_all_providers())
    assert inventory["mercadopago"]["native_expiration"] == 2
    assert inventory["mercadopago"]["native_unpaid_cancellation"] == 1


def test_observation_inventory_exposes_asaas_authentication_errors():
    inventory = observation_inventory(run_all_providers())
    assert inventory["asaas"]["native_authentication_error"] == 3


def test_error_inventory_preserves_provider_native_codes():
    inventory = error_inventory(run_all_providers())
    assert inventory["asaas"]["access_token_not_found"] == 1
    assert inventory["asaas"]["invalid_access_token"] == 1
    assert inventory["asaas"]["invalid_environment"] == 1
    assert inventory["mercadopago"]["order_not_found"] == 1


def test_observation_inventory_covers_every_provider_scenario():
    registries = run_all_providers()
    inventory = observation_inventory(registries)
    for provider, scenarios in registries.items():
        assert sum(inventory[provider].values()) >= len(scenarios)
        assert all(count > 0 for count in inventory[provider].values())


def test_observation_inventory_preserves_source_provenance():
    for provider, scenarios in run_all_providers().items():
        sources = {
            observation["source"]
            for report in scenarios.values()
            for observation in field(report, "observations")
        }
        assert sources <= allowed_sources(provider)
        assert provider in sources


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
