# Expiration follow-up refinement

## Pagar.me

The provider research documents Pix transaction statuses and simulator
success/failure thresholds, but does not establish an unpaid-QR expiration
event or status. Keep expiration out of the simulator until that evidence is
available.

## PagBank

The QR creation contract exposes an explicit `expiration_date`, but the
reviewed lifecycle evidence does not establish the post-expiry order, QR, or
charge state. A timestamp field alone is insufficient to build a transition.

## Build decision

No provider-native expiration transition is added. Mercado Pago remains the
only executable expiration slice; the graph must continue to represent these
two provider gaps as research work rather than inferred states.

Evidence: `research/pagarme/lifecycle.md`, `research/pagbank/lifecycle.md`,
and the official PagBank QR creation reference:
https://developer.pagbank.com.br/reference/criar-pedido-pedido-com-qr-code
