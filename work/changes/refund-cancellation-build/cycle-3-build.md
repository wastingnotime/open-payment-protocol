# Refund and cancellation refinement — cycle 3 build

- Added PagBank charge cancellation with provider-native partial/full status behavior.
- Partial cancellation preserves `PAID`; full cancellation yields `CANCELED`.
- Full deterministic suite passed (`115 passed`).
- Existing scenario inventory remains 72 scenarios pending scenario exposure.
