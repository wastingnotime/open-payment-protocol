# Mercado Pago Pix Scenario Backlog

Built scenarios:

- `MP-PIX-001`: create and retrieve an Orders API Pix order.
- `MP-PIX-002`: reject a transaction amount that differs from `total_amount`.
- `MP-PIX-003`: return documented `409 idempotency_key_already_used`.

Deferred: asynchronous creation, successful transfer, expiration, webhooks,
refunds, and legacy Payments API compatibility.
