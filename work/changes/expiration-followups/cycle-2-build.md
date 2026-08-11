# Pagar.me and PagBank expiration — refinement/build cycle 2

Pagar.me and PagBank expiration remain separate provider-native candidates.

Pagar.me documents Pix transaction outcomes but not an unpaid-QR expiry transition. PagBank exposes QR expiration input but not a documented post-expiry order, QR, or charge projection.

Build result: no expiration scenarios added; Mercado Pago remains the only executable expiration slice.

Validation: `pytest -q sandboxes/simulation/tests` — 157 passed; `python3 sandboxes/simulation/tools/validate_scenarios.py` — 93 scenarios validated.

