# Iugu Pix webhook lifecycle — cycle 3 build

- Added `IUGU-PIX-016` for configuring an `invoice.status_changed` trigger.
- The configuration preserves form-urlencoded transport and records only the
  boolean presence of optional Basic Authentication.
- Build: full deterministic suite passed (`81 passed`); 58 scenarios validated.
