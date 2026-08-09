# Asaas Documentation Fixtures

These sanitized fixtures were constructed from the official Asaas documentation
and OpenAPI schema through `https://docs.asaas.com/mcp` on 2026-08-09. They are
documentation fixtures, not Sandbox recordings.

- `create-pix-payment-request.json`: minimal documented Pix creation request,
  with non-live identifiers and a placeholder future date.
- `create-pix-payment-response.json`: slice-relevant subset assembled from the
  documented response schema examples; it is not a captured provider response.
- `pix-qr-code-response.json`: slice-relevant subset assembled from the
  documented QR Code response schema with the large Base64 example replaced.

Do not use these files as evidence for undocumented defaults, field omission,
initial status, uniqueness, or idempotency behavior.
