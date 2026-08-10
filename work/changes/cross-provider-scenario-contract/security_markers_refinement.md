# Security Marker Refinement

Scenario reports must remain sanitized discovery artifacts. In addition to
cardholder-data markers, validation will reject common credential markers:
`api_key`, `access_token`, and `secret_key`.
The marker list will be shared by pytest and the standalone validator.
