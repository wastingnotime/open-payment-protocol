# Mercado Pago Pix Build Refinement Check

## Evidence

Three deterministic scenarios pass. The projection retains an order containing
one payment transaction, decimal-string amounts, QR output, and native
`action_required/waiting_transfer` status. Reused idempotency keys produce the
documented HTTP 409 code.

## Model Pressure

- Mercado Pago's order and payment identifiers remain separate from Iugu's
  invoice identifier.
- Decimal-string money cannot be represented by the Iugu integer-cent field
  shape without losing provider fidelity.
- The API requires idempotency, but repeated-key replay semantics remain unknown.

## Remaining Questions

Asynchronous order creation, successful transfer transitions, notification
delivery, and refund behavior require their own refinement evidence.
