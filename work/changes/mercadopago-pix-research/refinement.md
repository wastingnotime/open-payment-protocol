# Mercado Pago Pix Research Refinement

## Outcome

The current Orders API documentation contract for Pix creation and order
retrieval is captured. The simulation slice remains in evidence refinement.

## Model Pressure Observed

- Recommended Orders API and legacy Payments API coexist and must not be merged.
- The native hierarchy is order -> payment transaction.
- Money is represented as decimal strings, unlike integer-cent providers.
- Order and payment each carry their own status pair.
- Asynchronous creation can temporarily omit transaction information.
- Idempotency is mandatory, but documented key reuse returns a conflict rather
  than an explicitly replayed original response.
- Webhook bodies are signals to retrieve the order, with HMAC authentication.

## Remaining Evidence

- sandbox-observed create, async, approval, expiration, and refund behavior;
- exact idempotency retention, scope, and timeout reconciliation;
- Pix-specific lifecycle graph and webhook delivery guarantees;
- error-envelope fixtures and rate-limit observations;
- compatibility differences from the legacy Payments API.
