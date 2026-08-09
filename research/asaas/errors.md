# Asaas Error Research

## Metadata

- Research date: 2026-08-09
- Source interface: official Asaas documentation MCP
- Evidence level: documented; not Sandbox-observed

## Shape and HTTP Semantics

Errors are JSON with an `errors` array. Each item contains a provider-native
`code` and human-readable `description`.

| HTTP status | Documented meaning |
| --- | --- |
| 400 | Required parameter missing or invalid; response describes the problem. |
| 401 | API key missing or invalid. |
| 403 | Unauthorized request, abuse/prohibited parameters, or a GET request carrying a body. |
| 404 | Endpoint or object does not exist. |
| 429 | Concurrency, quota, or endpoint rate limit exceeded. |
| 500 | Internal Asaas error. |

Sources: [HTTP response codes][responses] and [API limits][limits].

Documented create-payment examples include:

```json
{
  "errors": [
    {
      "code": "invalid_customer",
      "description": "Customer Inválido ou não informado"
    }
  ]
}
```

Authentication documentation additionally identifies `invalid_environment`,
`access_token_not_found`, `invalid_access_token_format`, and
`invalid_access_token` as 401 error codes.

## Limits

- Up to 50 concurrent GET requests are documented.
- An account quota of 25,000 API requests per 12-hour window is documented.
- Endpoint-specific rate-limit state may be returned through
  `RateLimit-Limit`, `RateLimit-Remaining`, and `RateLimit-Reset` headers.
- Exceeding these limits returns HTTP 429.

## Unknown Result Boundary

The reviewed material does not document whether a 500 response or transport
timeout on `POST /v3/payments` means the payment definitely failed, nor does it
document a create-request idempotency key. The simulator must not infer safe
automatic retry behavior.

[auth]: https://docs.asaas.com/docs/authentication-2
[limits]: https://docs.asaas.com/docs/api-limits-1
[responses]: https://docs.asaas.com/reference/http-response-codes
