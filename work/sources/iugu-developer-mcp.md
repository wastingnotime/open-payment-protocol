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

## Complementary Markdown Discovery

The official `https://dev.iugu.com/llms.txt` index was accessed on 2026-08-09.
Iugu serves page content as `text/markdown` by appending `.md` to documentation
and reference paths. Relevant pages record their own `updatedAt` timestamp.

The expanded pass used authentication, payment-method activation, invoices,
Pix-by-API, invoice statuses, idempotency, triggers, invoice-trigger payloads,
and error-reference pages.

| Page | Reported `updatedAt` |
| --- | --- |
| Authentication reference | 2026-07-28T20:16:41.000Z |
| Authentication tokens | 2026-07-30T14:51:01.000Z |
| Enable payment methods through API | 2026-08-03T14:48:26.000Z |
| Error reference | 2026-08-04T15:04:58.000Z |
| Invoices | 2025-10-31T16:32:22.000Z |
| Charge with Pix through API | 2025-10-31T16:37:22.000Z |
| Idempotency key | 2025-10-31T16:36:37.000Z |
| Invoice status | 2025-10-31T16:42:55.000Z |
| Triggers | 2025-10-31T16:35:21.000Z |
| Invoice triggers | 2025-10-31T16:35:22.000Z |

## Material Retrieved

- `faturas`: create invoice, retrieve invoice, and external-ID search;
- `gatilhos`: supported events and trigger creation;
- the endpoint security schemes, request fields, response examples, and HTTP
  response declarations associated with those operations.

Repository research files contain curated facts and sanitized fixtures. Raw MCP
or Markdown pages are not committed because examples include realistic
personal-looking payer data, credentials-shaped examples, and large payloads.
They can be re-queried from the recorded official sources.
