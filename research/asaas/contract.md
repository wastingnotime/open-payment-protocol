# Asaas Contract Research

## Research Metadata

- Provider: Asaas
- Research date: 2026-08-09
- Researcher: Codex, using the official Asaas documentation MCP
- Documentation MCP: `https://docs.asaas.com/mcp`
- OpenAPI title: `Asaas`
- API version: v3 endpoints; documentation version not reported by MCP
- Evidence level: documentation only

## First-Slice Contract

| Dimension | Provider behavior | Evidence | Source |
| --- | --- | --- | --- |
| Primary resource | The endpoint creates an object whose native type is `payment` and whose identifier uses a `pay_...` example. Asaas documentation also states that credited amounts are treated as payments. | Documented | [Create payment][create], [payment events][events] |
| Customer | `customer` is required and is an Asaas customer identifier. The documented Pix example uses `cus_...`. | Documented | [Create payment][create], [Pix payment][pix] |
| Money representation | `value` is a required JSON number. Examples use decimal values such as `100.90` and `129.9`; minor-unit or rounding guarantees are not documented in the reviewed material. | Documented / Unknown | [Create payment][create], [Pix payment][pix] |
| Currency | The create-payment request schema reviewed through MCP has no currency field. Whether currency is implicitly BRL is not explicitly guaranteed by the reviewed pages. | Documented / Unknown | [Create payment][create] |
| Payment method | `billingType` is required and accepts `PIX` among its enum values. | Documented | [Create payment][create] |
| Creation | `POST /v3/payments` with JSON. For the documented Pix path the required fields are `customer`, `billingType`, `value`, and `dueDate`. | Documented | [Create payment][create], [Pix payment][pix] |
| Retrieval | `GET /v3/payments/{id}` retrieves one payment using its unique Asaas payment identifier. | Documented | [Retrieve payment][retrieve] |
| Pix QR Code | `GET /v3/payments/{id}/pixQrCode` returns `encodedImage`, `payload`, `expirationDate`, and description according to the schema. The dynamic QR Code is payable once. | Documented | [Pix payment][pix], [Pix QR Code][qr] |
| Provider reference | Response field `id` is the unique payment identifier in Asaas. | Documented | [Create payment][create] |
| External reference | Optional `externalReference` is described only as a “free search field.” No uniqueness, idempotency, or lookup guarantee was found in the reviewed evidence. | Documented / Unknown | [Create payment][create] |
| Authentication | API key in the `access_token` request header. `Content-Type: application/json` and `User-Agent` are documented for all calls; User-Agent is mandatory for new root accounts created from 2024-06-11. Sandbox and production keys differ. | Documented | [Authentication][auth] |
| Sandbox | Base URL is `https://api-sandbox.asaas.com/v3`; production is `https://api.asaas.com/v3`. Sandbox behavior has not been observed in this repository. | Documented | [Authentication][auth] |
| Error shape | JSON object containing an `errors` array of objects with `code` and `description`. | Documented | [HTTP responses][responses], [Create payment][create] |
| Card boundary | The selected Pix request has no PAN or CVV fields. Other Asaas card endpoints are outside this slice and have not been assessed. | Documented | [Create payment][create] |

## Minimal Documented Create Request

```json
{
  "customer": "cus_000005219613",
  "billingType": "PIX",
  "value": 100.90,
  "dueDate": "2023-07-21"
}
```

The example date is historical documentation data, not a currently valid test
input. See the sanitized fixture for a clearly non-live placeholder.

## Response Fields Relevant to the Slice

The create and retrieve operations use the documented payment response schema.
Fields relevant to the initial slice include `object`, `id`, `dateCreated`,
`customer`, `value`, `netValue`, `billingType`, `status`, `dueDate`,
`originalDueDate`, `invoiceUrl`, `invoiceNumber`, `externalReference`, and
`deleted`. Optional product-specific fields must remain tolerated rather than
assumed absent.

## Open Questions

- What precision, scale, and rounding rules apply to `value`?
- Is BRL implicit for every payment created through this endpoint?
- What exact initial status is returned for a newly created Pix payment in
  production and Sandbox?
- Can `externalReference` be queried, and does it have uniqueness guarantees?
- Does repeating the same create request create a second payment?
- What error is returned for an unknown payment ID by the retrieve endpoint?
- Which Pix-key prerequisites are enforced at creation versus QR retrieval?

[auth]: https://docs.asaas.com/docs/authentication-2
[create]: https://docs.asaas.com/reference/create-new-payment
[events]: https://docs.asaas.com/docs/payment-events
[pix]: https://docs.asaas.com/docs/payments-via-pix-or-dynamic-qr-code
[qr]: https://docs.asaas.com/docs/payments-via-pix-or-dynamic-qr-code
[responses]: https://docs.asaas.com/reference/http-response-codes
[retrieve]: https://docs.asaas.com/reference/retrieve-a-single-payment
