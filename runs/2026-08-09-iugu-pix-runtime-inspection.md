# Iugu Pix Runtime Inspection

- Date: 2026-08-09
- Command: `mrl-simulation supervise --once --scenario-factory app.simulation.mrl_runtime_scenario:create_simulation`
- Direct runner: `SimulationRunner().run(create_simulation())`
- Result: runtime started successfully; 84 observations emitted
- Evidence mode: deterministic documentation-derived simulation; not provider sandbox evidence

## Observed Runtime Shape

The runtime emitted `scenario_started`, one scheduled action, forty-two scenario
traces, and `scenario_finished`. Each semantic observation now carries its
scenario identifier in the payload, allowing the combined runtime stream to be
partitioned without introducing separate simulations per provider or scenario.

## Refinement Finding

The first adapter version emitted valid semantic observations but did not carry
an explicit scenario identifier. The shared environment made that ambiguity
visible during inspection. The identifier is now attached at scenario-finalize
time and remains provider-neutral runtime metadata.

The success-transition refinement also exposes the native
`invoice.status_changed` event as a semantic observation rather than leaving it
only in the internal event store.

## Remaining Pressure

All ten scenarios currently run at the same simulated timestamp because this
slice models create/retrieve and deterministic query behavior only. Lifecycle
time advancement remains intentionally deferred until provider evidence supports
it.
