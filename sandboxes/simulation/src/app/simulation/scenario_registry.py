"""Single registry of provider-native scenario runners."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .asaas_scenarios import run_all as run_asaas
from .mercadopago_scenarios import run_all as run_mercado_pago
from .pagarme_scenarios import run_all as run_pagarme
from .pagbank_scenarios import run_all as run_pagbank
from .scenarios import run_all as run_iugu

PROVIDER_RUNNERS: dict[str, Callable[[], dict[str, Any]]] = {
    "asaas": run_asaas,
    "iugu": run_iugu,
    "mercadopago": run_mercado_pago,
    "pagarme": run_pagarme,
    "pagbank": run_pagbank,
}


def run_all_providers() -> dict[str, dict[str, Any]]:
    return {provider: runner() for provider, runner in PROVIDER_RUNNERS.items()}
