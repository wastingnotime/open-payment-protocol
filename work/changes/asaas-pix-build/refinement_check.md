# Asaas Pix Build Refinement Check

## Evidence

Two deterministic scenarios pass. Creation preserves a `pay_` payment ID,
`PIX` billing type, decimal JSON value, and `PENDING` status. QR data is
retrieved through a separate provider operation and is not added to the payment
projection.

## Model Pressure

- Asaas's separate QR endpoint differs from embedded Pix output in Iugu,
  Mercado Pago, and Pagar.me.
- Decimal JSON number precision remains an explicit unknown.
- No repetition or external-reference uniqueness behavior is invented.
- The unknown-payment scenario preserves a native 404 boundary without
  inventing lookup or reconciliation semantics.
- The unknown QR scenario keeps the separate QR operation's 404 boundary
  distinct from payment retrieval.

## Remaining Questions

Lifecycle, QR expiration, webhooks, repetition, external-reference lookup, and
sandbox behavior require refinement.
