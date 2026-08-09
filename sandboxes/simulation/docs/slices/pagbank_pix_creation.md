# PagBank Pix QR Order Creation and Retrieval

Status: creation and documented charge-emergence build complete.

The shared simulation preserves PagBank's order → single-use QR Code shape,
integer-cent amounts, QR image/base64 links, empty initial `charges`, amount
validation, and idempotency conflict. It does not normalize the order to the
Iugu invoice or Mercado Pago order/payment models.

Executable scenarios are `PB-PIX-001` through `PB-PIX-004` in
`simulators/pagbank/scenarios.md`.

Out of scope: expiration timing, refunds,
webhooks, and sandbox observation.
