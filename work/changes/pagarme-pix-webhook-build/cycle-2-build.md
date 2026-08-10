# Pagar.me webhook lifecycle — cycle 2 build

- Added `PG-PIX-013` for querying a recorded webhook delivery.
- Query preserves native delivery fields without exposing a normalized event
  contract.
- Build: full deterministic suite passed (`77 passed`); 54 scenarios validated.
