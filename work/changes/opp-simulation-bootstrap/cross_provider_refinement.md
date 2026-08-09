# Cross-Provider Create/Retrieve Refinement

## Evidence

The shared runtime now executes 17 provider-native scenarios across Asaas,
Iugu, Mercado Pago, PagBank, and Pagar.me. The five create/retrieve increments
pass 18 deterministic tests and emit 44 runtime observations.

## Resource Boundaries

| Provider | Native first-slice shape | QR boundary |
| --- | --- | --- |
| Asaas | `payment` | separate QR retrieval |
| Iugu | `invoice` with embedded Pix object | embedded |
| Mercado Pago | `order` with payment transaction | embedded |
| PagBank | `order` with QR and no initial charge | embedded QR; charge later |
| Pagar.me | `order` → `charge` → `last_transaction` | embedded in transaction |

## Model Pressure

- No single provider resource can be made authoritative without erasing native
  hierarchy or QR retrieval behavior.
- Money varies between decimal JSON numbers, decimal strings, and integer
  centavos; the simulation must retain the provider representation.
- Initial statuses are provider-native and cannot yet become one shared enum.
- Idempotency evidence differs: documented conflicts, same-response promises,
  and unknown behavior coexist.
- QR data may be embedded, separately retrieved, or attached to an order before
  a charge exists.

## Lifecycle Gate

All five create/retrieve slices are built and refinement-checked. The next
increment should model one documented successful transition per provider,
starting with Iugu's already-built `pending → paid` transition as the reference
for adapter-pressure comparison. It must not introduce a common payment model,
status enum, money type, or webhook contract.

## Remaining Unknowns

Sandbox observations, asynchronous processing, expiration, refunds, webhook
delivery, and timeout/result certainty remain provider-specific work.
