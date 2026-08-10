# Shared Contract Helper Refinement

The test suite and standalone validator currently duplicate report-contract
constants and serialization logic. The next build moves those rules into one
simulation helper while retaining the typed Iugu report compatibility.
The helper's public contract includes report field access, allowed sources,
provider prefixes, and canonical snapshots.
It also owns the expected current scenario counts used by both validation
paths.
Per-report validation remains limited to the shared envelope, attribution, and
prefix rules; provider payload semantics stay outside the helper.
Validation failures should identify the provider and scenario so local
receipts are actionable without debugging the runner registry first.
The helper remains an experimental internal simulation surface, not protocol
authority.
Provider runner registration is kept in a neighboring simulation registry so
tools do not maintain separate provider lists.
Its order follows the repository comparison sequence: Asaas, Iugu, Mercado
Pago, Pagar.me, and PagBank.
