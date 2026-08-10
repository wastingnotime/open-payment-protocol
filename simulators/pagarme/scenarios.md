# Pagar.me Pix Scenario Backlog

Built scenarios:

- `PG-PIX-001`: create an order and retrieve its native charge/transaction.
- `PG-PIX-002`: reject a request missing required order data.
- `PG-PIX-003`: documented Pix simulator success for amount ≤ BRL 500.
- `PG-PIX-004`: documented Pix simulator failure for amount > BRL 500.
- `PG-PIX-005`: unknown charge retrieval preserves the native not-found boundary.
- `PG-PIX-006`: non-Pix payment method preserves the native invalid-parameter boundary.

Deferred: production timing, charge retrieval errors, expiration, webhooks, and
idempotency behavior (not established in evidence).
