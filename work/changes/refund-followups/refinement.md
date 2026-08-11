# Refund and cancellation follow-up refinement

## Current executable boundary

Mercado Pago has native partial and total refund scenarios. PagBank has native
partial and full charge-cancellation scenarios. Their resource names, status
fields, and observation names remain distinct.

## Next provider gates

- Asaas: research must establish Pix refund events and the payment status
  projection before a refund scenario is added.
- Iugu: documented refund webhook names exist, but the relationship between
  those events, invoice state, and Pix funds remains incomplete.
- Pagar.me: refund operation and Pix transaction transitions require evidence;
  no scenario is added from the broader charge vocabulary.
- PagBank: Pix-specific refund rules and QR state after cancellation remain
  unknown; the existing charge cancellation slice is not generalized.

## Build decision

Do not add a shared `refunded` state. Build the next provider only after a
provider-native operation, status projection, amount boundary, and evidence
source are established.
