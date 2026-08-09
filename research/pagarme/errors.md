# Pagar.me Error Research

## Metadata

- Research date: 2026-08-09
- Source: official Pagar.me Markdown documentation
- Evidence level: documented; not test-observed

## Current Evidence

The create-order OpenAPI reference documents HTTP 400 but provides an empty
object example and schema. The reviewed pages do not establish a stable error
envelope, provider error codes, validation mapping, authentication errors,
not-found response, or retryability.

## Rate Limits

- Test accounts: 10 requests per second for any endpoint.
- `GET /charges/*`: 200 requests per minute.
- `GET /orders/*`: 200 requests per minute.
- `GET /hooks/*`: 50 requests per minute.
- For Pix charge cancellation, after the tenth attempt on the same charge, only
  one new attempt is allowed every 15 minutes.

The reviewed rate-limit page does not specify the response body, HTTP status,
or headers returned when a limit is exceeded.

## Unknown Result Boundary

No create-order idempotency contract was found. Transport timeout or server
failure after `POST /orders` must therefore be modeled as an unknown result
until documentation or test observations establish reconciliation behavior.
Automatic create retry is not justified by current evidence.

[create]: https://docs.pagar.me/reference/criar-pedido-2
[rate]: https://docs.pagar.me/reference/rate-limit
