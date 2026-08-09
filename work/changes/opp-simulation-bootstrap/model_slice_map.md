# Candidate Model Slice Map

Status: initial mapping; no slice has entered build.

| Order | Candidate slice | Primary uncertainty | Entry condition |
| --- | --- | --- | --- |
| 1 | Provider-native Pix creation and retrieval | Resource, validation, identifiers, initial state | Five-provider official-source research and sanitized fixtures |
| 2 | Successful transition and native event | Timing, finality, event payload and delivery | Slice 1 refinement plus lifecycle/webhook evidence |
| 3 | Failed or expired transition | Failure state, finality, error/result certainty | Provider lifecycle and error evidence |
| 4 | Repetition and reconciliation | Idempotency, timeout ambiguity, caller-reference lookup | Provider idempotency evidence |
| 5 | Thin adapter comparison | Smallest faithful shared semantics | Runnable native slices across all five providers |

## Selection Decision

Slice 1 is selected for evidence refinement. It is not ready to build. The next
action is provider research using current official documentation, with claims
labeled documented, sandbox-observed, inferred, or unknown.
