# PagBank Pix webhook lifecycle — cycle 2 build

- Added `PB-PIX-012` for a mismatched raw-payload authenticity token.
- The notification is marked for discard; retry, acknowledgement, and
  duplicate behavior remain unknown.
- Build: full deterministic suite passed (`83 passed`); 60 scenarios validated.
