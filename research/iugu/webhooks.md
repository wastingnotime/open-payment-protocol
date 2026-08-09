# Iugu Trigger Research

## Metadata

- Research date: 2026-08-09
- Sources: official Iugu MCP and Markdown documentation
- Evidence level: documented; not test-mode observed

## Native Concept and Transport

Iugu names webhook configuration a `web_hook` and calls it a `gatilho`
(trigger). `POST /web_hooks` requires `event` and `url`; optional
`authorization` configures a key for Basic Authentication.

Deliveries use `Content-Type: application/x-www-form-urlencoded`, not JSON.
The guide identifies outbound IP `98.82.243.132` for firewall allowlists. This
operational value is time-sensitive and must be rechecked before use.

## Invoice Events and Payload

Relevant events include `invoice.created`, `invoice.status_changed`,
`invoice.payment_failed`, `invoice.due`, `invoice.refund`,
`invoice.partially_refunded`, `invoice.refund_reverted`, and
`invoice.rejected`.

The invoice guide documents form fields for `invoice.created` and
`invoice.status_changed`, including invoice ID, account ID, native status,
source, order ID, external reference, payment method, paid time/value, and Pix
end-to-end ID where relevant. `invoice.status_changed` fires whenever an invoice
status changes.

## Unknown Delivery Semantics

The reviewed pages do not establish ordering, duplicate delivery, automatic
retry schedule, acknowledgement rules, timeout behavior, unique event/delivery
ID, or signatures. Optional Basic Authentication is not proof that no other
verification mechanism exists.

[create]: https://dev.iugu.com/reference/criar-gatilho
[guide]: https://dev.iugu.com/docs/gatilhos
[invoice-events]: https://dev.iugu.com/docs/gatilhos-fatura
