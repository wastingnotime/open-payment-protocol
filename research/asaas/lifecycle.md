# Asaas Payment Lifecycle Research

## Metadata

- Research date: 2026-08-09
- Source interface: official Asaas documentation MCP
- Evidence level: documented; not Sandbox-observed

## Collection Payment Statuses

The response schema for `POST /v3/payments` and `GET /v3/payments/{id}`
documents these native statuses:

```text
PENDING
RECEIVED
CONFIRMED
OVERDUE
REFUNDED
RECEIVED_IN_CASH
REFUND_REQUESTED
REFUND_IN_PROGRESS
CHARGEBACK_REQUESTED
CHARGEBACK_DISPUTE
AWAITING_CHARGEBACK_REVERSAL
DUNNING_REQUESTED
DUNNING_RECEIVED
AWAITING_RISK_ANALYSIS
```

Source: [create payment reference][create].

The payment-events guide documents the Pix collection flows as:

```text
on time:  PAYMENT_CREATED -> PAYMENT_RECEIVED
overdue:  PAYMENT_CREATED -> PAYMENT_OVERDUE -> PAYMENT_RECEIVED
refund:   PAYMENT_CREATED -> PAYMENT_RECEIVED -> PAYMENT_REFUNDED
```

These are webhook event sequences, not proof that response `status` values and
event names are interchangeable. The simulator must represent both native
fields explicitly.

## Unresolved Documentation Conflict

The MCP result titled “Possible Statuses” describes `PENDING`,
`BANK_PROCESSING`, `PAID`, `FAILED`, `CANCELLED`, and `REFUNDED`, and says all
Sandbox payments fail after creation. Its related links and wording concern bill
payment execution rather than payment collection. Those statuses conflict with
the collection endpoint schema above.

Until Asaas documentation or Sandbox evidence establishes applicability, this
page must not define the collection-payment simulator lifecycle. This is an
explicit unknown, not a normalization opportunity.

## First-Slice Unknowns

- Exact initial response status after Pix payment creation.
- Relationship and timing between `CONFIRMED` and `RECEIVED` for Pix beyond the
  documented event examples.
- Whether an overdue Pix payment remains payable and under what constraints.
- Sandbox transition controls and timing.

[create]: https://docs.asaas.com/reference/create-new-payment
[events]: https://docs.asaas.com/docs/payment-events
[statuses]: https://docs.asaas.com/docs/possible-statuses
