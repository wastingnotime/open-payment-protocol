# Provider-Native Scenario Graph

Status: internal discovery graph; not OPP protocol authority.

The graph expands the simulation beyond create/retrieve nodes while preserving
provider-native lifecycle and resource boundaries.

```mermaid
flowchart LR
  AC[Simulation coordinator] --> AA[Asaas actor] --> AUC[Asaas use case] --> AR[Asaas payment]
  AC --> AI[Iugu actor] --> IUC[Iugu use case] --> IR[Iugu invoice]
  AC --> AM[Mercado Pago actor] --> MUC[Create/reconcile use case] --> MR[Order + payment]
  AC --> AB[PagBank actor] --> BUC[Create/charge use case] --> BR[Order + QR + charge]
  AC --> AP[Pagar.me actor] --> PUC[Create/outcome use case] --> PR[Order + charge + transaction]
  I1[Iugu create/retrieve] --> I7[paid]
  I1 --> I8[canceled] --> I10[recovered paid]
  I1 --> I9[expired]
  I7 --> I11[cancel rejected]
  I9 --> I12[payment rejected]
  MP1[Mercado Pago create] --> MP4[processing]
  MP4 --> MP5[GET reconciliation]
  PB1[PagBank QR order] --> PB4[charge emerges]
  PB4 --> PB6[duplicate rejected]
  PG1[Pagar.me order] --> PG3[paid threshold]
  PG1 --> PG4[failed threshold]
  PG1 --> PG8[exact threshold paid]
  AS1[Asaas create] -. transition unknown .-> ASU[deferred]
  MP4 --> MP18[processed/accredited]
```

The runtime graph currently exposes 85 nodes: 6 actors, 6 use cases, 11
provider-native resources, 61 executable scenario nodes, 40 known edges, and 1 deferred
evidence-gap nodes. Its `snapshot()` method exposes those nodes and edges to
local validation tools. Topology and lifecycle edges are defined in
`src/app/simulation/native_graph.py`. Use-case edges connect actors to
provider-native resources and executable scenario nodes; lifecycle edges then
preserve observed transitions between scenario IDs. Deferred edges remain explicit
so missing evidence is not converted into an invented common state transition.
The MRL adapter passes `observatory_nodes` and `observatory_edges` into the
runtime `Scenario`, so supervision uses this graph instead of the runtime's
three-node actor/scheduler fallback.

The adapter also emits one `graph_route` observation per declared edge. The
observation source is the edge's declared `from` node and its name is the
declared `to` node, matching the runtime observatory's route inference. These
events are the animated beams; declared edges are the persistent structural
beams. Deferred routes use the same visual path but retain `status: deferred`.
For a local inspection of the exact ordered stream, run
`python3 sandboxes/simulation/tools/show_native_graph.py --beams`.

The Mercado Pago async increment now preserves the documented
`processed/accredited` order and payment pair after processing. The exact
notification timing and duplicate behavior remain unknown.

The refund increment adds Mercado Pago partial/total refund scenarios and
PagBank partial/full charge cancellation scenarios. Their native statuses and
observation names remain distinct; the graph does not introduce a shared
`refunded` state.

The expiration increment adds Mercado Pago unpaid cancellation and both
documented expiration outcomes (`expired` and `canceled`). Pagar.me expiration
remains explicitly unknown until provider evidence establishes its event and
status behavior.

The authentication-error increment adds Asaas native 401 branches for missing
credentials, invalid credentials, and invalid environment. Credential values
remain sanitized; retryability and unknown-result semantics are not inferred.

The error-boundary increment adds documented Asaas 429 rate limiting, 403
forbidden access, and 500/transport-timeout unknown-result branches. The
simulation records native status and evidence while leaving retry policy
unsupported and create-result certainty unknown.

The observatory uses distinct supported runtime kinds and graph-derived numeric
layers. Every linked target is placed in a later rank, including lifecycle
scenario chains; unlinked nodes may share a rank. The kinds remain actors, use
cases, provider-native aggregates, scenario projections, and deferred
external-provider nodes. Observatory domains are split into one
`simulation-coordination` domain and one domain per provider, such as
`provider-asaas` and `provider-iugu`. Pix is the current method slice, not the
name of the whole simulation domain.

## Comparison boundary

Cross-provider comparison is limited to report shape, scenario attribution,
graph reachability, and inventories of native observation names. The inventory
does not rename provider events into a shared lifecycle vocabulary. A missing
provider event, retry rule, authentication rule, or response transition remains
an explicit unknown or deferred edge.
