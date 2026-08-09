# Iugu Error Research

## Metadata

- Research date: 2026-08-09
- Source interface: official Iugu developer MCP
- Evidence level: documented OpenAPI only; not test-mode observed

## Current Evidence

The `POST /invoices`, `GET /invoices/{id}`, and `GET /resource_search`
definitions document an HTTP 400 response, but their examples and schemas are
empty JSON objects. The MCP output reviewed in this pass does not define:

- provider error codes or message fields;
- authentication failure responses;
- not-found behavior;
- rate-limit responses or headers;
- retryability;
- conflict semantics for caller references;
- server-error or unknown-result semantics.

All of these behaviors remain `Unknown`. A faithful simulator must not copy the
Asaas error envelope or invent a canonical error at the Iugu boundary.

## Unknown Result Boundary

No create-request idempotency key was documented. `order_id` is described as
helping avoid payment of the same invoice, which is not evidence that invoice
creation is idempotent. Transport timeouts and 5xx results must be treated as
unknown until documentation or test-mode observations establish otherwise.

[create]: https://dev.iugu.com/reference/criar-fatura
[retrieve]: https://dev.iugu.com/mcp
[search]: https://dev.iugu.com/reference/buscar-fatura-por-ids-externos
