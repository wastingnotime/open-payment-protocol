# Simulation Tests

Deterministic unit, integration, and scenario tests accompany runnable
simulation behavior. Tests must retain evidence links and avoid wall-clock
sleeps.

Every provider scenario report must retain its scenario name, observations,
event log, and provider-native projection. Observation payloads are tagged with
the scenario ID so runtime reports remain attributable when several providers
are compared.

Each observation also retains its event `type`, semantic `name`, provider
`source`, and structured `payload`; only the payload's provider-specific fields
remain intentionally unconstrained.

The `source` field must identify the provider registry that emitted the
observation. Framework-level Iugu replay observations may use `simulation`.

Run the full deterministic suite with `pytest -q sandboxes/simulation/tests`.

Cross-provider checks also ensure scenario reports do not introduce raw PAN,
CVV, equivalent cardholder-data field markers, or provider credential markers
such as API keys and access tokens.
The marker list is shared with the standalone validator.

Provider scenario registries must also be replayable: identical deterministic
inputs produce byte-equivalent report content across repeated runs.

The current five-provider inventory contains 61 scenarios; changes to that
total or to an individual provider count should update the relevant provider
backlog and refinement receipt.
Scenario identifiers also retain the native provider prefix used by the
corresponding backlog.

Shared report-field, source, prefix, and canonical-snapshot rules live in the
simulation package so pytest and the standalone validator use one contract.
