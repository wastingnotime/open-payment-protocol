# Pagar.me Pix Order, Charge, and Transaction Creation

Status: creation, documented transition, and caller-reference validation build
complete; refinement check recorded in
`work/changes/pagarme-pix-build/refinement_check.md`.

The shared simulation preserves Pagar.me's `order → charge → last_transaction`
hierarchy, integer amounts, pending native status, and embedded Pix QR fields.
It does not collapse the three provider identities into one resource.

Executable scenarios are `PG-PIX-001` through `PG-PIX-009` in
`simulators/pagarme/scenarios.md`.

Out of scope: production timing, expiry, webhooks, idempotency, refunds, and
provider sandbox behavior.
