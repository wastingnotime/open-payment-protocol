# Asaas Pix Build Refinement Check

## Evidence

Eight deterministic scenarios pass. Creation preserves a `pay_` payment ID,
`PIX` billing type, decimal JSON value, and `PENDING` status. QR data is
retrieved through a separate provider operation and is not added to the
payment projection.

## Model Pressure

- Asaas's separate QR endpoint differs from embedded Pix output in Iugu,
  Mercado Pago, and Pagar.me.
- Decimal JSON number precision remains an explicit unknown.
- No repetition or external-reference uniqueness behavior is invented.
- The unknown-payment scenario preserves a native 404 boundary without
  inventing lookup or reconciliation semantics.
- The unknown QR scenario keeps the separate QR operation's 404 boundary
  distinct from payment retrieval.
- QR retrieval is only valid for an existing payment and does not create or
  infer a payment when the billing type is unsupported.
- Payment creation requires a strictly positive value; zero and negative
  values remain provider-native validation errors.
- The documented payment create shape requires customer, billing type, value,
  and due date; omitted fields remain native required-parameter failures.

The focused test and scenario inventory are covered by the current build.

## Discrepancies and Unknowns

- Decimal JSON-number precision remains unknown.
## Remaining Questions

Lifecycle, QR expiration, webhooks, repetition, external-reference lookup, and
sandbox behavior require refinement.
