# PagBank Webhook Research

## Delivery and Payload

An order may carry one `notification_urls` HTTPS endpoint. PagBank sends POST
notifications on transaction status changes. By default the payload matches the
synchronous API response; the documented paid-Pix payload is the full order,
including QR Code and a `PAID` Pix charge.

## Authenticity

The `x-authenticity-token` header is SHA-256 of the exact, unformatted bytes:

```text
{account-token}-{raw-request-payload}
```

Any whitespace change changes the digest. A mismatched event must be discarded.
This construction uses the API account token itself rather than a distinct
webhook secret, which is a provider-native security boundary.

## Unknown Delivery Semantics

Retry schedule, timeout, accepted acknowledgement codes, maximum attempts,
ordering, and duplicate-event identity are not established by the reviewed
pages.

[authenticity]: https://developer.pagbank.com.br/reference/confirmar-autenticidade-da-notificacao
[webhooks]: https://developer.pagbank.com.br/reference/webhooks
