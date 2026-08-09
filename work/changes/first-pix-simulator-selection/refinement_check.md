# Iugu Pix First-Slice Refinement Check

## Evidence

The implementation passes five deterministic tests and produces six scenario
results. The provider projection preserves invoice identity, integer-cent
amounts, `pix` output, native `pending`/`qr_code_created` statuses, caller
references, and the documented 409 idempotency conflict.

## Model Pressure

- A provider-specific validation error must carry evidence and may remain less
  precise than a production response when the official envelope is incomplete.
- Idempotency conflict is represented as a native error, not a shared retry
  policy.
- Retrieval by provider ID and caller-reference lookup are separate queries.
- The first slice can be deterministic without modeling payment success,
  expiration, webhooks, or a normalized payment aggregate.

## Discrepancies and Unknowns

- The optional runtime package is not installed in this environment, so the
  adapter factory is present but supervision requires the WNT runtime install.
- Iugu's conflicting payer requirements remain unsupported/unknown combinations.
- Exact provider error bodies, idempotency retention, and lifecycle transitions
  remain deferred as documented in the slice plan.

## Decision

Keep the current slice boundary. Proceed to sandbox-observed validation or
install the WNT runtime for supervised observation before adding lifecycle and
webhook behavior.
