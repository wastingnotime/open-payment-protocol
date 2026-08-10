from app.simulation.asaas_scenarios import run_all as run_asaas
from app.simulation.scenarios import run_all as run_iugu
from app.simulation.mercadopago_scenarios import run_all as run_mercado_pago
from app.simulation.pagarme_scenarios import run_all as run_pagarme
from app.simulation.pagbank_scenarios import run_all as run_pagbank
from app.simulation.report_contract import REPORT_FIELDS, PROVIDER_PREFIXES, allowed_sources, canonical_snapshot, field
import json


def test_all_provider_scenarios_preserve_comparable_report_shape():
    registries = {
        "asaas": run_asaas(),
        "iugu": run_iugu(),
        "mercadopago": run_mercado_pago(),
        "pagarme": run_pagarme(),
        "pagbank": run_pagbank(),
    }
    assert {provider: len(scenarios) for provider, scenarios in registries.items()} == {
        "asaas": 8, "iugu": 13, "mercadopago": 10, "pagarme": 9, "pagbank": 10,
    }
    prefixes = {"asaas": "AS-", "iugu": "IUGU-", "mercadopago": "MP-", "pagarme": "PG-", "pagbank": "PB-"}
    assert sum(len(scenarios) for scenarios in registries.values()) == 50
    for provider, scenarios in registries.items():
        assert scenarios
        for scenario_id, report in scenarios.items():
            assert scenario_id.startswith(prefixes[provider])
            assert field(report, "name") == scenario_id
            assert isinstance(field(report, "events"), list)
            assert isinstance(field(report, "projection"), dict)
            assert field(report, "observations")
            for observation in field(report, "observations"):
                assert set(("type", "name", "source", "payload")) <= observation.keys()
                assert observation["source"] in allowed_sources(provider)
                assert observation["payload"]["scenario"] == scenario_id


def test_all_provider_scenario_reports_exclude_cardholder_data_markers():
    registries = (run_asaas(), run_iugu(), run_mercado_pago(), run_pagarme(), run_pagbank())
    reports = []
    for scenarios in registries:
        for report in scenarios.values():
            reports.append({name: field(report, name) for name in REPORT_FIELDS})
    serialized = json.dumps(reports).lower()
    for marker in ("pan", "cvv", "card_number", "api_key", "access_token", "secret_key"):
        assert marker not in serialized


def test_all_provider_scenario_registries_are_deterministically_replayable():
    runners = (run_asaas, run_iugu, run_mercado_pago, run_pagarme, run_pagbank)

    first_run = [canonical_snapshot(runner()) for runner in runners]
    second_run = [canonical_snapshot(runner()) for runner in runners]
    assert first_run == second_run
