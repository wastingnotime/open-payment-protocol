# Native Scenario Graph Refinement

The simulation graph now connects executable lifecycle-pressure scenarios while
keeping provider-native aggregates, statuses, and evidence links intact.

- Known edges: Iugu lifecycle outcomes, Mercado Pago asynchronous processing and
  retrieval, PagBank charge emergence/duplicate rejection, and Pagar.me
  threshold outcomes.
- Deferred edges: Asaas Pix finalization and Mercado Pago asynchronous payment
  finalization, both explicitly unsupported by current evidence.

`pytest -q sandboxes/simulation/tests` passes with 67 deterministic tests.
