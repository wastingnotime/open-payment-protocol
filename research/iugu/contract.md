# Iugu Contract Research

## Research Metadata

- Provider: Iugu
- Research date: 2026-08-09
- Researcher: Codex, using official Iugu MCP and Markdown documentation
- Documentation MCP: `https://dev.iugu.com/mcp`
- Documentation index: `https://dev.iugu.com/llms.txt`
- OpenAPI title: `faturas`
- API version: base URL `/v1`; documentation version not reported
- Evidence level: documentation only

## First-Slice Contract

| Dimension | Provider behavior | Evidence | Source |
| --- | --- | --- | --- |
| Primary resource | Native creation and retrieval resource is `invoice` (`fatura`). | Documented | [Create invoice][create], [retrieve invoice][retrieve] |
| Customer | OpenAPI marks `email` required and `customer_id` optional. The Pix guide says `email` is unnecessary with `customer_id`. OpenAPI prose says `payer` is required for Pix, while the guide's Pix request omits it. | Documented conflict | [Create invoice][create], [Pix guide][pix] |
| Money | Required `items` use integer `price_cents` in centavos, minimum 100. Responses expose integer cent totals and formatted display strings. | Documented | [Create invoice][create] |
| Currency | Response example returns `currency: "BRL"`; accepted alternatives are unknown. | Documented / Unknown | [Create invoice][create] |
| Payment method | Request `payable_with` is an array accepting `all`, `credit_card`, `bank_slip`, or `pix`; response examples serialize it as a string. | Documented | [Create invoice][create] |
| Prerequisite | Pix must be enabled with `PUT /v1/payments/pix`, `enable: true`; first activation creates an EVP key at the Central Bank. | Documented | [Enable methods][enable], [Pix guide][pix] |
| Creation | `POST /invoices` with `payable_with: ["pix"]`. OpenAPI requires `email`, `due_date`, and `items`; the guide documents the email/customer alternative and omits payer. | Documented conflict | [Create invoice][create], [Pix guide][pix] |
| Retrieval | `GET /invoices/{id}` retrieves one invoice by Iugu invoice ID. | Documented | [Retrieve invoice][retrieve] |
| Pix QR Code | Invoice response embeds `pix` with `qrcode`, `qrcode_text`, `status`, payer fields, end-to-end identifiers, and account-number last digits. | Documented | [Pix guide][pix] |
| Provider reference | Response `id` is the invoice ID; separate `secure_id` and hosted `secure_url` are returned. | Documented | [Create invoice][create] |
| Caller references | `order_id` helps prevent payment of the same invoice. `external_reference` is searchable and limited to 60 characters. `/resource_search` searches `external_id`, `order_id`, `end_to_end`, or `digitable_line`. | Documented | [Create invoice][create], [resource search][search] |
| Idempotency | Invoice creation accepts caller-generated `Idempotency-Key`. After one request is processed, reuse returns HTTP 409. Retention and payload-mismatch behavior are unknown. | Documented / Unknown | [Idempotency][idempotency] |
| Authentication | HTTP Basic Auth is recommended, Bearer Authentication is second, and request parameter `api_token` is third. MCP OpenAPI describes the query form. | Documented | [Authentication][auth] |
| Environment | OpenAPI server is `https://api.iugu.com/v1`; documentation distinguishes `test_mode` and `live_mode` but no separate Sandbox URL was found. | Documented / Unknown | [Create invoice][create] |
| Errors | General error reference documents HTTP 401 causes and create validation at 400 and 422. MCP examples remain empty objects, so serialization is incomplete. | Documented / Unknown | [Errors][errors] |
| Card boundary | Selected invoice/Pix request contains no PAN or CVV. Direct card charging is outside this slice. | Documented | [Create invoice][create] |

## Minimal Candidate Pix Request

```json
{
  "email": "payer@example.invalid",
  "due_date": "2099-12-31",
  "items": [
    {
      "description": "OPP documentation fixture",
      "quantity": 1,
      "price_cents": 1000
    }
  ],
  "payable_with": ["pix"],
  "payer": {
    "name": "Documentation Fixture",
    "email": "payer@example.invalid"
  }
}
```

This is not proof of a minimal valid request because official prose and OpenAPI
disagree about email/customer and Pix payer requirements.

## Open Questions

- Which payer fields are minimally required for Pix?
- Does `email` duplicate or differ from `payer.email`?
- Is request-array/response-string `payable_with` behavior stable?
- What uniqueness or conflict behavior does `order_id` enforce?
- How long is `Idempotency-Key` retained, and what happens if payload changes?
- What bodies accompany 401, 409, and all 422 responses?
- What rate-limit and server-failure semantics apply?
- How are test and live modes selected, and which behaviors differ?

[auth]: https://dev.iugu.com/reference/autentica%C3%A7%C3%A3o
[create]: https://dev.iugu.com/reference/criar-fatura
[enable]: https://dev.iugu.com/docs/habilitar-m%C3%A9todos-de-pagamento-via-api
[errors]: https://dev.iugu.com/reference/erros
[idempotency]: https://dev.iugu.com/docs/chave-de-idempot%C3%AAncia-1
[pix]: https://dev.iugu.com/docs/realizar-cobran%C3%A7a-com-pix-por-api
[retrieve]: https://dev.iugu.com/reference/buscar-fatura
[search]: https://dev.iugu.com/reference/buscar-fatura-por-ids-externos
