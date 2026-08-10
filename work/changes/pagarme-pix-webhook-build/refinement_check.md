# Pagar.me Pix lifecycle and webhook refinement check

## Built

- `PG-PIX-010`: documented paid outcome followed by one `charge.paid`
  webhook delivery with native `sent` status.
- `PG-PIX-011`: documented failed outcome followed by one
  `charge.payment_failed` delivery attempt with native `failed` status.
- `PG-PIX-012`: failed delivery manually resent with incremented attempts.
- `PG-PIX-013`: recorded delivery queried with native delivery fields.
- `PG-PIX-014`: distinct `order.paid` delivery signal.
- Webhook records preserve the documented `hook_...` identity shape,
  configured URL, event, attempts, response status, and delivery state.

## Deliberately unknown

Retry timing, acknowledgement policy, ordering, duplicate semantics,
authentication/signatures, and exact event payload schemas remain outside this
increment because the reviewed evidence does not establish them.

## Validation

- `pytest -q sandboxes/simulation/tests`: 75 passed.
- `python3 sandboxes/simulation/tools/validate_scenarios.py`: 52 scenarios.
- MRL runtime adapter: 45 graph nodes, 60 graph edges, 60 route observations.
