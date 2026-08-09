# Mercado Pago Webhook Research

## Order Notifications

The recommended topic is `order`. Mercado Pago sends JSON with HTTPS POST when
orders are created or updated and transactions are processed. The compact body
contains `action`, `api_version`, application/event metadata, `type: "order"`,
and `data.id`; consumers retrieve the authoritative order with
`GET /v1/orders/{id}`.

## Authentication Boundary

Notifications include `x-signature` (`ts` and `v1`) and `x-request-id`.
Verification computes HMAC-SHA256 with the application's webhook secret over:

```text
id:[lowercase data.id];request-id:[x-request-id];ts:[ts];
```

Missing optional values are omitted. Implementations should compare the digest
exactly and establish a timestamp tolerance. The application secret is created
when Webhooks are configured and can be reset.

## Unknown Delivery Semantics

The reviewed page does not establish retry schedule, acknowledgement timeout,
accepted HTTP response codes, maximum attempts, event ordering, or duplicate
guarantees. `id` is present in the notification, but its stability across a
redelivery has not been established.

[notifications]: https://www.mercadopago.com.br/developers/en/docs/checkout-api-orders/notifications
