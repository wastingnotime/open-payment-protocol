# Repository Guidelines

## Repository Identity

Open Payment Protocol (OPP) owns the discovery and eventual language-neutral
contract between applications and payment-provider implementations. Its core is
extracted from demonstrated provider behavior; it is not invented from provider
marketing categories or from any one language binding.

## Responsibilities

- Record provider contracts and evidence without forcing early uniformity.
- Build faithful provider simulators and thin adapters for discovery.
- Define versioned semantics, schemas, security boundaries, and conformance.
- Preserve provider differences through capabilities and namespaced extensions.

## Non-Responsibilities

- Do not implement payment processing, orchestration, routing, fallback, or fee
  optimization.
- Do not own merchant applications, accounting, settlement, fraud, credential
  storage, or deployment topology.
- Do not make Go interfaces or simulator behavior the protocol source of truth.
- Do not require raw PAN, CVV, or equivalent cardholder data in OPP Core.

## Surface Map

- `research/`: experimental provider facts, fixtures, recordings, and comparison.
- `simulators/`: internal discovery tools that preserve provider-native behavior.
- `spec/`, `schemas/`, `conformance/`: public but experimental until explicitly
  versioned stable; these become the exported protocol surfaces.
- `sdk/` and `providers/`: bindings and implementations, never protocol authority.
- `contracts/`: repository boundary and export-status guidance.
- `work/` and `runs/`: active artifacts and validation receipts.

No OPP surface is stable during the pre-v0.1 discovery phase.

## Working Rules

- Follow: provider contracts -> simulators -> adapters -> comparison -> invariants
  -> OPP Core.
- Prefer current official provider documentation and record source URL and access
  date. Separate documented, inferred, sandbox-observed, and unknown behavior.
- Never commit secrets, real customer data, or cardholder data. Sanitize fixtures.
- Keep unsupported behavior explicit; do not silently emulate capabilities.
- Keep changes narrow and commit each completed change before unrelated work.
- Use conventional commit prefixes.

## Visitor Guidance

Read `README.md`, `contracts/README.md`, and `research/template.md` first. Depend
only on surfaces explicitly marked stable. Use WNT campaigns or findings for
cross-repository coordination; do not couple consumers to research or simulator
internals.

## WNT Repository Defaults

Shared WNT guidance lives in user-space capabilities and the WNT MCP surface.

- Use `wnt capability show mcp-usage` for MCP guidance.
- Use `wnt capability show project-surfaces` for project-surface defaults.
- Keep WNT toolkit policy out of the repository-local source of truth.

<!-- wnt:wnt-toolkit-hints:start -->
## WNT Toolkit Hints

Resolve current WNT guidance from user or container space:

```bash
wnt capability list
wnt capability show <capability-name>
```
<!-- wnt:wnt-toolkit-hints:end -->
