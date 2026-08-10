# PagBank Pix lifecycle and webhook refinement check

## Built

- `PB-PIX-011`: paid notification preserves the full order, emerging `PAID`
  charge, QR code, and raw-payload SHA-256 authenticity verification.
- `PB-PIX-012`: mismatched authenticity is explicitly discarded.
- `PB-PIX-013`: the single HTTPS notification URL remains visible on the
  native order projection.
- `PB-PIX-014`: multiple notification URLs are rejected.
- `PB-PIX-015`: non-HTTPS notification URLs are rejected.

The authenticity helper consumes exact raw bytes, and reports exclude the
account token used to compute the header.

## Deliberately unknown

Retry schedule, acknowledgement codes, maximum attempts, ordering, duplicate
identity, and timing between charge emergence and notification remain unknown.
