from app.simulation.asaas_scenarios import run_all as run_asaas
from app.simulation.scenarios import run_all as run_iugu
from app.simulation.mercadopago_scenarios import run_all as run_mercado_pago
from app.simulation.pagarme_scenarios import run_all as run_pagarme
from app.simulation.pagbank_scenarios import run_all as run_pagbank
import json


def _field(report, name):
    return report[name] if isinstance(report, dict) else getattr(report, name)


def test_all_provider_scenarios_preserve_comparable_report_shape():
    registries = (run_asaas(), run_iugu(), run_mercado_pago(), run_pagarme(), run_pagbank())
    for scenarios in registries:
        assert scenarios
        for scenario_id, report in scenarios.items():
            assert _field(report, "name") == scenario_id
            assert isinstance(_field(report, "events"), list)
            assert isinstance(_field(report, "projection"), dict)
            assert _field(report, "observations")
            assert all(item["payload"]["scenario"] == scenario_id for item in _field(report, "observations"))


def test_all_provider_scenario_reports_exclude_cardholder_data_markers():
    registries = (run_asaas(), run_iugu(), run_mercado_pago(), run_pagarme(), run_pagbank())
    reports = []
    for scenarios in registries:
        for report in scenarios.values():
            reports.append({name: _field(report, name) for name in ("name", "observations", "events", "projection")})
    serialized = json.dumps(reports).lower()
    assert "pan" not in serialized
    assert "cvv" not in serialized
    assert "card_number" not in serialized
