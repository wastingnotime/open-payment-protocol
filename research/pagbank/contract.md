# PagBank Contract Research

## Research Metadata

- Provider: PagBank
- Research date: 2026-08-09
- Researcher: Codex, using official Markdown documentation
- API family: Orders API
- Evidence level: documentation only

## First-Slice Contract

| Dimension | Provider behavior | Evidence | Source |
| --- | --- | --- | --- |
| Primary resources | `POST /orders` creates an `order` with one single-use Pix `qr_code`. The create response has an empty `charges` array; after payment, the order webhook contains a new paid `charge`. | Documented | [Pix guide][pix], [webhooks][webhooks] |
| Account prerequisite | The seller must have at least one active Pix addressing key. If several exist, PagBank prioritizes a random key. | Documented | [Pix guide][pix] |
| Customer | The order object marks `customer.tax_id` required. The Pix guide example also sends name, email, and phone, but their Pix-specific requirement is not established. | Documented / Unknown | [order object][order], [Pix guide][pix] |
| Money representation | Item `unit_amount`, QR `amount.value`, and charge amounts are positive JSON integers in centavos. | Documented | [order object][order], [charge object][charge] |
| Currency | Charge currency is uppercase ISO 4217 and currently only `BRL` is supported. The QR create amount has no currency field. | Documented | [charge object][charge], [Pix guide][pix] |
| Creation | A Pix order includes `qr_codes` rather than `charges`. PagBank currently supports one QR Code per order and each QR Code accepts one successful payment. | Documented | [Pix guide][pix] |
| Retrieval | `GET /orders/{order_id}` retrieves the order. Responses provide HATEOAS-style `SELF`, QR image/base64, and payment links. | Documented | [get order][get], [Pix guide][pix] |
| QR data | `qr_codes[].text` is the copy-and-paste value; links with `QRCODE.PNG` and `QRCODE.BASE64` retrieve image and base64 forms. | Documented | [Pix guide][pix] |
| Caller references | Order `reference_id` is described as a unique caller-assigned identifier, 1–64 characters. Items and later charges have separate `reference_id` fields. | Documented | [order object][order], [charge object][charge] |
| Idempotency | Repeated requests with the same idempotency key are documented to always return the same response. The key is sent as a request header. Header name, retention, scope, and required endpoints are not established by the selected guide. | Documented / Unknown | [idempotency][idempotency] |
| Authentication | API requests use an authentication token as `Authorization: Bearer <token>`. Sandbox and production tokens are obtained separately. | Documented | [auth][auth], [get order][get] |
| Environments | Sandbox base URL is `https://sandbox.api.pagseguro.com`; production is `https://api.pagseguro.com`. | Documented | [environments][environments] |
| Expiration | The Pix guide says default validity is 24 hours, while the order object says until 23:59 the following day. This conflict must remain explicit until observed. | Documented conflict | [Pix guide][pix], [order object][order] |
| Refunds | `POST /charges/{charge_id}/cancel` can return partial refund totals while status remains `PAID`, or a fully refunded `CANCELED` charge. Pix applicability and limits require observation. | Documented / Unknown | [cancel][cancel] |
| Errors | Errors use `error_messages[]` with `code`, `description`, `parameter_name`, and `error`. Documented statuses include 400, 401, 403, 404, 409, and 500. | Documented | [errors][errors] |
| Card boundary | The selected Pix request contains no cardholder data. Raw card fields exist in the shared order/charge schema and must not enter OPP Core. | Documented | [order object][order] |

## Minimal Candidate Pix Request

```json
{
  "reference_id": "opp-documentation-fixture",
  "customer": {
    "name": "Documentation Fixture",
    "email": "payer@example.invalid",
    "tax_id": "00000000000"
  },
  "items": [
    {
      "name": "OPP documentation fixture",
      "quantity": 1,
      "unit_amount": 1000
    }
  ],
  "qr_codes": [
    {
      "amount": {
        "value": 1000
      },
      "expiration_date": "2030-01-01T12:00:00-03:00"
    }
  ],
  "notification_urls": [
    "https://example.invalid/webhooks/pagbank"
  ]
}
```

The tax ID is an intentionally invalid documentation placeholder and must be
replaced only with approved sandbox test data before observation.

## Open Questions

- What is the exact idempotency header name, key length, scope, and retention?
- Which customer fields are truly required for a Pix-only order?
- Is `reference_id` enforced as unique, and can it be used for reconciliation?
- Which documented default-expiration statement is authoritative?
- Does an unpaid QR Code expose status anywhere before a charge exists?
- What happens to the order and QR Code after expiration?
- What are the retry, acknowledgement, ordering, and duplicate webhook rules?
- Which partial/full cancellation rules and time windows apply to Pix charges?

[auth]: https://developer.pagbank.com.br/docs/token-de-autenticacao
[cancel]: https://developer.pagbank.com.br/reference/cancelar-pagamento
[charge]: https://developer.pagbank.com.br/reference/objeto-charge
[environments]: https://developer.pagbank.com.br/docs/ambientes-disponiveis
[errors]: https://developer.pagbank.com.br/reference/codigos-de-erro-order
[get]: https://developer.pagbank.com.br/reference/consultar-pedido
[idempotency]: https://developer.pagbank.com.br/docs/chaves-publicas-e-de-idempotencia
[order]: https://developer.pagbank.com.br/reference/objeto-order
[pix]: https://developer.pagbank.com.br/reference/criar-pedido-pedido-com-qr-code
[webhooks]: https://developer.pagbank.com.br/reference/webhooks
