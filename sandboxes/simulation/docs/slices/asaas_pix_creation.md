# Asaas Pix Payment Creation and QR Retrieval

Status: creation, documented validation, and bounded webhook event/redelivery
boundaries built; refinement checks recorded in
`work/changes/asaas-pix-build/refinement_check.md` and
`work/changes/asaas-pix-webhook-build/`.

The shared simulation preserves Asaas's `payment` resource, decimal JSON value,
`PENDING` status, `PIX` billing type, and separate
`GET /v3/payments/{id}/pixQrCode` output. QR data is not embedded into the
payment projection.

Executable scenarios are `AS-PIX-001` through `AS-PIX-011` in
`simulators/asaas/scenarios.md`.

The lifecycle/event increment adds `AS-PIX-009` for `PAYMENT_RECEIVED`,
`AS-PIX-010` for stable-ID redelivery, and `AS-PIX-011` for
`PAYMENT_OVERDUE`. Response-status transitions, retries, acknowledgement
codes, and ordering guarantees remain unknown.

Out of scope: expiry, repetition, external-reference lookup, and sandbox
behavior.
