# Mercado Pago Contract Research

## Research Metadata

- Provider: Mercado Pago
- Research date: 2026-08-09
- Researcher: Codex, using official Markdown documentation and API references
- API family: Checkout Transparente via Orders API (`/v1/orders`)
- Evidence level: documentation only

## First-Slice Contract

| Dimension | Provider behavior | Evidence | Source |
| --- | --- | --- | --- |
| Primary resources | `POST /v1/orders` creates an order containing payment transactions. Each has a provider-generated order ID and payment-transaction ID. | Documented | [Pix guide][pix], [create order][create] |
| API choice | Orders API is the recommended Checkout Transparente integration. Payments API (`/v1/payments`) is explicitly classified as legacy. | Documented | [Documentation index][docs-index], [reference index][ref-index] |
| Customer | The Pix guide requires `payer.email`. Its frontend example also collects name and identification, but their server-side requirement for the shown request is not established. | Documented / Unknown | [Pix guide][pix] |
| Money representation | `total_amount`, transaction `amount`, and `paid_amount` are decimal strings such as `"50.00"`. Total must equal the sum of transaction amounts. | Documented | [create order][create] |
| Currency | The order response returns `country_code: "BRA"`, but the Pix create request has no currency field. A formal BRL-only guarantee is not established by the reviewed fields. | Documented / Unknown | [Pix guide][pix] |
| Creation | Pix uses `POST /v1/orders`, `type: "online"`, a payment method with `id: "pix"` and `type: "bank_transfer"`, and `processing_mode` `automatic` or `manual`. Manual orders require a later process-order call. | Documented | [Pix guide][pix] |
| Retrieval | `GET /v1/orders/{id}` returns current order and transaction information. It is also the documented reconciliation path for asynchronous creation or a missed notification. | Documented | [Pix guide][pix], [get order][get] |
| Pix QR data | The payment method response embeds `ticket_url`, copy-and-paste `qr_code`, and renderable `qr_code_base64`; `e2e_id` is also defined on retrieved transactions. | Documented | [Pix guide][pix], [get order][get] |
| Caller references | Pix requires order `external_reference`; API reference limits it to 150 letters, digits, hyphens, and underscores. A transaction has a separate `reference_id`. | Documented | [Pix guide][pix], [create order][create] |
| Idempotency | `X-Idempotency-Key` is required, 1–150 characters, and intended to ensure one-time processing. Reusing a key is documented as HTTP 409 `idempotency_key_already_used`; retention and replay-response behavior are unknown. | Documented / Unknown | [Pix guide][pix], [create order][create] |
| Authentication | Server calls use a private Access Token as `Authorization: Bearer <ACCESS_TOKEN>`. Test and production tokens are distinct. | Documented | [AI resources][ai], [Pix guide][pix] |
| Async behavior | Creation can be asynchronous, leaving an order in `processing` without transaction information until a later webhook or GET. | Documented | [Pix guide][pix], [get order][get] |
| Rate limiting | Order creation can return HTTP 429; the client must wait for the `Retry-After` duration before retrying. | Documented | [Pix guide][pix] |
| Refunds | Orders API supports total and per-transaction partial refunds. Pix funds return to the payer account; refund window is documented as 180 days after approval and sufficient balance is required. | Documented | [refunds][refunds] |
| Card boundary | The selected Pix request contains no PAN or CVV. Card-specific fields exist in the shared order schema and must not enter OPP Core. | Documented | [create order][create] |

## Minimal Candidate Pix Request

The HTTP request must additionally carry an Access Token and a unique
`X-Idempotency-Key`.

```json
{
  "type": "online",
  "total_amount": "50.00",
  "external_reference": "opp_documentation_fixture",
  "processing_mode": "automatic",
  "transactions": {
    "payments": [
      {
        "amount": "50.00",
        "payment_method": {
          "id": "pix",
          "type": "bank_transfer"
        },
        "expiration_time": "PT1H"
      }
    ]
  },
  "payer": {
    "email": "payer@example.invalid"
  }
}
```

## Open Questions

- Is BRL the guaranteed currency for every order using Pix in Brazil?
- Is `external_reference` unique, searchable, or reusable?
- Does a repeated identical request with the same idempotency key always return
  409, or can any successful replay return the original result?
- What retention period and scope apply to idempotency keys?
- Which exact fields are absent during asynchronous order creation?
- What are the complete Pix-specific order and payment transition graphs?
- What delivery retry, duplicate, and ordering guarantees apply to order
  notifications?
- Which Orders API behavior differs from the legacy Payments API beyond resource
  shape?

[ai]: https://www.mercadopago.com.br/developers/en/docs/ai-resources.md
[create]: https://www.mercadopago.com.br/developers/en/reference/online-payments/checkout-api/create-order/post
[docs-index]: https://www.mercadopago.com.br/developers/en/docs/llms.txt
[get]: https://www.mercadopago.com.br/developers/en/reference/online-payments/checkout-api/get-order/get
[pix]: https://www.mercadopago.com.br/developers/en/docs/checkout-api-orders/payment-integration/pix
[ref-index]: https://www.mercadopago.com.br/developers/en/reference/llms.txt
[refunds]: https://www.mercadopago.com.br/developers/en/docs/checkout-api-orders/refunds-cancellations
