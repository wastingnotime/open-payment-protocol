# Mercado Pago Pix lifecycle and webhook refinement check

## Built

- `MP-PIX-011`: async processing order notification with JSON `order` topic,
  GET reconciliation, and HMAC signature verification.
- `MP-PIX-012`: mismatched signature explicitly discarded.

## Deliberately unknown

Timestamp tolerance, retries, acknowledgement codes, ordering, duplicate
identity, and delivery timing remain unmodeled.

Final validation for this increment: all provider reports remain deterministic,
the graph has no integrity errors, and the notification references the
authoritative async order ID rather than embedding a second order projection.
