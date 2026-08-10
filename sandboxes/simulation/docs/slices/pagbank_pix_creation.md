# PagBank Pix QR Order Creation and Retrieval

Status: creation, charge-emergence, notification authenticity, and bounded
notification configuration boundaries built;
refinement check recorded in
`work/changes/pagbank-pix-build/refinement_check.md`.

The shared simulation preserves PagBank's order → single-use QR Code shape,
integer-cent amounts, QR image/base64 links, empty initial `charges`, amount
validation, and idempotency conflict. It does not normalize the order to the
Iugu invoice or Mercado Pago order/payment models.

Executable scenarios are `PB-PIX-001` through `PB-PIX-015` in
`simulators/pagbank/scenarios.md`.

The lifecycle/event increment adds `PB-PIX-011` for a paid full-order
notification with raw-payload authenticity verification, `PB-PIX-012` for a
mismatched token that is discarded, and `PB-PIX-013` for preserving the single
HTTPS notification URL.

`PB-PIX-014` rejects multiple notification URLs and `PB-PIX-015` rejects a
non-HTTPS notification URL. These are configuration boundaries, not delivery
retry semantics.

Out of scope: expiration timing, refunds, retry schedule, acknowledgement
codes, duplicate identity, and sandbox observation.
