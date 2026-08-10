# Mercado Pago Pix Build Refinement Check

## Evidence

Four deterministic scenarios pass. The projection retains an order containing
one payment transaction, decimal-string amounts, QR output, and native
`action_required/waiting_transfer` status. Reused idempotency keys produce the
documented HTTP 409 code. Runtime inspection now exposes native order-created,
rejected, and idempotency-conflict events as semantic observations.

## Model Pressure

- Mercado Pago's order and payment identifiers remain separate from Iugu's
  invoice identifier.
- Decimal-string money cannot be represented by the Iugu integer-cent field
  shape without losing provider fidelity.
- The API requires idempotency, but repeated-key replay semantics remain unknown.
- Provider-native events need explicit semantic observations in addition to the
append-only event store for runtime inspection and later adapter pressure.
- The documented asynchronous variant retains `processing` with no payment
  information; later reconciliation is explicitly through webhook or GET.
- Runtime inspection confirms the `processing` result is correlated as
  `MP-PIX-004` without fabricating a payment transaction.
- `MP-PIX-005` confirms GET reconciliation returns the same `processing` order
  with no payment information, preserving the documented unknown-result
  boundary.
- Unknown order retrieval remains a native 404 boundary and is distinct from
  asynchronous reconciliation of a known processing order.

## Remaining Questions

Asynchronous finalization, successful transfer transitions, notification
delivery, and refund behavior require their own refinement evidence.
