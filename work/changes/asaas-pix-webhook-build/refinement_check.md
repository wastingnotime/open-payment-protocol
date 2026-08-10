# Asaas Pix lifecycle and webhook refinement check

## Built

- `AS-PIX-009`: `PAYMENT_RECEIVED` envelope with persist-before-ack guidance.
- `AS-PIX-010`: at-least-once redelivery with stable event ID.
- `AS-PIX-011`: `PAYMENT_OVERDUE` event sequence without response-status
  normalization.

## Deliberately unknown

Response-status transitions, retry schedule, acknowledgement codes, ordering,
authentication, and queue behavior remain unmodeled.
