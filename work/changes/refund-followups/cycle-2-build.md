# Provider refunds and cancellation — refinement/build cycle 2

The refund boundary remains provider-native.

Mercado Pago partial/total refunds and PagBank partial/full charge cancellations remain executable. Asaas, Iugu, and Pagar.me still lack sufficient evidence for faithful Pix refund projections; PagBank Pix-specific post-cancellation behavior also remains unknown.

Build result: no shared refund state and no unsupported provider operation added.

Validation: `pytest -q sandboxes/simulation/tests` — 157 passed; `python3 sandboxes/simulation/tools/validate_scenarios.py` — 93 scenarios validated.

