# Pix Simulator Selection Review

Status: discovery decision, not an OPP contract.

## Decision

Build the first provider-native simulator slice for **Iugu**. This is an
incremental implementation decision inside the shared simulation environment;
it does not make Iugu the protocol model or defer the other providers from the
five-provider comparison.

## Selection Criteria

The first simulator should maximize documented behavior that can be reproduced
without inventing semantics:

1. create and retrieve contracts are explicit;
2. initial resource and Pix output are represented in sanitized fixtures;
3. money, identifiers, and native statuses are sufficiently defined;
4. repeated-create behavior and reconciliation have evidence;
5. errors can be made provider-native;
6. the slice creates useful contrast for later providers;
7. unresolved questions do not block the bounded create/retrieve path.

## Evidence Review

| Provider | Create/retrieve readiness | Repetition/reconciliation | Principal blocker or pressure | Decision |
| --- | --- | --- | --- | --- |
| Iugu | Strong: invoice create/get, integer `price_cents`, embedded Pix response, invoice status vocabulary | `Idempotency-Key` and external-ID lookup documented | Minimal payer fields conflict across pages; exact 401/409/422 bodies incomplete | **First** |
| Mercado Pago | Strong: Orders API create/get, decimal-string money, explicit initial status and QR output | Mandatory idempotency; GET reconciliation documented | Async create can temporarily omit information; repeated-key outcome needs clarification | Second-wave candidate |
| Pagar.me | Strong order/charge/transaction hierarchy and deterministic Pix test rules | No create idempotency evidence | Minor-unit guarantee and Gateway/PSP customer requirements incomplete | Best lifecycle-transition candidate after creation slice |
| Asaas | Simple payment create/get and separate QR retrieval | No create idempotency or established caller-reference lookup | Initial Pix status and repetition behavior unknown | Defer pending sandbox evidence |
| PagBank | Clear order/QR create/get and same-response idempotency promise | Header details incomplete | No initial order status, charge emerges only after payment, conflicting default expiry | Preserve for resource-emergence comparison |

## Why Iugu First

Iugu permits a narrow, deterministic slice centered on one native aggregate:
an invoice with embedded Pix data. The slice can exercise create, retrieve,
native validation, idempotency conflict, and caller-reference lookup without
normalizing another provider's order, payment, or charge model.

The unresolved payer-field conflict is handled by using the conservative
documentation fixture and by limiting validation claims to fields explicitly
supported by evidence. The simulator must label unestablished combinations as
unsupported or unknown rather than guessing.

## Sequence After Iugu

1. Add Mercado Pago creation/retrieval to pressure decimal-string money,
   two-level status, mandatory idempotency, and asynchronous results.
2. Add PagBank to pressure resource emergence: QR Code now, charge later.
3. Add Pagar.me to pressure order/charge/transaction identity and deterministic
   lifecycle outcomes.
4. Add Asaas to pressure a payment-centered resource with separate QR retrieval
   and weaker repetition evidence.

This order is an implementation-risk sequence, not a provider quality ranking.

## Non-Decision

No shared `Payment`, status enum, error envelope, money type, or idempotency
contract is selected here. Those remain hypotheses until multiple native
simulators and thin adapters create evidence for extraction.
