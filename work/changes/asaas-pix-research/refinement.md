# Asaas Pix Research Refinement

## Outcome

The documentation-evidence portion of Asaas Pix creation and retrieval is
captured. The first simulation slice remains blocked from build until equivalent
evidence exists for Iugu, Mercado Pago, PagBank, and Pagar.me.

## Model Pressure Observed

- Asaas natively calls the collection resource `payment`.
- A separate Asaas page uses payment terminology for a bill-payment execution
  lifecycle with incompatible statuses. Resource context must accompany native
  status names.
- `externalReference` is a free search field in the reviewed schema, not
  documented proof of idempotency.
- Response statuses and webhook event types are separate observable concepts.
- At-least-once webhook delivery requires deterministic duplicate-event behavior
  in a later event slice.

## Remaining Asaas Evidence

- Sandbox-observed create, retrieve, QR retrieval, and invalid-request examples;
- exact initial Pix payment status;
- create-request repetition and timeout behavior;
- external-reference lookup and uniqueness semantics;
- webhook authentication, retries, timeouts, and queue behavior.

These gaps do not prevent researching the other providers. They do prevent a
claim that the Asaas simulator is already faithful.
