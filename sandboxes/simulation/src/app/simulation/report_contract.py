"""Shared report-contract rules for tests and local validation tools."""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any


__all__ = ["REPORT_FIELDS", "PROVIDER_PREFIXES", "PROVIDER_SCENARIO_COUNTS", "allowed_sources", "canonical_snapshot", "field", "validate_report"]


REPORT_FIELDS = ("name", "observations", "events", "projection")
PROVIDER_PREFIXES = {"asaas": "AS-", "iugu": "IUGU-", "mercadopago": "MP-", "pagarme": "PG-", "pagbank": "PB-"}
PROVIDER_SCENARIO_COUNTS = {"asaas": 8, "iugu": 13, "mercadopago": 10, "pagarme": 9, "pagbank": 10}


def field(report: Any, name: str) -> Any:
    return report[name] if isinstance(report, dict) else getattr(report, name)


def allowed_sources(provider: str) -> set[str]:
    return {provider, "simulation"} if provider == "iugu" else {provider}


def canonical_snapshot(reports: Mapping[str, Any]) -> str:
    return json.dumps(
        [{name: field(report, name) for name in REPORT_FIELDS} for report in sorted(reports.values(), key=lambda item: field(item, "name"))],
        sort_keys=True,
        separators=(",", ":"),
    )


def validate_report(provider: str, scenario_id: str, report: Any) -> None:
    assert scenario_id.startswith(PROVIDER_PREFIXES[provider])
    assert field(report, "name") == scenario_id
    assert isinstance(field(report, "events"), list)
    assert isinstance(field(report, "projection"), dict)
    observations = field(report, "observations")
    assert observations
    for observation in observations:
        assert {"type", "name", "source", "payload"} <= observation.keys()
        assert observation["source"] in allowed_sources(provider)
        assert observation["payload"]["scenario"] == scenario_id
