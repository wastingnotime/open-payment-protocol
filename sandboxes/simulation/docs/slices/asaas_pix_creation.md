# Asaas Pix Payment Creation and QR Retrieval

Status: creation and documented validation boundaries built; refinement check
recorded in `work/changes/asaas-pix-build/refinement_check.md`.

The shared simulation preserves Asaas's `payment` resource, decimal JSON value,
`PENDING` status, `PIX` billing type, and separate
`GET /v3/payments/{id}/pixQrCode` output. QR data is not embedded into the
payment projection.

Executable scenarios are `AS-PIX-001` through `AS-PIX-008` in
`simulators/asaas/scenarios.md`.

Out of scope: lifecycle transitions, expiry, webhooks, repetition,
external-reference lookup, and sandbox behavior.
