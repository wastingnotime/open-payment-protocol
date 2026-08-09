# Mercado Pago Pix Order Creation and Retrieval

Status: creation and documented asynchronous variant built; refinement pending.

The shared simulation preserves Mercado Pago's Orders API order/payment
hierarchy, decimal-string amounts, `action_required/waiting_transfer` initial
state, embedded Pix QR fields, mandatory idempotency conflict, and native
validation error. It does not reuse the Iugu invoice aggregate.

Executable scenarios are `MP-PIX-001` through `MP-PIX-004` in
`simulators/mercadopago/scenarios.md`.

Out of scope: asynchronous omission, payment success, expiration, webhooks,
refunds, legacy Payments API, and any normalized OPP model.
