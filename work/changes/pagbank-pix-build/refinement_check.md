# PagBank Pix Build Refinement Check

## Evidence

Three deterministic scenarios pass. Creation projects a single QR Code with
integer-cent amount and an empty `charges` array; retrieval preserves the QR
copy text and image/base64 links. Reused keys produce the documented conflict.
Combined runtime inspection emitted 35 observations and preserved all three
PagBank scenario IDs. The `PB-PIX-001` observation proves the QR-first boundary
with `charges: []` at creation.
The paid-transition increment now emits 50 combined observations and shows a
`PAID` Pix charge emerging while the original QR Code remains on the order.

## Model Pressure

- PagBank has no charge at initial QR creation; charge emergence belongs to a
  later lifecycle increment.
- QR Code is single-use and attached directly to the order.
- Integer-cent money and order `reference_id` differ from the other built
  providers' representations.
- Runtime evidence must not create a synthetic charge merely because other
  providers expose a payment resource at creation.
- Charge emergence is a documented PagBank lifecycle event and remains distinct
  from initial QR creation.

## Remaining Questions

Payment-created charge state, expiry, Pix-specific refund behavior, webhook
delivery, and exact idempotency header/retention semantics require refinement.
