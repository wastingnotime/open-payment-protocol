"""Validate the minimum report shape across provider scenario registries."""

from __future__ import annotations

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app.simulation.asaas_scenarios import run_all as run_asaas
from app.simulation.mercadopago_scenarios import run_all as run_mercado_pago
from app.simulation.pagarme_scenarios import run_all as run_pagarme
from app.simulation.pagbank_scenarios import run_all as run_pagbank
from app.simulation.scenarios import run_all as run_iugu
from app.simulation.report_contract import REPORT_FIELDS, PROVIDER_PREFIXES, allowed_sources, canonical_snapshot, field


def main() -> int:
    runners = {
        "asaas": run_asaas(),
        "iugu": run_iugu(),
        "mercadopago": run_mercado_pago(),
        "pagarme": run_pagarme(),
        "pagbank": run_pagbank(),
    }
    second_run = {
        "asaas": run_asaas(),
        "iugu": run_iugu(),
        "mercadopago": run_mercado_pago(),
        "pagarme": run_pagarme(),
        "pagbank": run_pagbank(),
    }
    total = 0
    serialized_reports = []
    for provider, reports in runners.items():
        for scenario_id, report in reports.items():
            observations = field(report, "observations")
            assert scenario_id.startswith(PROVIDER_PREFIXES[provider])
            assert field(report, "name") == scenario_id
            assert isinstance(field(report, "events"), list)
            assert isinstance(field(report, "projection"), dict)
            assert observations
            for observation in observations:
                assert {"type", "name", "source", "payload"} <= observation.keys()
                assert observation["source"] in allowed_sources(provider)
                assert observation["payload"]["scenario"] == scenario_id
            serialized_reports.append({name: field(report, name) for name in REPORT_FIELDS})
            total += 1
        print(f"{provider}: {len(reports)} scenarios validated")
    serialized = json.dumps(serialized_reports).lower()
    for marker in ("pan", "cvv", "card_number", "api_key", "access_token", "secret_key"):
        assert marker not in serialized
    assert total == 50
    assert {provider: canonical_snapshot(reports) for provider, reports in runners.items()} == {
        provider: canonical_snapshot(reports) for provider, reports in second_run.items()
    }
    print(f"validated {total} scenarios")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
