# Pagar.me Pix Build Refinement Check

## Evidence

Four deterministic scenarios pass. Creation preserves separate order, charge,
and Pix transaction identifiers, pending status, integer amount, and embedded
`qr_code`/`qr_code_url` fields. Invalid creation remains provider-native.
Combined runtime inspection emitted 39 observations and preserved both
Pagar.me scenario IDs. The `PG-PIX-001` trace exposes distinct order, charge,
and transaction IDs plus the charge's Pix `last_transaction` QR value.
The documented Pix simulator threshold is now exercised: amounts up to BRL
500 become `paid`, while larger amounts become `failed`, with order, charge,
and transaction statuses updated independently but consistently.
Runtime inspection emitted 48 observations and preserved all four Pagar.me
scenario IDs. The transition traces confirm the three native status levels are
visible together without introducing a normalized status enum.

## Model Pressure

- Pagar.me's order → charge → transaction hierarchy differs from the QR-first
  PagBank order and Mercado Pago order/payment hierarchy.
- The charge's `last_transaction` is the native Pix output boundary.
- No create idempotency guarantee is invented because the reviewed evidence is
  unknown.
- Runtime observations must retain all three provider identifiers so later
  adapter experiments cannot accidentally collapse the hierarchy.
- Simulator thresholds are sandbox rules, not production lifecycle guarantees.
- The success/failure threshold is now an explicit provider simulator rule with
  a source link, not an inferred production behavior.
- Unknown charge retrieval preserves the native 404 `charge_not_found` boundary
  and does not infer an order lookup fallback.
- Pix outcome simulation applies the documented amount threshold once per
  charge and keeps order, charge, and transaction statuses aligned.

## Remaining Questions

Production Pix timing, charge retrieval errors, expiry, webhooks, refunds, and
other sandbox behavior require refinement.
