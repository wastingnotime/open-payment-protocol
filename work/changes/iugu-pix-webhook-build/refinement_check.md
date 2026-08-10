# Iugu Pix lifecycle and webhook refinement check

## Built

- `IUGU-PIX-014`: paid `invoice.status_changed` event with documented
  form-urlencoded fields.
- `IUGU-PIX-015`: canceled `invoice.status_changed` event without paid-only
  fields.
- `IUGU-PIX-016`: webhook trigger configuration with optional Basic
  Authentication represented as a capability boolean.

## Deliberately unknown

Delivery IDs, retries, acknowledgements, ordering, duplicates, timeout
behavior, signatures, and delivery outcomes remain unmodeled.
