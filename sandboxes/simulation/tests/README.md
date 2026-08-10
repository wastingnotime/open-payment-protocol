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

Run the full deterministic suite with `pytest -q sandboxes/simulation/tests`.

Cross-provider checks also ensure scenario reports do not introduce raw PAN,
CVV, or equivalent cardholder-data field markers.
