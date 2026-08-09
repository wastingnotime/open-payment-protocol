"""WNT MRL Runtime boundary for the repository simulation.

The pure simulation is importable without the optional runtime package. The
factory deliberately fails with an actionable message when the local WNT MRL
Runtime is not installed, instead of shipping a second incompatible runtime.
"""

from __future__ import annotations

from .scenarios import run_all


def create_simulation():
    try:
        from mrl_simulation_runtime.scenario import Scenario
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Install the WNT MRL Runtime before supervision: "
            "wnt install --target mrl_runtime_user --target mrl_user_bin --user --force"
        ) from exc

    results = run_all()
    observations = []
    for result in results.values():
        observations.extend(result.observations)
    try:
        return Scenario(
            name="opp-iugu-pix",
            run_id="iugu-pix-first-slice",
            seed=1,
            observations=observations,
        )
    except TypeError as exc:
        raise RuntimeError(
            "The installed MRL Runtime Scenario constructor differs from this adapter; "
            "inspect the local runtime contract before supervision."
        ) from exc
