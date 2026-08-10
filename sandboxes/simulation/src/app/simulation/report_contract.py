"""Shared report-contract rules for tests and local validation tools."""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any
from types import MappingProxyType


__all__ = ["REPORT_FIELDS", "PROVIDER_ORDER", "PROVIDER_PREFIXES", "PROVIDER_SCENARIO_COUNTS", "TOTAL_SCENARIO_COUNT", "SECURITY_MARKERS", "ERROR_OBSERVATION_NAMES", "PROVIDER_NATIVE_WEBHOOK_EVENTS", "allowed_sources", "assert_sanitized", "canonical_snapshot", "error_inventory", "field", "observation_inventory", "validate_report"]


REPORT_FIELDS = ("name", "observations", "events", "projection")
PROVIDER_ORDER = ("asaas", "iugu", "mercadopago", "pagarme", "pagbank")
PROVIDER_PREFIXES: Mapping[str, str] = MappingProxyType({"asaas": "AS-", "iugu": "IUGU-", "mercadopago": "MP-", "pagarme": "PG-", "pagbank": "PB-"})
PROVIDER_SCENARIO_COUNTS: Mapping[str, int] = MappingProxyType({"asaas": 19, "iugu": 25, "mercadopago": 17, "pagarme": 14, "pagbank": 17})
TOTAL_SCENARIO_COUNT = sum(PROVIDER_SCENARIO_COUNTS.values())
SECURITY_MARKERS = ("pan", "cvv", "card_number", "api_key_value", "access_token_value", "secret_key_value")
ERROR_OBSERVATION_NAMES = frozenset(("native_error", "native_authentication_error"))
PROVIDER_NATIVE_WEBHOOK_EVENTS: Mapping[str, tuple[str, ...]] = MappingProxyType({
    "iugu": ("invoice.status_changed", "invoice.due", "invoice.payment_failed", "invoice.refund", "invoice.rejected", "invoice.partially_refunded", "invoice.refund_reverted", "invoice.created", "invoice.released"),
})


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


def observation_inventory(registries: Mapping[str, Mapping[str, Any]]) -> dict[str, dict[str, int]]:
    """Count each provider's native observation names without normalizing them."""
    return {
        provider: {
            name: sum(
                1
                for report in scenarios.values()
                for observation in field(report, "observations")
                if observation["name"] == name
            )
            for name in sorted({
                observation["name"]
                for report in scenarios.values()
                for observation in field(report, "observations")
            })
        }
        for provider, scenarios in registries.items()
    }


def error_inventory(registries: Mapping[str, Mapping[str, Any]]) -> dict[str, dict[str, int]]:
    """Count native error codes without classifying provider semantics."""
    return {
        provider: {
            code: sum(
                1
                for report in scenarios.values()
                for observation in field(report, "observations")
                if observation["name"] in ERROR_OBSERVATION_NAMES
                and observation["payload"].get("code") == code
            )
            for code in sorted({
                observation["payload"].get("code")
                for report in scenarios.values()
                for observation in field(report, "observations")
                if observation["name"] in ERROR_OBSERVATION_NAMES
                and observation["payload"].get("code")
            })
        }
        for provider, scenarios in registries.items()
    }


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
