# Iugu Provider Simulator

Status: selected and runnable through the shared simulation environment.

This internal simulator will reproduce the documented Iugu Pix invoice
creation and retrieval contract. It is a discovery tool and does not implement
OPP internally.

The implementation belongs to the repository's shared deterministic simulation
under `sandboxes/simulation/`. This directory records the provider-native
contract and scenario boundary; it must not become a separate simulation
project or protocol authority.

See [scenarios.md](scenarios.md) and the refined
[simulation slice](../../sandboxes/simulation/docs/slices/iugu_pix_creation.md).

The executable implementation is under
`../../sandboxes/simulation/src/app/simulation/`; this directory remains a
provider-native contract boundary, not a second implementation surface.
