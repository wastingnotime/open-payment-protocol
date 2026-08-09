# Pagar.me Webhook Research

## Metadata

- Research date: 2026-08-09
- Source: official Pagar.me Markdown documentation
- Evidence level: documented; not test-observed

## Delivery and Object

Pagar.me sends HTTP POST notifications to configured URLs when selected events
occur. The documented webhook object includes:

- `id` in `hook_...` format;
- target `url` and `event`;
- delivery `status`: `pending`, `sent`, or `failed`;
- `attempts`, `last_attempt`, `response_status`, and `response_raw`;
- `account` and event `data`.

The guide says retry count can be configured when receipt fails. Failed
webhooks can be queried and manually resent. Exact retry timing,
acknowledgement codes, ordering, and duplicate semantics are not documented in
the reviewed pages.

## First-Slice Events

- `order.created`, `order.paid`, `order.payment_failed`, `order.canceled`;
- `charge.created`, `charge.updated`, `charge.pending`, `charge.processing`,
  `charge.paid`, `charge.payment_failed`, `charge.refunded`;
- `charge.underpaid`, `charge.overpaid`, and `charge.partial_canceled` expose
  additional native outcomes.

The event list documents event names and meanings but not the precise `data`
payload schema for each event.

## Operational Notes

Only standard port 80 for HTTP and 443 for HTTPS are documented for webhook
targets. Authentication or signature verification was not established by the
reviewed pages.

[events]: https://docs.pagar.me/reference/eventos-de-webhook-1
[guide]: https://docs.pagar.me/docs/webhooks
[overview]: https://docs.pagar.me/reference/vis%C3%A3o-geral-sobre-webhooks
