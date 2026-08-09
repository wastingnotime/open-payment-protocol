# Iugu Pix Research Refinement

## Outcome

The OpenAPI-evidence portion of Iugu Pix invoice creation and retrieval is
captured. The first simulation slice remains in evidence refinement.

## Model Pressure Observed

- Iugu's native resource is an invoice, not an Asaas-style payment.
- Money is modeled through integer cent-valued invoice items rather than a
  required top-level decimal amount.
- The response explicitly returns `BRL` and embeds Pix QR data in the invoice.
- Invoice status and embedded Pix status are distinct.
- `order_id`, `external_reference`, and provider invoice ID have different
  documented purposes; none should be relabeled as idempotency.
- Iugu names webhook configuration a trigger and supports optional Basic
  Authentication material on that configuration.

## Remaining Iugu Evidence

- exact required payer fields for Pix;
- complete invoice/Pix lifecycle and error contracts;
- authentication guidance beyond the OpenAPI query-key scheme;
- test-mode behavior and sanitized observations;
- repetition, timeout, `order_id`, and external-reference semantics;
- trigger payload, ordering, duplicate, retry, and acknowledgement behavior.

These gaps prevent a claim that an Iugu simulator is already faithful, but the
documented differences are sufficient to refine the comparison model.
