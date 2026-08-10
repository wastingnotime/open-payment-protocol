# Iugu webhook events refinement — cycle 1 build

- Added four documented Iugu form-urlencoded event envelopes: `invoice.due`, `invoice.payment_failed`, `invoice.refund`, and `invoice.rejected`.
- Event-only semantics remain explicit; no delivery retry or state-transition behavior was invented.
- Full deterministic suite passed (`139 passed`).
- Provider inventory now contains 84 scenarios.
