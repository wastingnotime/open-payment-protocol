# Error boundary refinement — cycle 1 build

- Added Asaas authentication handling for missing token, invalid token, invalid environment, and sanitized success.
- Authentication errors preserve documented HTTP 401 codes without storing credential values.
- Full deterministic suite passed (`132 passed`).
- Existing inventory remains 77 scenarios and 70 graph nodes.
