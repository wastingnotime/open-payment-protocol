# Mercado Pago Error Research

## Create-Order Evidence

The reference documents structured error codes including:

- HTTP 400 for missing/invalid idempotency headers, malformed JSON, property
  validation, and a `total_amount` mismatch;
- HTTP 401 for access-token problems;
- HTTP 402 when the order is created but a transaction fails;
- HTTP 409 `idempotency_key_already_used`;
- HTTP 429 for request limits, with `Retry-After` documented by the Pix guide;
- HTTP 500 `internal_error`, whose description says to submit again.

The exact JSON error envelope and whether every code uses it consistently still
require fixtures. A blind retry after HTTP 500 conflicts with the uniqueness
rules unless the idempotency replay behavior is clarified; model the result as
unknown and reconcile by order ID when one was received.

[create]: https://www.mercadopago.com.br/developers/en/reference/online-payments/checkout-api/create-order/post
[pix]: https://www.mercadopago.com.br/developers/en/docs/checkout-api-orders/payment-integration/pix
