# Iugu Contract Research

## Research Metadata

- Provider: Iugu
- Research date: 2026-08-09
- Researcher: Codex, using the official Iugu developer MCP
- Documentation MCP: `https://dev.iugu.com/mcp`
- OpenAPI title: `faturas`
- API version: base URL `/v1`; documentation version not reported by MCP
- Evidence level: documentation only

## First-Slice Contract

| Dimension | Provider behavior | Evidence | Source |
| --- | --- | --- | --- |
| Primary resource | The native creation and retrieval resource is `invoice` (`fatura`). | Documented | [Create invoice][create], [retrieve invoice][retrieve] |
| Customer | `email` is required. `customer_id` is optional in the request schema. A separate `payer` object is documented as required for Pix and boleto issuance, though its individual required fields are not identified by the schema. | Documented / Unknown | [Create invoice][create] |
| Money representation | An invoice contains required `items`; each item uses integer `price_cents` in centavos and has a documented minimum of 100. Responses expose integer `items_total_cents`, `total_cents`, and related cent fields, plus formatted display strings. | Documented | [Create invoice][create] |
| Currency | The response example explicitly returns `currency: "BRL"`. Whether other currencies are accepted is not documented by the reviewed endpoint. | Documented / Unknown | [Create invoice][create] |
| Payment method | Optional `payable_with` is an array accepting `all`, `credit_card`, `bank_slip`, or `pix`. The response example serializes it as a string. | Documented | [Create invoice][create] |
| Creation | `POST /invoices`. Required top-level fields are `email`, `due_date`, and `items`. A Pix-only request also needs the documented payer information and `payable_with: ["pix"]`. | Documented / Inferred | [Create invoice][create] |
| Retrieval | `GET /invoices/{id}` retrieves one invoice by its Iugu invoice ID. | Documented | [Retrieve invoice][retrieve] |
| Pix QR Code | The invoice response contains a `pix` object with `qrcode`, `qrcode_text`, `status`, payer fields, end-to-end identifiers, and account-number last digits. | Documented | [Create invoice][create] |
| Provider reference | Response field `id` is the invoice ID. A separate `secure_id` and hosted `secure_url` are also returned. | Documented | [Create invoice][create] |
| Caller references | `order_id` is described as a unique purchase-order number that helps avoid payment of the same invoice. `external_reference` is searchable and limited to 60 characters. `/resource_search` can search by `external_id`, `order_id`, `end_to_end`, or `digitable_line`. Creation idempotency is not documented. | Documented / Unknown | [Create invoice][create], [resource search][search] |
| Authentication | The MCP OpenAPI security scheme specifies an API key named `api_token` in the query string. Other supported authentication forms and secret-handling guidance were not exposed by the reviewed MCP tools. | Documented / Unknown | [Create invoice][create] |
| Environment | The OpenAPI server is `https://api.iugu.com/v1`. The reviewed MCP output does not identify a separate Sandbox URL; examples refer to `test_mode` and `live_mode`. | Documented / Unknown | [Create invoice][create] |
| Error shape | Create and retrieve document HTTP 400 but expose an empty object example and no useful error schema. | Documented / Unknown | [Create invoice][create], [retrieve invoice][retrieve] |
| Card boundary | The selected invoice/Pix request contains no PAN or CVV. Direct card-charge surfaces are outside this slice. | Documented | [Create invoice][create] |

## Minimal Candidate Pix Request

This request is assembled from the endpoint schema rather than copied from a
complete provider example:

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

Because the schema says payer data is required for Pix without marking specific
payer fields required, this candidate is not yet proof of a valid request.

## Open Questions

- Which `payer` fields are minimally required for Pix creation?
- Does `email` duplicate or differ semantically from `payer.email`?
- Does `payable_with` consistently use an array in requests and a string in
  responses?
- Which invoice status values and transitions apply to Pix?
- What uniqueness or conflict behavior does `order_id` enforce?
- Does request repetition create multiple invoices?
- What errors and HTTP codes are returned for validation, authentication,
  missing invoices, conflicts, rate limiting, and server failures?
- How are test mode and live mode selected, and which behaviors differ?

[create]: https://dev.iugu.com/reference/criar-fatura
[retrieve]: https://dev.iugu.com/mcp
[search]: https://dev.iugu.com/reference/buscar-fatura-por-ids-externos
