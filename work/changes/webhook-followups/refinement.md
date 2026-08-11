# Webhook delivery follow-up refinement

## Built boundaries

The five providers now have bounded webhook or notification scenarios that
preserve their native transports, authenticity mechanisms, event names, and
endpoint/configuration rules.

## Deliberately unresolved

Retry timing, acknowledgement policy, ordering, duplicate identity, delivery
timing, and exact payload schemas remain provider-specific unknowns. The
simulation must not introduce a shared webhook contract from the comparable
report envelope.

## Build decision

The next webhook build should be selected by a new dated official or sanitized
Sandbox observation for one provider and one missing behavior. Until then,
retain the current event/notification scenarios and their explicit unknowns.
