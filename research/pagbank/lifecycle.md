# PagBank Pix Lifecycle Research

## Resource Emergence

PagBank does not document an order-level status for the first Pix slice. At
creation, the order contains a QR Code and `charges: []`. After successful Pix
payment, the webhook example contains a newly created charge with:

```text
status: PAID
payment_method.type: PIX
payment_method.pix.end_to_end_id
payment_method.pix.holder
```

The general charge vocabulary is `AUTHORIZED`, `PAID`, `IN_ANALYSIS`,
`DECLINED`, `CANCELED`, and `WAITING`, but the reviewed docs do not establish
which states other than `PAID` apply to QR-created Pix charges.

## Expiration

The Pix guide documents a 24-hour default. The order-object reference instead
says 23:59 on the following day. No expiration status, event, or post-expiry
resource example was found.

## Unknowns

- Whether a charge exists before successful payment in any Pix scenario.
- Exact Pix charge transition graph.
- QR Code state after payment, expiration, or refund.
- Atomicity and timing between charge creation, order retrieval, and webhook.

[charge]: https://developer.pagbank.com.br/reference/objeto-charge
[order]: https://developer.pagbank.com.br/reference/objeto-order
[pix]: https://developer.pagbank.com.br/reference/criar-pedido-pedido-com-qr-code
[webhooks]: https://developer.pagbank.com.br/reference/webhooks
