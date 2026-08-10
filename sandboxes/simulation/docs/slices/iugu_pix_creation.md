# Iugu Pix Invoice Creation and Retrieval

Status: creation, documented lifecycle, caller-reference, and bounded webhook
event/configuration boundaries built;
refinement checks recorded in
`work/changes/iugu-pix-research/refinement.md`.

## Selected Shape

- Implementation pack: WNT MRL Python event-sourced simulation.
- Runtime targets: deterministic headless tests and WNT MRL Runtime observations.
- Architecture mode: one shared simulation environment with an Iugu-native fake
  behind explicit ports; no OPP domain model inside the fake.

## Discovery Scope

Reproduce Iugu's documented Pix invoice create, provider-ID retrieval,
documented invalid request, unknown retrieval, repeated idempotency key, and
external-ID lookup behaviors. Evidence comes from `research/iugu/` and its
linked official sources.

The conservative sanitized fixture is the valid baseline. Conflicting minimal
payer requirements are not resolved in code; combinations without evidence are
unsupported or explicitly unknown.

Executable scenarios are `IUGU-PIX-001` through `IUGU-PIX-013` in
`simulators/iugu/scenarios.md`.

## Native Use-Case Contract

Given an Iugu-specific create-invoice command, the simulator validates only
documented requirements, appends Iugu-native invoice events, projects the
invoice and embedded Pix response, and supports documented retrieval paths.
Repeated commands follow Iugu evidence rather than a generic idempotency model.

## Initial Native Vocabulary

- aggregate: Iugu invoice;
- provider identity: invoice `id`;
- caller identifiers: `order_id` and `external_reference`, kept distinct;
- money: integer cents in request items and native response totals;
- payment-method request: `payable_with` containing `pix`;
- output: invoice fields plus embedded `pix` object;
- status: exact Iugu invoice and Pix values from evidence, never normalized.

## Required Ports

- deterministic clock;
- deterministic Iugu identifier source;
- append-only event store;
- Iugu invoice repository and query boundary;
- idempotency record boundary;
- semantic observation sink.

## Scenario Plan

The executable scenario identifiers and acceptance expectations are defined in
`simulators/iugu/scenarios.md`: IUGU-PIX-001 through IUGU-PIX-010.

Runtime observations must cover actor intention, command, native event, query,
response, and invariant result. The runtime adapter will expose the shared
scenario from `src/app/simulation/mrl_runtime_scenario.py` when this slice first
becomes runnable.

## Done Criteria

- Seven selected scenarios have deterministic tests and a canonical JSON report.
- Native event history, invoice projection, observations, and invariants are inspectable.
- Each material branch is linked to documented or explicit unknown evidence.
- The common runtime adapter returns one repository Scenario and emits
  JSONL-compatible semantic observations.
- A lightweight refinement check records discrepancies and updates the slice map.
- No common OPP model, schema, or conformance claim is introduced.

## Out of Scope

Expiration, cancellation, webhook delivery,
refunds, cards, subscriptions, split, live Iugu calls, other providers, common
adapters, OPP schemas, and conformance behavior.
