# Exported Contract Map

OPP is retired and archived at pre-v0.1. No surface became stable.
See [the retirement record](https://github.com/wastingnotime/open-payment-protocol/blob/main/contracts/decommission.md).

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

Licensing is defined separately from export stability. See
[`licensing.md`](licensing.md) for the license applying to each surface and the
boundary between copyright licensing and future compatibility claims.
