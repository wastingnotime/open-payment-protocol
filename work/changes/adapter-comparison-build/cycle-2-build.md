# Thin adapter comparison — refinement/build cycle 2

The thin adapter-pressure report remains a discovery tool rather than protocol authority.

It now reports the five native resource/QR/money boundaries and current observation inventories without a normalized payment, status, money, or webhook type.

Build result: comparison output is ready for a future provider-specific adapter experiment; no consumer-facing adapter contract is released.

Validation: `pytest -q sandboxes/simulation/tests` — 157 passed; `python3 sandboxes/simulation/tools/validate_scenarios.py` — 93 scenarios validated.

