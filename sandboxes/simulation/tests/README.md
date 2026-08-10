# Simulation Tests

Deterministic unit, integration, and scenario tests accompany runnable
simulation behavior. Tests must retain evidence links and avoid wall-clock
sleeps.

Every provider scenario report must retain its scenario name, observations,
event log, and provider-native projection. Observation payloads are tagged with
the scenario ID so runtime reports remain attributable when several providers
are compared.
