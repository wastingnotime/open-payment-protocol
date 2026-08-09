# Provider-Native Pix Creation and Retrieval

Status: umbrella candidate; split into incremental provider-native builds.

## Selected Shape

- Implementation pack: WNT MRL Python event-sourced simulation.
- Runtime target: deterministic headless tests and WNT MRL Runtime observations.
- Architecture: one shared simulation environment with provider-native fakes
  behind explicit ports; no OPP model inside the fakes.

## Discovery Scope

Across Asaas, Iugu, Mercado Pago, PagBank, and Pagar.me, incrementally simulate
the smallest documented Pix creation path and retrieval by provider reference.
Preserve each provider's resource name, request/response shape, identifiers,
validation, initial status, and error shape. Iugu is selected as the first
increment in [`iugu_pix_creation.md`](iugu_pix_creation.md).

## Refinement Gate

The five-provider documentation baseline is complete. Each provider enters
build only when its own bounded increment has dated official-source evidence,
sanitized fixtures, explicit unknowns, a security assessment, and a refined
slice document. One provider's gap does not block faithful work on another.

## Use-Case Contract

Given a provider-specific valid create command, the corresponding fake accepts
or rejects it according to recorded evidence, persists its native event stream,
and exposes the native resource through its documented retrieval contract.
Repeating a command has only the behavior supported by that provider's evidence.

## Required Ports

- deterministic clock;
- deterministic provider identifier source;
- append-only event store;
- provider-native repository/query boundary;
- semantic observation sink.

## Initial Test and Scenario Plan

- valid create and retrieve for each evidenced provider;
- required-field and invalid-value rejection using native error shapes;
- unknown provider reference;
- deterministic replay with identical seed;
- explicit behavior for repeated create requests;
- invariant checks for evidence traceability, native-status visibility, and
  absence of sensitive cardholder data;
- runtime observations for intention, command, domain event, query, response,
  and invariant result.

## Done Criteria

- All behavior is evidence-linked and provider-native.
- Event history, projection state, observations, and invariant results are
  deterministic and inspectable.
- The runtime adapter exposes the shared scenario through `create_simulation()`.
- Tests demonstrate differences rather than normalizing them away.
- A refinement note updates the semantic hypothesis and candidate slice map.

## Out of Scope

Lifecycle completion, webhook delivery, refunds, cancellation, cards, a common
adapter, OPP schemas, conformance claims, live provider calls, and orchestration.
