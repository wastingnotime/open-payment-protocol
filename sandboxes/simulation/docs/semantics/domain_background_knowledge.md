# Domain Background Knowledge

Status: broad context for expectation-gap detection, not protocol authority.

## Domain Frame

OPP seeks a narrow, language-neutral contract between payment-consuming
applications and provider implementations. Applications or deployment
configuration choose the provider. Routing, balancing, fallback, fee
optimization, accounting, settlement, fraud, credential storage, and merchant
business rules are outside the model.

Provider APIs may center different resources and split operations differently.
Equal field names do not imply equal semantics, and different names do not rule
out a shared invariant. Research therefore records each provider independently
before comparison.

## Evidence Classes

- `Documented`: stated by a current official provider source.
- `Sandbox-observed`: observed in a sanitized provider test environment.
- `Inferred`: reasoned from evidence but not guaranteed by the provider.
- `Unknown`: not established by available evidence.

Simulator behavior must retain its evidence class and source. A simulator is a
contract-discovery tool, not independent proof that the interpretation is
correct.

## Important Semantic Pressure

- Resource identity: payment, charge, invoice, order, and transaction may have
  materially different boundaries.
- Result certainty: transport failure can leave creation outcome unknown.
- Idempotency: keys, external references, uniqueness, replay, and lookup can be
  separate provider capabilities.
- Lifecycle: similar labels may have different transition and finality rules.
- Events: payload completeness, authentication, ordering, retries, delay, and
  duplicate delivery vary.
- Capabilities: cancellation, refund, partial refund, installments, split, and
  hosted flows must remain explicit.
- Regional mechanisms: Pix and boleto may require profiles or extensions rather
  than lossy generic names.
- Security: OPP Core must not require raw PAN, CVV, or equivalent cardholder
  data; safer provider tokenization and hosted mechanisms are preferred.

## Evaluation Lens

Expectation-gap detection should ask whether the coherent model preserves
provider reality, exposes unsupported behavior, distinguishes definite from
unknown outcomes, remains deterministic, and supports a genuinely small shared
contract without becoming either an API union or a useless intersection.
