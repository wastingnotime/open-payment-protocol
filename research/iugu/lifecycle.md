# Iugu Invoice Lifecycle Research

## Metadata

- Research date: 2026-08-09
- Source interface: official Iugu developer MCP
- Evidence level: documented examples only; not test-mode observed

## Observed Vocabulary

The create and retrieve endpoint examples return invoice `status: "pending"`
and embedded Pix `status: "qr_code_created"`. The external-ID search example
shows a paid Pix invoice with invoice `status: "paid"`, embedded Pix
`status: "paid"`, `payment_method: "iugu_pix"`, and populated
`end_to_end_id`.

These examples support candidate observations, not a complete status enum or
transition graph:

```text
invoice: pending -> paid
pix: qr_code_created -> paid
```

The invoice and embedded Pix statuses must remain distinct in the simulator.

## Supported Event Names

The trigger endpoint lists `invoice.created`, `invoice.status_changed`,
`invoice.refund`, `invoice.payment_failed`, `invoice.due`,
`invoice.partially_refunded`, `invoice.refund_reverted`, and
`invoice.rejected`, among other invoice events. Event names do not establish
their payloads, ordering, or exact relationship to status values.

## Unknowns

- Complete invoice and Pix status sets.
- Final versus intermediate statuses.
- Expiration and overdue behavior for Pix invoices.
- Exact transition timing and test-mode controls.
- Whether `invoice.status_changed` is emitted for every native transition.

[create]: https://dev.iugu.com/reference/criar-fatura
[events]: https://dev.iugu.com/mcp
[search]: https://dev.iugu.com/reference/buscar-fatura-por-ids-externos
