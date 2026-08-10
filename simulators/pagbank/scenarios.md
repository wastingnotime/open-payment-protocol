# PagBank Pix Scenario Backlog

Built scenarios:

- `PB-PIX-001`: create and retrieve an order with one single-use QR Code and no charge.
- `PB-PIX-002`: reject a QR amount that differs from the item total.
- `PB-PIX-003`: return documented `409 idempotency_key_in_use`.
- `PB-PIX-004`: documented paid Pix charge emerges after QR payment.
- `PB-PIX-005`: unknown order retrieval preserves the native not-found boundary.
- `PB-PIX-006`: duplicate Pix payment preserves the native invalid-status boundary.
- `PB-PIX-007`: multiple QR codes preserve the native invalid-parameter boundary.

Deferred: QR expiration, Pix refund, webhook delivery,
and exact idempotency header/retention behavior.
