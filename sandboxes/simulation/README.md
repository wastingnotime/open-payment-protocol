# OPP Domain Simulation

This directory contains the repository's single evolving deterministic domain
simulation. It supports discovery of payment-provider contracts before OPP Core
is defined.

The simulation follows the Python event-sourced MRL project shape. Provider
simulators remain provider-native; shared vocabulary in this project is a
hypothesis until supported by research, simulator observations, adapter
pressure, and an explicit model release.

## Current Phase

The project is in `extract -> map candidate slices`. There is no runnable slice
yet because the five-provider evidence baseline has not been completed.

The next candidate is documented in
[`docs/slices/provider_native_pix_creation.md`](docs/slices/provider_native_pix_creation.md).
Its refinement gate requires documented create and retrieve behavior for each
selected provider. Building before that gate would create circular validation.

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
