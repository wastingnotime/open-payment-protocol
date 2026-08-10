# Pagar.me Pix Order, Charge, and Transaction Creation

Status: creation, documented transition, and caller-reference validation build
complete; refinement check recorded in
`work/changes/pagarme-pix-build/refinement_check.md`.

The shared simulation preserves Pagar.me's `order → charge → last_transaction`
hierarchy, integer amounts, pending native status, and embedded Pix QR fields.
It does not collapse the three provider identities into one resource.

Executable scenarios are `PG-PIX-001` through `PG-PIX-011` in
`simulators/pagarme/scenarios.md`.

The lifecycle/event-delivery increment adds `PG-PIX-010` for a paid outcome
with one `charge.paid` delivery marked `sent`, and `PG-PIX-011` for a failed
delivery attempt marked `failed`. Retry timing, ordering, duplicates,
authentication, and exact webhook payload schemas remain unknown.

Out of scope: production timing, expiry, idempotency, refunds, and provider
sandbox behavior.
