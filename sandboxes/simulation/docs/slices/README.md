# Simulation Slices

Each slice extends the same shared simulation environment. A slice document
must state:

- selected implementation pack;
- runtime targets and architecture mode;
- discovery scope and evidence prerequisites;
- use-case contract and business rules;
- required ports;
- deterministic test and scenario plan;
- done criteria and explicit out-of-scope boundaries.

Candidate slices are hypotheses. Refinement may split, merge, reorder, add, or
remove them. After each build, record a lightweight refinement check and update
the semantic model and slice map where observations disprove assumptions.

Current lifecycle/event-delivery increments cover Pagar.me, Iugu, PagBank, and
Mercado Pago; each retains provider-specific transport and authenticity rules.
The current expiration increment covers Mercado Pago unpaid cancellation and
its two documented expiration outcomes; Pagar.me and PagBank expiration remain
out of scope pending evidence.
