# Iugu Pix First-Slice Run

- Date: 2026-08-09
- Slice: `iugu_pix_creation`
- Command: `pytest -q sandboxes/simulation/tests`
- Result: 5 tests passed
- Report command: `python3 sandboxes/simulation/tools/run_iugu_pix.py`
- Scenario count: 6
- Evidence mode: documentation-derived deterministic simulation; not sandbox-observed

## Scenario Receipt

| Scenario | Result | Native evidence exercised |
| --- | --- | --- |
| IUGU-PIX-001 | Passed | invoice create, Pix projection, provider-ID retrieval |
| IUGU-PIX-002 | Passed | documented required-field validation boundary |
| IUGU-PIX-003 | Passed | unknown invoice retrieval boundary |
| IUGU-PIX-004 | Passed | documented reused idempotency-key conflict |
| IUGU-PIX-005 | Passed | external-reference and order-ID lookup paths |
| IUGU-PIX-006 | Passed | canonical replay equality |

The generated report is intentionally not checked in; it contains deterministic
derived output and can be regenerated with the documented command.
