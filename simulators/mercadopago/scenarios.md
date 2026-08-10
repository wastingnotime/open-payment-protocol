# Mercado Pago Pix Scenario Backlog

Built scenarios:

- `MP-PIX-001`: create and retrieve an Orders API Pix order.
- `MP-PIX-002`: reject a transaction amount that differs from `total_amount`.
- `MP-PIX-003`: return documented `409 idempotency_key_already_used`.
- `MP-PIX-004`: represent documented asynchronous order creation with
  `processing` and no payment information.
- `MP-PIX-005`: reconcile that asynchronous order through GET.
- `MP-PIX-006`: unknown order retrieval preserves the native not-found boundary.
- `MP-PIX-007`: non-Pix payment method preserves the native property-value boundary.

Deferred: asynchronous finalization, successful transfer, expiration, webhooks,
refunds, and legacy Payments API compatibility.
