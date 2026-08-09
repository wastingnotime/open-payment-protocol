# Pagar.me Contract Research

## Research Metadata

- Provider: Pagar.me
- Research date: 2026-08-09
- Researcher: Codex, using official Markdown documentation
- Documentation index: `https://docs.pagar.me/llms.txt`
- API version: v5 / Core API references
- Evidence level: documentation only

## First-Slice Contract

| Dimension | Provider behavior | Evidence | Source |
| --- | --- | --- | --- |
| Primary resources | `POST /orders` creates an `order`; a payment entry produces a `charge`; its `last_transaction` holds the Pix transaction. The guide says a charge is the basis of a payment and is generated through orders or subscriptions. | Documented | [Create order][create], [charge guide][charge], [Pix reference][pix] |
| Customer | Either `customer_id` or an inline `customer` is required. For PSP clients, all customer fields, including address and phone, are required. | Documented | [Create order][create] |
| Money representation | Order items and charge/transaction amounts are JSON integers. Examples and simulator thresholds are consistent with centavos, but the reviewed create-order field description only says unit value greater than zero. | Documented / Inferred | [Create order][create], [Pix simulator][simulator] |
| Currency | Order and charge response examples explicitly return `BRL`; the create request has no currency field. Alternative currencies are not established. | Documented / Unknown | [Pix reference][pix] |
| Payment method | Request uses `payment_method: "pix"` and a `pix` object. Response examples vary between `"Pix"` and `"pix"`; casing stability is not established. | Documented / Unknown | [Pix reference][pix] |
| Creation | `POST /orders` requires `items` and `payments`. Pix requires `expires_in`, or `expires_at` when `expires_in` is omitted. | Documented | [Create order][create], [Pix reference][pix] |
| Retrieval | `GET /charges/{charge_id}` retrieves a native charge. The Pix creation response also returns order, charge, and transaction IDs. | Documented | [Get charge][retrieve], [Pix reference][pix] |
| Pix QR Code | `last_transaction` includes `qr_code`, `qr_code_url`, `expires_at`, additional information, and later the end-to-end ID and payer data. | Documented | [Pix reference][pix] |
| Caller references | Optional order `code` identifies the order in the merchant system, maximum 52 characters. Item and customer also have native `code` fields; their scopes must remain distinct. | Documented | [Create order][create] |
| Idempotency | No idempotency key or repeated-create guarantee was found in the reviewed `llms.txt` index or selected pages. | Unknown | [Documentation index][index] |
| Authentication | Secret and public keys exist separately for test and production. Secret key is required for server-side transactional operations. OpenAPI operations use HTTP Basic authentication. | Documented | [Access keys][auth], [Create order][create] |
| Environments | Test keys create no real receivables; production keys create real transactions. Both use the documented API surface. | Documented | [Access keys][auth] |
| Errors | Create order documents HTTP 400 with an empty object schema. Stable validation, authentication, not-found, and server-error envelopes remain unknown. | Documented / Unknown | [Create order][create] |
| Card boundary | Pagar.me explicitly warns not to send open card data in create order. The selected Pix request contains no PAN or CVV. | Documented | [Create order][create] |

## Minimal Candidate Pix Request

```json
{
  "code": "opp-documentation-fixture",
  "items": [
    {
      "amount": 1000,
      "description": "OPP documentation fixture",
      "quantity": 1,
      "code": "item-documentation-fixture"
    }
  ],
  "customer": {
    "name": "Documentation Fixture",
    "email": "payer@example.invalid"
  },
  "payments": [
    {
      "payment_method": "pix",
      "pix": {
        "expires_in": 3600
      }
    }
  ]
}
```

This conservative fixture is assembled from the documented schema. PSP-specific
customer requirements and test-account eligibility must be verified before a
live test.

## Open Questions

- Is every monetary `amount` guaranteed to use BRL minor units?
- What exact customer fields are required for Gateway versus PSP Pix requests?
- Is order `code` unique, searchable, or reusable?
- Is `payment_method` casing stable in current responses?
- Does Pagar.me support a create-order idempotency key outside the indexed docs?
- Should first-slice retrieval center the order or charge for each scenario?
- What exact response and certainty semantics apply to timeouts and 5xx errors?
- Which gateway/account configuration is required to enable Pix?

[auth]: https://docs.pagar.me/docs/chaves-de-acesso
[charge]: https://docs.pagar.me/docs/cobran%C3%A7a
[create]: https://docs.pagar.me/reference/criar-pedido-2
[index]: https://docs.pagar.me/llms.txt
[pix]: https://docs.pagar.me/reference/pix-2
[retrieve]: https://docs.pagar.me/reference/obter-cobran%C3%A7a
[simulator]: https://docs.pagar.me/docs/simulador-pix
