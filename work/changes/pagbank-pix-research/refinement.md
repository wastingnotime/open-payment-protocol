# PagBank Pix Research Refinement

## Outcome

Official Markdown evidence for PagBank Pix QR order creation and retrieval is
captured. The first simulation slice remains in evidence refinement.

## Model Pressure Observed

- A single-use QR Code belongs to the order before any charge exists.
- Successful payment causes a paid Pix charge to emerge later.
- Money is integer centavos and currency is currently BRL only.
- Idempotency promises same-response replay, unlike providers documenting 409
  on key reuse.
- Webhooks carry the full resource and authenticate with a hash involving the
  API token, not a separate webhook secret.
- Two official pages conflict on default QR expiration.

## Remaining Evidence

- sandbox-observed create, payment, expiration, and refund flows;
- exact create requirements and idempotency header contract;
- Pix-specific charge lifecycle and QR post-payment state;
- webhook delivery guarantees and error/retry fixtures.
