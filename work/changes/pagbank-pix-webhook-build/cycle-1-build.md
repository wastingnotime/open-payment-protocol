# PagBank Pix webhook lifecycle — cycle 1 build

- Added `PB-PIX-011` for the paid order notification.
- The notification preserves the full order shape, emerging `PAID` charge,
  QR code, and PagBank's raw-payload SHA-256 authenticity boundary.
- Build: focused PagBank tests passed (`11 passed`).
