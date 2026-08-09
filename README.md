# Open Payment Protocol

Open Payment Protocol (OPP) is an effort to define a small, stable,
provider-neutral contract between applications and payment providers.

> Implement OPP once for a provider; use that provider in any OPP-compatible
> application.

OPP is not a processor, gateway, or orchestration platform. It is the narrow
waist between payment consumers and provider implementations.

## Status

OPP is in discovery, before v0.1. There is no stable protocol or compatibility
claim yet.

The first research set covers Asaas, Iugu, Mercado Pago, PagBank, and Pagar.me.
The project records each provider faithfully, validates that understanding with
local contract simulators and sandbox evidence where possible, and only then
extracts shared semantics.

```text
provider contracts
  -> provider simulators
  -> provider adapters
  -> comparison
  -> discovered invariants
  -> OPP Core
```

## Repository Map

- `research/`: provider-specific evidence and the comparison matrix
- `simulators/`: provider-native local contract simulators
- `spec/`: emerging language-neutral semantics
- `schemas/`: machine-readable protocol schemas
- `conformance/`: reusable compatibility behavior
- `sdk/go/`: first language binding
- `providers/go/`: initial provider implementations
- `contracts/`: repository boundary and export status

The specification, schemas, and conformance behavior will be authoritative.
Language bindings and provider implementations will not define OPP semantics.

## Scope

Candidate areas include payment creation and retrieval, cancellation, refunds,
lifecycle states, errors, events, idempotency, capabilities, payment methods,
security boundaries, and conformance.

OPP deliberately excludes provider selection, routing, fallback, provider
weighting, multi-provider retry, accounting, settlement, fraud, credential
storage, and merchant business rules.

## Contributing

Start with [CONTRIBUTING.md](CONTRIBUTING.md). Provider research must distinguish
documented facts, inference, sandbox observations, and unknowns. Never include
secrets, personal data, or cardholder data.

## License

Licensing has not yet been selected. Until a license is added, copyright law
applies and no reuse license is granted.
