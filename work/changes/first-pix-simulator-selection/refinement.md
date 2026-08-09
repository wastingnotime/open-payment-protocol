# First Pix Simulator Selection

## Outcome

The five-provider evidence baseline was compared and Iugu was selected for the
first provider-native simulator increment. Six build-now scenarios and explicit
deferred scenarios are recorded.

## Boundary Decisions

- The MRL project remains one shared environment under `sandboxes/simulation/`.
- `simulators/iugu/` records provider-native intent; it is not a second project.
- The first slice models an Iugu invoice, not a generic payment.
- Other providers enter as incremental slices rather than blocking the first
  build behind a five-provider big bang.
- No protocol semantics, schemas, adapters, or conformance claims are extracted.

## Next Action

Build IUGU-PIX-001 through IUGU-PIX-006 using the Python event-sourced shape,
including the repository-owned WNT MRL Runtime adapter and deterministic tests.
