# Exported Contract Map

OPP is pre-v0.1. Nothing is stable yet.

| Surface | Status | Intended role |
| --- | --- | --- |
| `spec/` | Experimental | Language-neutral protocol semantics |
| `schemas/` | Experimental | Machine-readable representations |
| `conformance/` | Experimental | Observable compatibility behavior |
| `research/` | Internal evidence | Provider facts and comparison inputs |
| `simulators/` | Internal tool | Provider-native discovery validation |
| `sdk/` | Experimental binding | Language-specific access to OPP |
| `providers/` | Experimental implementation | Provider adapters |

Stable releases must identify exact versioned exports. Consumers must not depend
on research layout, simulator internals, or language-binding implementation
details.
