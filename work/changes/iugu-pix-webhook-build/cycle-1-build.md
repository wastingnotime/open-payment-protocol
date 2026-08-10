# Iugu Pix webhook lifecycle — cycle 1 build

- Added `IUGU-PIX-014` for a paid `invoice.status_changed` event.
- The event preserves Iugu's documented form-urlencoded transport and native
  invoice/Pix fields, including the Pix end-to-end ID.
- Build: focused Iugu tests passed (`15 passed`).
