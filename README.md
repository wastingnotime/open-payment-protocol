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
- `sandboxes/simulation/`: deterministic domain simulation used to refine the model
- `contracts/`: repository boundary and export status

The simulation is an internal discovery environment. It preserves provider
differences and produces evidence for later protocol extraction; it is not an
authoritative OPP implementation. See
[`sandboxes/simulation/README.md`](sandboxes/simulation/README.md).

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

Implementation artifacts—including schemas, conformance tests, SDKs, provider
adapters, simulators, and reference implementations—are licensed under the
[Apache License 2.0](LICENSE). The protocol specification under `spec/` is
licensed separately under [CC BY 4.0](spec/LICENSE.md).

See the [licensing boundary](contracts/licensing.md) for exact scope. These
licenses do not grant certification status or permission to make protected
compatibility claims.
