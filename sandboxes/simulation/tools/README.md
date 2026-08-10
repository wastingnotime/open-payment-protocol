# Simulation Tools

Repository-owned utilities may run or inspect the shared simulation. The common
WNT MRL Runtime remains local infrastructure, not an OPP production surface.

Validate every current provider scenario report with:

```bash
python3 sandboxes/simulation/tools/validate_scenarios.py
```

The validator checks report shape, observation envelopes, scenario attribution,
and absence of raw PAN, CVV, `card_number`, `api_key`, `access_token`, and
`secret_key` markers.
It also replays each provider registry and compares the serialized report
snapshot.
The only framework-level source exception is Iugu's `simulation` replay
observation.
Provider registration is shared with the deterministic test suite.
