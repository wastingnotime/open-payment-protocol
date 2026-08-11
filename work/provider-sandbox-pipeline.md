# Provider Sandbox Validation Pipeline

Status: tracking document; no provider account or credential is recorded as
configured in this repository as of 2026-08-11.

This document tracks operational readiness for provider-sandbox observation. It
must never contain API keys, tokens, passwords, certificates, customer data, or
raw unsanitized provider payloads.

## State model

`not-started` means no account setup is recorded. `account-ready` means a test
account exists but credentials are not recorded here. `credentials-ready`
means credentials have been placed in an approved local secret store. `webhook-
ready` means the local receiver is reachable through a temporary HTTPS endpoint.
`observed` means a sanitized run receipt exists under `runs/` and the relevant
research claim is labeled `Sandbox-observed`.

## Provider readiness matrix

| Provider | Test account prerequisite | Credential prerequisite | Webhook prerequisite | Current state | First target |
| --- | --- | --- | --- | --- | --- |
| Asaas | Separate account at `sandbox.asaas.com` | Sandbox API key and Sandbox API URL | Public HTTPS callback; configure Sandbox webhook | `not-started` | Pix payment transition and `PAYMENT_RECEIVED` flow |
| Iugu | Iugu account with test mode | Test API token; token creation may require account-admin approval | Public HTTPS callback for trigger delivery | `not-started` | Invoice/Pix lifecycle and webhook event delivery |
| Mercado Pago | Developer account and application; seller/buyer test users for end-to-end flow | Test Public Key and Access Token | Public HTTPS callback and notification configuration | `not-started` | Pix `action_required` to automatic approval/finalization |
| Pagar.me | Pagar.me account with test mode/simulator enabled | Test API key, commonly `sk_test_*` | Public HTTPS callback for webhook events | `not-started` | Pix success/failure simulator, then refund/expiration evidence |
| PagBank | PagBank account; Sandbox account is assigned during setup | Sandbox token from Developer Portal; extra mTLS/Connect steps only for applicable APIs | Public HTTPS callback and notification configuration | `not-started` | QR order, charge emergence, cancellation, and notification |

## Execution pipeline

1. Create or confirm the provider test account.
2. Obtain test credentials and store them only in the approved local secret
   store. Record provider, credential type, environment, creation date, and a
   non-secret identifier or masked suffix here if useful.
3. Start a local receiver with a deterministic scenario correlation ID.
4. Expose only the receiver through an HTTPS ngrok endpoint. The basic local
   shape is `ngrok http <local-port>`; do not put the auth token or public URL
   in committed fixtures.
5. Configure the provider's Sandbox webhook URL and authenticity settings.
6. Execute one provider-native scenario at a time. Preserve raw bytes and
   headers only in a protected local run area until sanitized.
7. Sanitize the observation: remove credentials, personal data, cardholder
   data, QR secrets, and unnecessary identifiers; retain status, event name,
   ordering, delivery attempt, response code, and provider resource shape.
8. Store the sanitized receipt under `runs/<provider>/<date>-<scenario>/` and
   update the relevant `research/` claim from `Documented` to
   `Sandbox-observed` only when the observation directly supports it.
9. Run the deterministic simulation and record the refinement check in
   `work/changes/<slice>/`.

## ngrok boundary

ngrok is transport and inspection infrastructure, not payment-provider
evidence. Use its official documentation index at
`https://ngrok.com/docs/llms.txt`; the HTTP agent endpoint and Traffic
Inspector are useful for local webhook delivery and troubleshooting. The
provider remains responsible for webhook authenticity and the repository must
retain the provider-native headers/body needed to evaluate that behavior.

Do not use a public tunnel as an authorization boundary. Keep the receiver
minimal, reject unexpected methods or paths, avoid logging secrets, and close
the endpoint after the test session.

## Evidence and completion rules

- Documentation alone remains `Documented`.
- A reproducible Sandbox response or webhook receipt becomes
  `Sandbox-observed`.
- A behavior inferred from several observations remains `Inferred` until the
  provider guarantees it.
- A missing or contradictory result remains `Unknown`.
- A sandbox result must not be generalized to production without provider
  evidence.
- No slice is marked complete from account setup alone.

## Source entrypoints

- Asaas: `https://docs.asaas.com/mcp`
- Iugu: `https://dev.iugu.com/mcp` and `https://dev.iugu.com/llms.txt`
- Mercado Pago: `https://www.mercadopago.com.br/developers/en/docs/llms.txt`
- Pagar.me: `https://docs.pagar.me/llms.txt`
- PagBank: `https://developer.pagbank.com.br/llms.txt`
- ngrok: `https://ngrok.com/docs/llms.txt`
