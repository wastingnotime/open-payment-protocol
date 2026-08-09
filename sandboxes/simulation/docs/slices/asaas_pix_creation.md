# Asaas Pix Payment Creation and QR Retrieval

Status: first build complete; refinement check pending.

The shared simulation preserves Asaas's `payment` resource, decimal JSON value,
`PENDING` status, `PIX` billing type, and separate
`GET /v3/payments/{id}/pixQrCode` output. QR data is not embedded into the
payment projection.

Executable scenarios are `AS-PIX-001` and `AS-PIX-002` in
`simulators/asaas/scenarios.md`.

Out of scope: lifecycle transitions, expiry, webhooks, repetition,
external-reference lookup, and sandbox behavior.
