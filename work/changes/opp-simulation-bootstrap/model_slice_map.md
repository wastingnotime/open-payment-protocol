# Candidate Model Slice Map

Status: five-provider evidence review complete; first slice built and refinement-checked.

| Order | Candidate slice | Primary uncertainty | Entry condition |
| --- | --- | --- | --- |
| 1 | Iugu-native Pix invoice creation and retrieval | Validation, identifiers, native initial representation | Built; refinement check passed |
| 2 | Mercado Pago, PagBank, Pagar.me, and Asaas create/retrieve increments | Resource hierarchy and provider differences | Mercado Pago built; refine remaining providers one at a time |
| 3 | Successful transition and native event | Timing, finality, event payload and delivery | Runnable creation slice plus lifecycle evidence; Pagar.me leads |
| 4 | Failed or expired transition and result certainty | Failure state, finality, timeout ambiguity | Provider lifecycle and error evidence |
| 5 | Thin adapter comparison | Smallest faithful shared semantics | Runnable native slices across all five providers |

## Selection Decision

Iugu is selected for the first build because its bounded create/retrieve path
has the strongest combined evidence for resource identity, integer-cent money,
embedded Pix output, native status, idempotency, caller-reference lookup, and
errors. This is an implementation-risk decision, not protocol authority.

See `research/pix-simulator-selection.md` and
`sandboxes/simulation/docs/slices/iugu_pix_creation.md`.
