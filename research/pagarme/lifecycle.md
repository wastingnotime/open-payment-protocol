# Pagar.me Pix Lifecycle Research

## Metadata

- Research date: 2026-08-09
- Source: official Pagar.me Markdown documentation
- Evidence level: documented; not test-observed

## Separate Native Lifecycles

The first Pix path exposes at least three status-bearing resources:

- order, with examples `pending` and `paid`;
- charge, with Pix examples `pending` and `paid` plus a broader charge status
  vocabulary;
- Pix transaction in `last_transaction`.

Pix transaction statuses are explicitly documented as:

```text
waiting_payment
paid
pending_refund
refunded
with_error
failed
```

The general charge guide documents:

```text
authorized_pending_capture
not_authorized
captured
partial_capture
waiting_capture
refunded
voided
partial_refunded
partial_void
error_on_voiding
error_on_refunding
waiting_cancellation
with_error
failed
chargedback
```

The general list appears broader than Pix and does not include the Pix response
example's `pending`/`paid` values. It must not be treated as a complete Pix
charge transition graph without test evidence.

## Test Simulator Behavior

With transactional test keys, the official Pix simulator documents:

```text
amount <= BRL 500.00: created pending -> automatically paid seconds later
amount >  BRL 500.00: created failed
```

The simulator cannot currently be combined with split. These are documented
test-environment rules, not production guarantees.

## Webhook Signals

Relevant events include `order.created`, `order.paid`,
`order.payment_failed`, `order.canceled`, `charge.created`, `charge.pending`,
`charge.processing`, `charge.paid`, `charge.payment_failed`, and
`charge.refunded`.

## Unknowns

- Exact order and Pix-charge transition graphs in production.
- Expiration event/status behavior for an unpaid Pix QR Code.
- Timing and ordering between order, charge, transaction, and webhook updates.
- Whether a failed transaction leaves the order and charge in matching states.

[charge]: https://docs.pagar.me/docs/cobran%C3%A7a
[events]: https://docs.pagar.me/reference/eventos-de-webhook-1
[pix]: https://docs.pagar.me/reference/pix-2
[simulator]: https://docs.pagar.me/docs/simulador-pix
