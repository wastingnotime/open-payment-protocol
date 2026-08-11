# ngrok Documentation Source Record

- Provider: ngrok transport/inspection infrastructure
- Source type: official `llms.txt` documentation index
- Index: `https://ngrok.com/docs/llms.txt`
- Access date: 2026-08-11
- Use in OPP: temporary HTTPS delivery for local provider webhook receivers
- Not evidence of: provider event semantics, authenticity guarantees, retries,
  ordering, or production payment behavior

Relevant official guidance includes HTTP agent endpoints, Traffic Inspector,
webhook gateway patterns, and webhook verification traffic policies. OPP uses
ngrok only as a local test transport; provider-native headers and raw request
bytes remain the evidence inputs for each provider slice.
