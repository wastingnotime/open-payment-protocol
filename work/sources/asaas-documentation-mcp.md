# Asaas Documentation MCP Source Record

- Provider: Asaas
- Source type: official documentation MCP and underlying official pages/OpenAPI
- MCP endpoint: `https://docs.asaas.com/mcp`
- Access date: 2026-08-09
- MCP server identity: `Asaas - Documentação API`, version `3`
- Negotiated MCP protocol version: `2025-03-26`
- Authentication used: none
- Live Asaas API requests made: none

## MCP Tools Used

- `list-specs`
- `search`
- `fetch`
- `search-endpoints`
- `get-endpoint`

The `execute-request` tool was deliberately not used. This research pass queried
documentation only and did not possess or request an Asaas API key.

## Material Retrieved

- Pix payment creation and QR Code guide;
- Pix overview;
- `POST /v3/payments` OpenAPI operation and schemas;
- `GET /v3/payments/{id}` OpenAPI operation and schemas;
- `GET /v3/payments/{id}/pixQrCode` OpenAPI operation and schemas;
- payment events and documented Pix event flows;
- webhook at-least-once/idempotency guidance;
- authentication guidance;
- API limits and HTTP response codes.

Repository research files contain curated facts and direct official-page URLs.
Large raw MCP responses are not committed because they include the complete,
evolving OpenAPI component graph and a large sample Base64 QR image. They can be
re-queried from the recorded official MCP source.
