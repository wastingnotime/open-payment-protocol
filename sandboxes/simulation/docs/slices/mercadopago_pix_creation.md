# Mercado Pago Pix Order Creation and Retrieval

Status: creation, asynchronous variant, notification authenticity, and
documented validation boundaries
built; refinement check recorded in
`work/changes/mercadopago-pix-build/refinement_check.md`.

The shared simulation preserves Mercado Pago's Orders API order/payment
hierarchy, decimal-string amounts, `action_required/waiting_transfer` initial
state, embedded Pix QR fields, mandatory idempotency conflict, and native
validation error. It does not reuse the Iugu invoice aggregate.

Executable scenarios are `MP-PIX-001` through `MP-PIX-010` in
`simulators/mercadopago/scenarios.md`.

The lifecycle/event increment adds `MP-PIX-011` for an `order` JSON
notification with GET reconciliation and `MP-PIX-012` for mismatched signature
discard. Timestamp tolerance, retries, acknowledgements, ordering, and
duplicate guarantees remain unknown.

Out of scope: asynchronous omission, payment success, expiration, refunds,
legacy Payments API, and any normalized OPP model.
