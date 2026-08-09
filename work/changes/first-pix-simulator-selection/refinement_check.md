# Iugu Pix First-Slice Refinement Check

## Evidence

The implementation passes six deterministic tests and produces seven scenario
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
- The documented success transition can be added without normalizing invoice
  and embedded Pix statuses: both move to `paid` and retain native fields.

## Discrepancies and Unknowns

- The WNT MRL Runtime was installed from the local toolkit checkout and the
  adapter was verified with `mrl-simulation supervise --once`.
- Runtime inspection emitted 17 observations. The combined stream initially
  lacked scenario correlation; scenario IDs are now present in each semantic
  observation payload.
- Iugu's conflicting payer requirements remain unsupported/unknown combinations.
- Exact provider error bodies, idempotency retention, expiry, refunds, and
  webhook delivery remain deferred as documented in the slice plan.

## Decision

Keep the current slice boundary. Proceed to sandbox-observed validation before
adding lifecycle and webhook behavior.
