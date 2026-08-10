# Pagar.me webhook lifecycle — cycle 1 build

- Added `PG-PIX-012` for an explicitly manual resend of a failed webhook.
- The delivery record preserves the same webhook identity and increments
  `attempts` from 1 to 2; automatic retry timing remains out of scope.
- Build: focused Pagar.me tests passed (`12 passed`).
