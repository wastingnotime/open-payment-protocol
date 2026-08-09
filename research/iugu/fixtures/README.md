# Iugu Documentation Fixtures

These sanitized fixtures were assembled from the official Iugu OpenAPI
definitions through `https://dev.iugu.com/mcp` on 2026-08-09. They are not live
or test-mode recordings.

- `create-pix-invoice-request.json` is a candidate request assembled from the
  documented fields. Exact minimal payer requirements remain unknown.
- `create-pix-invoice-response.json` is a sanitized, slice-relevant subset of
  the documented response example.

Do not use these fixtures as evidence for idempotency, field omission, complete
status sets, or error behavior.
