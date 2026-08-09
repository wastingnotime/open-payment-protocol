# Pagar.me Pix Research Refinement

## Outcome

The official Markdown evidence for Pagar.me Pix order creation and charge
retrieval is captured. The first simulation slice remains in evidence
refinement.

## Model Pressure Observed

- Pagar.me exposes an order -> charge -> transaction hierarchy, unlike the
  single Asaas payment or Iugu invoice with embedded Pix state.
- Merchant codes exist at several scopes and must not be conflated.
- Documentation response examples vary between `Pix` and `pix` casing.
- Order, charge, and Pix transaction statuses are independently observable.
- Test keys offer deterministic amount-based Pix success/failure behavior that
  can support the first simulator scenario after the contract is refined.
- Webhook delivery itself has native state, attempt count, and response evidence.

## Remaining Pagar.me Evidence

- test-observed request validation and order/charge/transaction transitions;
- exact monetary unit guarantee and Gateway versus PSP customer requirements;
- idempotency or caller-code uniqueness semantics;
- stable error envelope and unknown-result reconciliation;
- webhook authentication, retry schedule, acknowledgement, ordering, and
  duplicate behavior.

These gaps prevent a claim that a Pagar.me simulator is already faithful.
