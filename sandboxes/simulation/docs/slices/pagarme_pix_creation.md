# Pagar.me Pix Order, Charge, and Transaction Creation

Status: first build complete; refinement check pending.

The shared simulation preserves Pagar.me's `order → charge → last_transaction`
hierarchy, integer amounts, pending native status, and embedded Pix QR fields.
It does not collapse the three provider identities into one resource.

Executable scenarios are `PG-PIX-001` and `PG-PIX-002` in
`simulators/pagarme/scenarios.md`.

Out of scope: payment outcomes, expiry, webhooks, idempotency, refunds, and
provider sandbox behavior.
