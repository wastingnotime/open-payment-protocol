# Cross-provider Replay Refinement

The shared simulation is intended for deterministic discovery and comparison.
The final cycle adds a replay check across all provider registries, comparing
the report's minimum fields without requiring provider payloads to share a
schema. The assertion must capture two named snapshots per provider so a
future edit cannot accidentally compare a value to itself.
Canonical snapshots must sort reports by their reported scenario name so
registry insertion order cannot change the replay receipt.
Repeated registry runs must also return independent report projections.
Canonical JSON must reject non-standard floating-point values rather than
emitting implementation-specific replay output.
