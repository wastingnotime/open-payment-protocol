# Pagar.me Pix Build Refinement Check

## Evidence

Two deterministic scenarios pass. Creation preserves separate order, charge,
and Pix transaction identifiers, pending status, integer amount, and embedded
`qr_code`/`qr_code_url` fields. Invalid creation remains provider-native.

## Model Pressure

- Pagar.me's order → charge → transaction hierarchy differs from the QR-first
  PagBank order and Mercado Pago order/payment hierarchy.
- The charge's `last_transaction` is the native Pix output boundary.
- No create idempotency guarantee is invented because the reviewed evidence is
  unknown.

## Remaining Questions

Deterministic Pix success/failure rules, charge retrieval errors, expiry,
webhooks, refunds, and sandbox behavior require refinement.
