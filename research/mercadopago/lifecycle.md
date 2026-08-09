# Mercado Pago Pix Lifecycle Research

## Documented States

The order and its payment transaction each expose `status` and
`status_detail`; they must remain distinct in the simulator.

The Pix creation guide documents the initial pair:

```text
action_required / waiting_transfer
```

The general Orders API vocabulary includes order statuses `created`,
`processed`, `failed`, `action_required`, `refunded`, `canceled`, and
`expired`. Creation may instead initially return `processing` with incomplete
information because processing is asynchronous. The test guide says its
predefined Pix request begins `action_required` and later becomes approved,
but does not state the exact final Orders API status pair in prose.

## Expiration and Cancellation

- Default Pix expiry is 24 hours.
- `expiration_time` accepts an ISO 8601 duration from 30 minutes through 30 days.
- An `action_required` Pix payment may be canceled.
- If still unpaid 30 days after its due date, Mercado Pago considers it expired
  and changes it to `canceled` or `expired`; manual cancellation is then unavailable.

## Unknowns

- Complete Pix-specific transition graph at both resource levels.
- Whether order and transaction state changes are atomic.
- Exact status after the documented test's automatic approval.
- Timing, ordering, and duplication between GET-visible and webhook-visible state.

[get]: https://www.mercadopago.com.br/developers/en/reference/online-payments/checkout-api/get-order/get
[pix]: https://www.mercadopago.com.br/developers/en/docs/checkout-api-orders/payment-integration/pix
[test]: https://www.mercadopago.com.br/developers/en/docs/checkout-api-orders/integration-test/pix
