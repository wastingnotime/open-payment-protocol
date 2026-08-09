# Provider Comparison

This matrix includes only provider-specific documented evidence. Absence of
evidence remains `Unknown`; it is not converted into an assumed common behavior.

| Dimension | Asaas | Iugu | Mercado Pago | PagBank | Pagar.me |
| --- | --- | --- | --- | --- | --- |
| Primary resource | `payment` | `invoice` | `order` -> payment transaction (Orders API); Payments API is legacy | Unknown | `order` -> `charge` -> Pix transaction |
| Money representation | Required JSON number `value`; precision rules unknown | Required invoice items with integer `price_cents`; response totals in cents | Decimal strings for order and transaction amounts | Unknown | Integer item/charge/transaction amounts; minor-unit guarantee not explicit in reviewed field description |
| Currency | No create field found; implicit behavior unknown | Response example explicitly returns `BRL`; accepted currencies unknown | Create has no currency field; response country is `BRA`; formal BRL guarantee unknown | Unknown | Response explicitly returns `BRL`; create request has no currency field |
| Pix creation | `POST /v3/payments` with required customer, billing type, value, and due date | `POST /invoices` with required email, due date, and items; payer requirements conflict across docs | `POST /v1/orders` with a Pix bank-transfer payment transaction | Unknown | `POST /orders` with items, customer/customer ID, and Pix payment entry |
| Pix QR data | Separate `GET /v3/payments/{id}/pixQrCode` | Embedded `pix` object in invoice response | Embedded `ticket_url`, `qr_code`, and `qr_code_base64` in payment method | Unknown | Embedded in charge `last_transaction` |
| Caller reference | Optional `externalReference` described as a free search field | `order_id` helps avoid duplicate payment; `external_reference` is searchable | Required order `external_reference`; separate transaction `reference_id` | Unknown | Optional merchant `code` at order, item, and customer scopes |
| Request idempotency | No create key found in reviewed evidence | `Idempotency-Key` accepted for invoice creation; reuse returns HTTP 409; retention details unknown | Required `X-Idempotency-Key`; reuse documented as HTTP 409; retention/replay details unknown | Unknown | No create guarantee found in reviewed index/pages |
| Lifecycle | Response status enum and separate webhook event flow documented; initial Pix status still unknown | Invoice status graph documented; embedded Pix graph incomplete | Separate order and payment status pairs; initial Pix is `action_required/waiting_transfer`; async create possible | Unknown | Separate order, charge, and Pix transaction states; deterministic test rules documented |
| Refunds | Unknown | Unknown | Total and per-transaction partial order refunds; Pix returns to payer account | Unknown | Unknown |
| Webhooks | JSON payment event POST; at-least-once delivery and stable duplicate event ID documented | Form-urlencoded trigger; invoice fields documented; duplicate/order/retry semantics unknown | Signed JSON order signal followed by GET; retry/order/duplicate semantics unknown | Unknown | POST webhook object tracks status, attempts, and response; exact retry/duplicate semantics unknown |
| Card security boundary | Selected Pix request contains no cardholder data | Selected Pix invoice request contains no cardholder data | Selected Pix request contains no cardholder data; shared order schema includes card-only fields | Unknown | Selected Pix request contains no cardholder data; create-order docs warn against open card data |

Detailed evidence and source links live in each provider directory. These rows
are comparison inputs, not discovered OPP invariants.
