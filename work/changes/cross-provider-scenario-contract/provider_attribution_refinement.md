# Provider Attribution Refinement

Scenario envelopes carry a provider source label for comparison and runtime
inspection. The next build checks that each registry's observations identify
their own provider, without requiring common event names or payload fields.
The Iugu replay-comparison observation is the deliberate framework-level
exception and uses `simulation` as its source.
