# Contributing

OPP is discovery-driven. Record provider reality before proposing a common
abstraction.

## Research Rules

1. Prefer current official provider documentation.
2. Record source URLs and the research date.
3. Label each claim as documented, inferred, sandbox-observed, or unknown.
4. Preserve provider-native names, payload shapes, states, and quirks.
5. Note ambiguities instead of silently filling gaps.
6. Add only sanitized documentation fixtures or sandbox recordings.
7. Never commit secrets, customer data, PAN, CVV, or other sensitive data.

Use `research/template.md` for each provider. A protocol proposal must cite the
provider evidence from which its invariant was extracted.

## Change Discipline

Keep commits focused and use conventional commit prefixes. Document how a
simulator was validated and retain relevant receipts under `runs/`.
