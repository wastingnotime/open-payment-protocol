# Iugu Error Research

## Metadata

- Research date: 2026-08-09
- Sources: official Iugu MCP and Markdown documentation
- Evidence level: documented; not test-mode observed

## Authentication Errors

HTTP 401 is documented for an unverified subaccount, missing or wrong-account
token, use of `api_token` where `user_token` is required, a token awaiting
administrator approval, or a disallowed source IP.

## Create-Invoice Validation

For `POST /v1/invoices`, the error reference distinguishes:

- HTTP 400, including missing `due_date`;
- HTTP 422, including blank email when `customer_id` is null, invalid email,
  invalid or past due date, missing items, invalid customer, invalid
  `payable_with`, non-integer item price/quantity, and daily invoice limit.

The documented payer-validation rows specifically mention boleto, not Pix,
reinforcing the unresolved Pix payer conflict.

## Idempotency Conflict

The idempotency guide says a repeated `Idempotency-Key` returns HTTP 409 after
one request is processed. Its error body is shown only as an image.

## Remaining Unknowns

MCP response examples use empty objects for HTTP 400 and define no consistent
machine-readable error schema. Not-found retrieval, rate limits, retryability,
stable error codes, server failures, and unknown-result semantics remain open.

Invoice creation supports idempotency, but retention, concurrent requests,
replay response, and payload mismatch remain unspecified. Transport timeouts
and 5xx outcomes still require test-mode evidence.

[errors]: https://dev.iugu.com/reference/erros
[idempotency]: https://dev.iugu.com/docs/chave-de-idempot%C3%AAncia-1
