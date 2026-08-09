# Asaas Payment Webhook Research

## Metadata

- Research date: 2026-08-09
- Source interface: official Asaas documentation MCP
- Evidence level: documented; not Sandbox-observed

## Payload and Events

Asaas sends payment events with HTTP POST. The documented envelope includes
`id`, `event`, `dateCreated`, `account`, and a `payment` object containing the
complete payment information. Consumers must tolerate newly added attributes.

The first Pix slice is directly concerned with:

- `PAYMENT_CREATED`;
- `PAYMENT_RECEIVED`;
- `PAYMENT_OVERDUE`;
- `PAYMENT_REFUNDED`.

The complete documented payment-event list contains additional card, refund,
chargeback, dunning, view, split, deletion, and restoration events. The
simulator should add them only with corresponding slice scope and evidence.

Source: [payment events][events].

## Delivery Semantics

- Delivery is documented as at least once, so duplicate delivery is expected.
- A redelivered event retains the same unique event `id`.
- Asaas recommends acknowledging with HTTP 200 after durable persistence.
- The documentation says it does not guarantee that an event will be resent
  automatically, so persistence must precede acknowledgement.
- If sequence matters, Asaas advises processing in chronological/ascending
  order; this is not an ordering guarantee from the provider.

Source: [webhook idempotency][idempotency].

## Authentication and Retry Unknowns

Webhook authentication/signature behavior, retry schedule, delivery timeout,
and queue-pausing rules have not yet been captured. These are required before a
faithful webhook-delivery slice can be built.

[events]: https://docs.asaas.com/docs/payment-events
[idempotency]: https://docs.asaas.com/docs/how-to-implement-idempotence-in-webhooks
