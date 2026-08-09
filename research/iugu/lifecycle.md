# Iugu Invoice Lifecycle Research

## Metadata

- Research date: 2026-08-09
- Sources: official Iugu MCP and Markdown documentation
- Evidence level: documented; not test-mode observed

## Invoice Statuses

The official status reference documents:

```text
pending
paid
canceled
in_analysis
draft
partially_paid
refunded
expired
in_protest
chargeback
externally_paid
```

It documents these possible transitions:

```text
pending        -> paid | canceled | partially_paid | expired | in_analysis | externally_paid
paid           -> refunded | in_protest | chargeback
canceled       -> paid
partially_paid -> paid
expired        -> paid
in_analysis    -> canceled | paid
in_protest     -> paid | chargeback
```

`refunded` and `chargeback` have no next state in the documented table.

## Pix Status

Create/retrieve examples return invoice `pending` and embedded Pix
`qr_code_created`. A paid search example returns invoice and Pix `paid`,
`payment_method: "iugu_pix"`, and an end-to-end ID:

```text
invoice: pending -> paid
pix: qr_code_created -> paid
```

The embedded Pix status set remains incomplete. Invoice and Pix statuses must
stay distinct in the simulator.

## Events

`invoice.status_changed` is documented as firing whenever invoice status
changes. Other relevant events include `invoice.created`, `invoice.refund`,
`invoice.payment_failed`, `invoice.due`, `invoice.partially_refunded`,
`invoice.refund_reverted`, and `invoice.rejected`.

## Unknowns

- Complete embedded Pix status set and transitions.
- Operational finality despite documented recovery from `canceled` or `expired`
  to `paid`.
- Pix expiration timing and test-mode controls.
- Relationship between payment success and `invoice.released`, which the Pix
  guide recommends for notification when funds become available.

[events]: https://dev.iugu.com/docs/gatilhos-fatura
[pix]: https://dev.iugu.com/docs/realizar-cobran%C3%A7a-com-pix-por-api
[search]: https://dev.iugu.com/reference/buscar-fatura-por-ids-externos
[status]: https://dev.iugu.com/reference/status
