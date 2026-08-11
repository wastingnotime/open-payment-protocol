# Asaas Pix transition refinement

## Decision

Keep the Asaas success transition deferred. The official collection-payment
evidence documents `PAYMENT_CREATED -> PAYMENT_RECEIVED` and a broad payment
status vocabulary, but it does not establish the exact Pix create response,
the relationship between `RECEIVED` and `CONFIRMED`, or transition timing.

The unrelated "Possible Statuses" page describes bill-payment execution and
must not be imported into the collection-payment simulator.

## Build gate

No success-transition scenario is added until collection-specific evidence or
sanitized Sandbox observation establishes the status projection. Existing
`AS-PIX-009` through `AS-PIX-012` remain the bounded event/envelope build, and
the native graph keeps `AS-PIX-DEFERRED-SUCCESS` explicit.

## Evidence

- `research/asaas/lifecycle.md`
- `research/asaas/webhooks.md`
- `https://docs.asaas.com/docs/webhooks-events`
