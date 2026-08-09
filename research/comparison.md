# Provider Comparison

This matrix includes only provider-specific documented evidence. Absence of
evidence remains `Unknown`; it is not converted into an assumed common behavior.

| Dimension | Asaas | Iugu | Mercado Pago | PagBank | Pagar.me |
| --- | --- | --- | --- | --- | --- |
| Primary resource | `payment` | `invoice` | Unknown | Unknown | Unknown |
| Money representation | Required JSON number `value`; precision rules unknown | Required invoice items with integer `price_cents`; response totals in cents | Unknown | Unknown | Unknown |
| Currency | No create field found; implicit behavior unknown | Response example explicitly returns `BRL`; accepted currencies unknown | Unknown | Unknown | Unknown |
| Pix creation | `POST /v3/payments` with required customer, billing type, value, and due date | `POST /invoices` with required email, due date, and items; payer data documented as required for Pix | Unknown | Unknown | Unknown |
| Pix QR data | Separate `GET /v3/payments/{id}/pixQrCode` | Embedded `pix` object in invoice response | Unknown | Unknown | Unknown |
| Caller reference | Optional `externalReference` described as a free search field | `order_id` helps avoid duplicate payment; `external_reference` is searchable | Unknown | Unknown | Unknown |
| Request idempotency | No create key found in reviewed evidence | `Idempotency-Key` accepted for invoice creation; reuse returns HTTP 409; retention details unknown | Unknown | Unknown | Unknown |
| Lifecycle | Response status enum and separate webhook event flow documented; initial Pix status still unknown | Examples show invoice `pending`/`paid` and embedded Pix `qr_code_created`/`paid`; complete enum unknown | Unknown | Unknown | Unknown |
| Refunds | Unknown | Unknown | Unknown | Unknown | Unknown |
| Webhooks | JSON payment event POST; at-least-once delivery and stable duplicate event ID documented | Form-urlencoded trigger; invoice fields documented; duplicate/order/retry semantics unknown | Unknown | Unknown | Unknown |
| Card security boundary | Selected Pix request contains no cardholder data | Selected Pix invoice request contains no cardholder data | Unknown | Unknown | Unknown |

Detailed evidence and source links live in each provider directory. These rows
are comparison inputs, not discovered OPP invariants.
