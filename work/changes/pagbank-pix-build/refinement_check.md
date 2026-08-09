# PagBank Pix Build Refinement Check

## Evidence

Three deterministic scenarios pass. Creation projects a single QR Code with
integer-cent amount and an empty `charges` array; retrieval preserves the QR
copy text and image/base64 links. Reused keys produce the documented conflict.

## Model Pressure

- PagBank has no charge at initial QR creation; charge emergence belongs to a
  later lifecycle increment.
- QR Code is single-use and attached directly to the order.
- Integer-cent money and order `reference_id` differ from the other built
  providers' representations.

## Remaining Questions

Payment-created charge state, expiry, Pix-specific refund behavior, webhook
delivery, and exact idempotency header/retention semantics require refinement.
