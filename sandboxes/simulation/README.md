# OPP Domain Simulation

This directory contains the repository's single evolving deterministic domain
simulation. It supports discovery of payment-provider contracts before OPP Core
is defined.

The simulation follows the Python event-sourced MRL project shape. Provider
simulators remain provider-native; shared vocabulary in this project is a
hypothesis until supported by research, simulator observations, adapter
pressure, and an explicit model release.

## Current Phase

The five-provider documentation baseline is complete. All five native
create/retrieve increments are runnable with deterministic tests and scenario
reports. The project is now refining cross-provider lifecycle pressure. The
first bounded lifecycle/event-delivery increment is runnable for Pagar.me.

The selection evidence is recorded in
[`research/pix-simulator-selection.md`](../../research/pix-simulator-selection.md)
and the refined slice in
[`docs/slices/iugu_pix_creation.md`](docs/slices/iugu_pix_creation.md).

The current provider-native lifecycle graph is recorded in
[`docs/semantics/native_scenario_graph.md`](docs/semantics/native_scenario_graph.md).
It distinguishes executable transitions from explicitly deferred edges.

Run the pure scenario suite with `pytest -q sandboxes/simulation/tests` or
emit a canonical report with
`python3 sandboxes/simulation/tools/run_iugu_pix.py`. WNT MRL Runtime
supervision additionally requires the user-space runtime installation; start a
fresh session with `mrl-simulation supervise` after changing the graph so its
stream includes the `graph_route` beam observations.

## Layout

- `docs/semantics/`: current domain hypothesis and background knowledge.
- `docs/slices/`: candidate and refined vertical simulation slices.
- `docs/evaluation/`: future evaluation and EGD guidance.
- `src/`: shared event-sourced simulation code once a slice is runnable.
- `tests/`: deterministic unit, integration, and scenario tests.
- `tools/`: narrow repository-owned simulation utilities.

Validation receipts belong in the repository-level `runs/` directory and
change artifacts belong in `work/changes/`.

## Method Boundary

The canonical loop is:

```text
extract -> map -> iterative refine/build/refinement-check -> model EGD -> model release
```

The simulation does not define stable protocol semantics, perform payment
processing, select providers, route traffic, retry across providers, or handle
raw PAN/CVV. The WNT MRL Runtime adapter will be added at
`src/app/simulation/mrl_runtime_scenario.py` with the first runnable slice.
