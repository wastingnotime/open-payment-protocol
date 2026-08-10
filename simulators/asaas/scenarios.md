# Asaas Pix Scenario Backlog

Built scenarios:

- `AS-PIX-001`: create/retrieve a payment and retrieve its separate Pix QR code.
- `AS-PIX-002`: reject invalid payment input.
- `AS-PIX-003`: retrieve an unknown payment and retain the native not-found boundary.
- `AS-PIX-004`: retrieve an unknown Pix QR resource and retain the operation boundary.
- `AS-PIX-005`: reject a non-Pix billing type with the native validation boundary.
- `AS-PIX-006`: reject a non-positive payment value with the native invalid-value boundary.
- `AS-PIX-007`: missing due date preserves the native required-parameter boundary.
- `AS-PIX-008`: missing customer preserves the native required-parameter boundary.

Deferred: payment lifecycle, QR expiration, webhook delivery, external-reference
lookup, repetition behavior, and sandbox observation.
