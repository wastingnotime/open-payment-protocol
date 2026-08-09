# Model Hypothesis

Status: extracted discovery hypothesis, not an OPP contract.

## Purpose and Boundary

The simulation exists to reveal the smallest useful provider-neutral payment
contract by reproducing provider-native behavior and observing the pressure on
thin adapters. It models neither payment orchestration nor production payment
processing.

The evidence sequence is fixed:

```text
provider contracts -> provider simulators -> provider adapters -> comparison
-> discovered invariants -> OPP Core
```

## Current Vocabulary

The following terms are candidate comparison vocabulary only:

- provider-native payment resource: whatever a provider actually calls and
  exposes (for example payment, charge, invoice, order, or transaction);
- caller reference: a caller-supplied correlation identifier where supported;
- provider reference: the provider-assigned resource identifier;
- provider-native status: the exact status exposed by the provider;
- lifecycle transition: an observed provider-native change over simulated time;
- provider event: a native webhook or notification delivery;
- capability: explicit evidence that an operation or behavior is supported.

`Payment`, normalized status, canonical error, and idempotency guarantee remain
unconfirmed OPP candidates. They must not be coded as protocol truth yet.

## Candidate Use Cases

1. Create one provider-native Pix-like payment resource.
2. Retrieve that resource by provider reference.
3. Advance it through one successful native transition.
4. Advance an alternative run through one failed or expired native transition.
5. Deliver the corresponding provider-native event, including deterministic
   duplicate or delayed delivery where evidence supports it.
6. Exercise a thin experimental adapter to compare semantic pressure.

## Candidate State and Events

Each provider fake may own a different aggregate and event vocabulary. The
shared simulation infrastructure may provide deterministic time, identifiers,
scheduling, event storage, and observations, but must not erase provider
differences.

Candidate semantic observations are actor intention, command, provider-native
domain event, external effect, actor reaction, and invariant result. These are
simulation evidence, not provider API fields.

## Invariants

- Every material simulated behavior cites documented, sandbox-observed, or
  explicitly inferred evidence.
- Unsupported behavior is explicit and is never silently emulated.
- Replaying a scenario with the same seed produces the same event history and
  observation log.
- Simulated lifecycle behavior uses controlled time and no wall-clock sleeps.
- No fixture, command, event, or observation contains secrets, customer data,
  raw PAN, CVV, or equivalent cardholder data.
- Provider-native identifiers, statuses, payloads, errors, and event behavior
  remain observable.
- Simulator success does not by itself establish an OPP invariant.

## Open Questions

- How should later adapter experiments relate invoice, payment, order, QR Code,
  charge, and transaction without erasing their boundaries?
- Is customer creation or association required for that path?
- What money representation and currency behavior does each provider expose?
- Which providers support native idempotency, caller references, or lookup by
  caller reference, and with what guarantees?
- Which transitions are synchronous, scheduled, or sandbox-only?
- What event authentication, delivery, duplication, and ordering behavior is
  documented for each provider?
- Which failures can be classified as definite versus unknown result?

## Candidate Slice Map

1. Iugu-native Pix invoice creation and retrieval, including evidenced
   repetition and reconciliation behavior (built; refinement-checked).
2. Incremental create/retrieve slices for Mercado Pago, PagBank, Pagar.me, and
   Asaas, ordered by evidence readiness and semantic pressure.
3. Successful provider-native lifecycle transition and event delivery, with
   Pagar.me as the leading deterministic candidate.
4. Failed or expired transition and error/result certainty.
5. Thin adapter comparison across all five providers.

The map is provisional and must be updated after every refinement check.
