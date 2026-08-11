# Webhook delivery semantics — refinement/build cycle 2

The provider-specific webhook and notification envelopes remain executable at their current evidence boundary.

Retry timing, acknowledgement policy, ordering, duplicate identity, delivery timing, and exact payload schemas remain unknown. Comparable report fields are not promoted into a shared webhook contract.

Build result: no cross-provider delivery semantics added; the next build requires one provider-specific official or sanitized Sandbox observation.

Validation: `pytest -q sandboxes/simulation/tests` — 157 passed; `python3 sandboxes/simulation/tools/validate_scenarios.py` — 93 scenarios validated.

