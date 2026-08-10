"""Shared report-contract rules for tests and local validation tools."""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any
from types import MappingProxyType


__all__ = ["REPORT_FIELDS", "PROVIDER_ORDER", "PROVIDER_PREFIXES", "PROVIDER_SCENARIO_COUNTS", "SECURITY_MARKERS", "allowed_sources", "assert_sanitized", "canonical_snapshot", "field", "validate_report"]


REPORT_FIELDS = ("name", "observations", "events", "projection")
PROVIDER_ORDER = ("asaas", "iugu", "mercadopago", "pagarme", "pagbank")
PROVIDER_PREFIXES: Mapping[str, str] = MappingProxyType({"asaas": "AS-", "iugu": "IUGU-", "mercadopago": "MP-", "pagarme": "PG-", "pagbank": "PB-"})
PROVIDER_SCENARIO_COUNTS: Mapping[str, int] = MappingProxyType({"asaas": 8, "iugu": 17, "mercadopago": 10, "pagarme": 14, "pagbank": 14})
SECURITY_MARKERS = ("pan", "cvv", "card_number", "api_key", "access_token", "secret_key")


def field(report: Any, name: str) -> Any:
    try:
        return report[name] if isinstance(report, Mapping) else getattr(report, name)
    except (KeyError, AttributeError, TypeError) as exc:
        raise AssertionError(f"report is missing required field: {name}") from exc


def allowed_sources(provider: str) -> frozenset[str]:
    return frozenset((provider, "simulation")) if provider == "iugu" else frozenset((provider,))


def assert_sanitized(serialized: str) -> None:
    lowered = serialized.lower()
    for marker in SECURITY_MARKERS:
        assert marker not in lowered, f"serialized report contains prohibited marker: {marker}"


def canonical_snapshot(reports: Mapping[str, Any]) -> str:
    return json.dumps(
        [{name: field(report, name) for name in REPORT_FIELDS} for report in sorted(reports.values(), key=lambda item: field(item, "name"))],
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def validate_report(provider: str, scenario_id: str, report: Any) -> None:
    context = f"{provider}/{scenario_id}"
    assert provider in PROVIDER_PREFIXES, f"{context}: unknown provider"
    assert scenario_id.startswith(PROVIDER_PREFIXES[provider]), f"{context}: invalid provider prefix"
    assert field(report, "name") == scenario_id, f"{context}: report name mismatch"
    events = field(report, "events")
    assert isinstance(events, list), f"{context}: events must be a list"
    assert all(isinstance(event, Mapping) for event in events), f"{context}: event items must be mappings"
    assert isinstance(field(report, "projection"), dict), f"{context}: projection must be a mapping"
    observations = field(report, "observations")
    assert isinstance(observations, list) and observations, f"{context}: observations must be a non-empty list"
    for observation in observations:
        assert isinstance(observation, Mapping), f"{context}: observation must be a mapping"
        assert {"type", "name", "source", "payload"} <= observation.keys(), f"{context}: incomplete observation envelope"
        assert observation["source"] in allowed_sources(provider), f"{context}: invalid observation source"
        payload = observation["payload"]
        assert isinstance(payload, Mapping), f"{context}: observation payload must be a mapping"
        assert payload.get("scenario") == scenario_id, f"{context}: observation attribution mismatch"
