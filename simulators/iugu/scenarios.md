# Iugu Pix Scenario Backlog

Evidence labels refer to the files under `research/iugu/`.

## Build Now

### IUGU-PIX-001 — Create and retrieve an invoice

Given the sanitized documented request, create an Iugu invoice with Pix enabled,
persist its native identifiers and initial response, then retrieve the same
invoice by provider ID.

Expected observations:

- the create command retains `email`, `due_date`, integer `price_cents`, item
  description and quantity, and `payable_with: ["pix"]`;
- the response retains the invoice ID, native status, BRL totals, secure URL,
  and embedded Pix data;
- retrieval returns the same provider-native invoice projection;
- no OPP-normalized resource or status is emitted.

### IUGU-PIX-002 — Reject a documented invalid request

Reject a request missing a field that the selected create reference explicitly
marks required. Emit the Iugu-native HTTP/status/error evidence available for
that validation; do not fabricate a more precise body where documentation is
incomplete.

### IUGU-PIX-003 — Retrieve an unknown invoice

Query an unrecognized provider invoice ID and return only the not-found
behavior established by Iugu evidence. If the exact body remains unknown, the
simulator exposes that uncertainty explicitly.

### IUGU-PIX-004 — Repeat an idempotency key

Create once with an `Idempotency-Key`, then repeat the create command using the
same key. Reproduce the documented HTTP 409 behavior without assuming key
retention duration or payload-mismatch semantics.

### IUGU-PIX-005 — Lookup by caller references

Retrieve using supported external identifiers such as `order_id` or
`external_reference`, keeping their meanings distinct. This scenario validates
reconciliation capability; it does not assert uniqueness beyond documentation.

### IUGU-PIX-006 — Deterministic replay

Run the same seed, clock, commands, and identifier source twice. Event history,
projection, observations, and invariant results must be byte-equivalent after
canonical serialization.

## Refinement Scenarios — Do Not Invent Yet

- minimal Pix payer-field combinations;
- changed payload under a reused idempotency key;
- exact 401, 409, and all 422 response bodies;
- Pix payment success, cancellation, expiration, and recovery transitions;
- notification delivery, retries, duplicates, and ordering;
- timeout and server-error result certainty;
- test-mode timing and behavior.

These enter build only when documentation or sanitized sandbox observations
establish their behavior.

## Invariants

- Every simulated branch carries an evidence label and source locator.
- Money remains integer cents and currency remains the native documented value.
- Invoice and embedded Pix statuses remain separate where evidence distinguishes them.
- No raw PAN, CVV, credential, real customer data, or real tax identifier appears.
- Unsupported and unknown behaviors are explicit.
- Replaying a scenario never depends on wall-clock time.

### IUGU-PIX-007 — Documented successful Pix transition

Create a pending invoice, apply the documented `pending -> paid` invoice and
`qr_code_created -> paid` Pix transitions, attach a sanitized end-to-end ID,
and retrieve the paid invoice. Keep invoice and embedded Pix statuses distinct
and emit the native `invoice.status_changed` event.

Expiry, refunds, webhook delivery, and test-mode timing remain deferred.

### IUGU-PIX-008 — Documented cancellation transition

Create a pending invoice, apply the documented `pending -> canceled` invoice
transition, and retain the embedded Pix status as provider-native state. This
does not claim that the QR status or cancellation timing is fully documented.
