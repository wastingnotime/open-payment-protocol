# PagBank Error Research

## Envelope

Documented client errors return an `error_messages` array. Entries expose a
numeric/string `code`, description, parameter name, and error text. The catalog
includes validation, authentication, permission, not-found, idempotency, rate
limit, refund, and internal-server failures across HTTP 400, 401, 403, 404,
409, and 500.

Notable codes include `40004 rate_limit`, `40005 idempotency_key_in_use`,
`40007 unabled_refund`, `40008 refund_temporarily_unavailable`, and
`internal_server_error`.

## Retry Boundary

Idempotency documentation says the same key always returns the same response,
which supports replay after an inconclusive transport failure. Exact behavior
while a key is concurrently in use, and retry guidance for rate limits and 500
responses, remain unknown.

[errors]: https://developer.pagbank.com.br/reference/codigos-de-erro-order
[idempotency]: https://developer.pagbank.com.br/docs/chaves-publicas-e-de-idempotencia
