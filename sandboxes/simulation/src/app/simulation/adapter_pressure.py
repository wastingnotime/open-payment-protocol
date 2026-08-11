"""Thin comparison report for adapter-pressure discovery.

This is an experimental observation surface. It deliberately reports native
provider differences and does not define a shared payment model.
"""

from __future__ import annotations

from typing import Any

from .report_contract import observation_inventory
from .scenario_registry import run_all_providers


NATIVE_SHAPES = {
    "asaas": {"resource": "payment", "qr": "separate_retrieval", "money": "decimal_json_number"},
    "iugu": {"resource": "invoice", "qr": "embedded_pix", "money": "integer_cents"},
    "mercadopago": {"resource": "order_payment", "qr": "embedded_payment", "money": "decimal_string"},
    "pagbank": {"resource": "order_qr_charge", "qr": "embedded_qr_then_charge", "money": "integer_cents"},
    "pagarme": {"resource": "order_charge_transaction", "qr": "embedded_transaction", "money": "integer_amount"},
}


def build_pressure_report() -> dict[str, Any]:
    registries = run_all_providers()
    inventory = observation_inventory(registries)
    return {
        provider: {
            "scenario_count": len(registries[provider]),
            "native_shape": dict(NATIVE_SHAPES[provider]),
            "observation_names": tuple(sorted(inventory[provider])),
        }
        for provider in NATIVE_SHAPES
    }
