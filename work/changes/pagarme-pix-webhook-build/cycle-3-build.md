# Pagar.me webhook lifecycle — cycle 3 build

- Added `PG-PIX-014` for the distinct provider-native `order.paid` signal.
- The slice now demonstrates both charge-level and order-level webhook event
  names without collapsing them.
- Build: full deterministic suite passed (`78 passed`); 55 scenarios validated.
