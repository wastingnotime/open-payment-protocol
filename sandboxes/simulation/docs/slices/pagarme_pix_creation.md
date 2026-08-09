# Pagar.me Pix Order, Charge, and Transaction Creation

Status: creation and documented simulator transition build complete.

The shared simulation preserves Pagar.me's `order → charge → last_transaction`
hierarchy, integer amounts, pending native status, and embedded Pix QR fields.
It does not collapse the three provider identities into one resource.

Executable scenarios are `PG-PIX-001` through `PG-PIX-004` in
`simulators/pagarme/scenarios.md`.

Out of scope: production timing, expiry, webhooks, idempotency, refunds, and
provider sandbox behavior.
