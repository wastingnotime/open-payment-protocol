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

## Contribution Licensing

By intentionally submitting a contribution for inclusion in this repository,
you agree to license it under the license applicable to the contributed
surface: CC BY 4.0 for `spec/`, and Apache-2.0 for other repository content
unless that content is separately marked. Do not contribute material you do not
have the right to submit under those terms.

No contributor license agreement, certification program, or compatibility mark
policy is currently established. Any future policy will be documented
separately and will not be inferred from acceptance of a contribution.
