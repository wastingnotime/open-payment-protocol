# Pagar.me Pix Order, Charge, and Transaction Creation

Status: creation, documented transition, caller-reference, and bounded webhook
delivery/query/resend build complete; refinement checks recorded in
`work/changes/pagarme-pix-build/refinement_check.md` and
`work/changes/pagarme-pix-webhook-build/refinement_check.md`.

The shared simulation preserves Pagar.me's `order → charge → last_transaction`
hierarchy, integer amounts, pending native status, and embedded Pix QR fields.
It does not collapse the three provider identities into one resource.

Executable scenarios are `PG-PIX-001` through `PG-PIX-014` in
`simulators/pagarme/scenarios.md`.

The lifecycle/event-delivery increment adds `PG-PIX-010` for a paid outcome
with one `charge.paid` delivery marked `sent`, `PG-PIX-011` for a failed
delivery attempt marked `failed`, `PG-PIX-012` for a manual resend,
`PG-PIX-013` for querying delivery state, and `PG-PIX-014` for the distinct
`order.paid` event. Retry timing, ordering, duplicates, authentication, and
exact webhook payload schemas remain unknown.

Out of scope: production timing, expiry, idempotency, refunds, and provider
sandbox behavior.
