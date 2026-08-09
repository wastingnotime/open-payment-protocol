# Iugu Trigger Research

## Metadata

- Research date: 2026-08-09
- Source interface: official Iugu developer MCP
- Evidence level: documented OpenAPI only; not test-mode observed

## Native Concept

Iugu names its webhook configuration resource a `web_hook` and describes
creation as creating a `gatilho` (trigger). `POST /web_hooks` requires:

- `event`: desired event name;
- `url`: receiving endpoint;
- optional `authorization`: a key used as Basic Authentication when validating
  received triggers.

The response includes `id`, `url`, `authorization`, `event`, and `active`.

## First-Slice Events

The supported-events endpoint documents these directly relevant names:

- `invoice.created`;
- `invoice.status_changed`;
- `invoice.payment_failed`;
- `invoice.due`;
- `invoice.refund`;
- `invoice.partially_refunded`;
- `invoice.refund_reverted`;
- `invoice.rejected`.

## Unknown Delivery Semantics

The MCP definitions reviewed here do not establish event payload shape,
delivery ordering, duplicate delivery, retry schedule, acknowledgement rules,
timeout behavior, event identifiers, timestamps, or signature mechanisms. The
optional Basic Authentication key is configuration evidence, not proof that no
other verification mechanism exists.

[create]: https://dev.iugu.com/reference/criar-gatilho
[events]: https://dev.iugu.com/mcp
