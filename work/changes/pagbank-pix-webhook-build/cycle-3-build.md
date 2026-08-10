# PagBank Pix webhook lifecycle — cycle 3 build

- Added `PB-PIX-013` for preserving the single HTTPS notification URL on the
  native order projection.
- The notification transport remains explicit as HTTPS POST; delivery timing
  and acknowledgement semantics remain unknown.
- Build: full deterministic suite passed (`84 passed`); 61 scenarios validated.
