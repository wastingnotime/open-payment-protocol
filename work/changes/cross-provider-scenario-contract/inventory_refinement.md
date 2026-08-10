# Scenario Inventory Refinement

The cross-provider report contract currently covers 50 executable scenarios:
8 Asaas, 13 Iugu, 10 Mercado Pago, 9 Pagar.me, and 10 PagBank. The build adds
explicit per-provider and aggregate assertions so inventory drift is visible
in validation. Scenario IDs must also retain their provider prefixes (`AS`,
`IUGU`, `MP`, `PG`, and `PB`).
