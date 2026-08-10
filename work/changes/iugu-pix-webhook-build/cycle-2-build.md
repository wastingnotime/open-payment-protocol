# Iugu Pix webhook lifecycle — cycle 2 build

- Added `IUGU-PIX-015` for a canceled `invoice.status_changed` event.
- The canceled payload omits paid-only fields, preserving Iugu's native
  status-dependent shape.
- Build: full deterministic suite passed (`80 passed`); 57 scenarios validated.
