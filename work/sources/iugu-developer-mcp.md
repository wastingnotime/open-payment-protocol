# Iugu Developer MCP Source Record

- Provider: Iugu
- Source type: official developer MCP and returned OpenAPI definitions
- MCP endpoint: `https://dev.iugu.com/mcp`
- Access date: 2026-08-09
- MCP server identity: `Central do Desenvolvedor`, version `1.0`
- Negotiated MCP protocol version: `2025-03-26`
- Authentication used: none
- Live Iugu API requests made: none

## MCP Tools Used

- `list-specs`
- `search-endpoints`
- `list-endpoints`
- `get-endpoint`

The MCP does not currently advertise documentation `search` or `fetch` tools.
The `execute-request` tool was deliberately not used.

## Material Retrieved

- `faturas`: create invoice, retrieve invoice, and external-ID search;
- `gatilhos`: supported events and trigger creation;
- the endpoint security schemes, request fields, response examples, and HTTP
  response declarations associated with those operations.

Repository research files contain curated facts and sanitized fixtures. Raw MCP
responses are not committed because the invoice examples include realistic
personal-looking payer data and large payment payloads. They can be re-queried
from the recorded official MCP source.
