# Provider-Native Scenario Graph

Status: internal discovery graph; not OPP protocol authority.

The graph expands the simulation beyond create/retrieve nodes while preserving
provider-native lifecycle and resource boundaries.

```mermaid
flowchart LR
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
  MP4 -. finalization unknown .-> MPU[deferred]
```

The runtime graph currently exposes 20 nodes: 18 executable scenario nodes and
2 deferred evidence-gap nodes. Its `snapshot()` method exposes those nodes and
edges to local validation tools. Executable edges are defined in
`src/app/simulation/native_graph.py` and every executable edge points to
scenario IDs in the provider scenario registry. Deferred edges remain explicit
so missing evidence is not converted into an invented common state transition.
The MRL adapter passes `observatory_nodes` and `observatory_edges` into the
runtime `Scenario`, so supervision uses this graph instead of the runtime's
three-node actor/scheduler fallback.
