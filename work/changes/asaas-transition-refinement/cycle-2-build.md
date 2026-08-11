# Asaas Pix transition — refinement/build cycle 2

The Asaas success transition remains deferred.

The current executable boundary preserves `PAYMENT_RECEIVED`, redelivery, overdue, and invalid-envelope events. It does not project `RECEIVED` or `CONFIRMED` onto the payment after creation because the collection-specific Pix relationship and timing remain unestablished.

Build result: no new success scenario; `AS-PIX-DEFERRED-SUCCESS` remains the only deferred graph edge.

Validation: `pytest -q sandboxes/simulation/tests` — 157 passed; `python3 sandboxes/simulation/tools/validate_scenarios.py` — 93 scenarios validated.

