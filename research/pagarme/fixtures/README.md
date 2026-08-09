# Pagar.me Documentation Fixtures

These sanitized fixtures were assembled from official Pagar.me Markdown pages
discovered through `https://docs.pagar.me/llms.txt` on 2026-08-09. They are not
test or production recordings.

- `create-pix-order-request.json`: conservative Pix order request with synthetic
  customer and merchant references.
- `create-pix-order-response.json`: slice-relevant order, charge, and transaction
  hierarchy adapted from the documented response.

Do not infer idempotency, complete field requirements, omission rules, or
production timing from these fixtures.
