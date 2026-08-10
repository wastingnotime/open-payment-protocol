# Simulation Tools

Repository-owned utilities may run or inspect the shared simulation. The common
WNT MRL Runtime remains local infrastructure, not an OPP production surface.

Validate every current provider scenario report with:

```bash
python3 sandboxes/simulation/tools/validate_scenarios.py
```

The validator checks report shape, observation envelopes, scenario attribution,
and absence of raw PAN, CVV, and `card_number` markers.
It also replays each provider registry and compares the serialized report
snapshot.
