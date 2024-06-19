import asyncio
import subprocess

from bluesky.run_engine import RunEngine
from ophyd_async.core import DeviceCollector

from p99_bluesky.devices.p99.sample_stage import (
    FilterMotor,
    SampleAngleStage,
    p99StageSelections,
)
from soft_motor import SoftThreeAxisStage

# Long enough for multiple asyncio event loop cycles to run so
# all the tasks have a chance to run
A_BIT = 0.001


async def test_soft_sampleAngleStage(RE: RunEngine) -> None:
    p = subprocess.Popen(
        [
            "python",
            "tests/epics/soft_ioc/p99_softioc.py",
        ],
    )

    await asyncio.sleep(A_BIT)
    with DeviceCollector(mock=False):
        mock_sampleAngleStage = SampleAngleStage(
            "p99-MO-TABLE-01:", name="mock_sampleAngleStage"
        )
        mock_filter_wheel = FilterMotor(
            "p99-MO-STAGE-02:MP:SELECT", name="mock_filter_wheel"
        )
        xyz_motor = SoftThreeAxisStage("p99-MO-STAGE-02:", name="xyz_motor")

    assert mock_sampleAngleStage.roll.name == "mock_sampleAngleStage-roll"
    assert mock_sampleAngleStage.pitch.name == "mock_sampleAngleStage-pitch"
    assert mock_filter_wheel.user_setpoint.name == "mock_filter_wheel-user_setpoint"

    await asyncio.gather(
        mock_sampleAngleStage.theta.set(2),
        mock_sampleAngleStage.pitch.set(3.1),
        mock_sampleAngleStage.roll.set(4),
        mock_filter_wheel.user_setpoint.set(p99StageSelections.Cd25um),
        xyz_motor.x.user_setpoint.set(0),
    )
    await asyncio.sleep(A_BIT)
    result = asyncio.gather(
        mock_sampleAngleStage.theta.get_value(),
        mock_sampleAngleStage.pitch.get_value(),
        mock_sampleAngleStage.roll.get_value(),
        mock_filter_wheel.user_setpoint.get_value(),
        xyz_motor.x.user_readback.get_value(),
    )
    await asyncio.wait_for(result, timeout=2)
    assert result.result() == [2.0, 3.1, 4.0, p99StageSelections.Cd25um, 0.0]
    from bluesky.plans import scan
    from ophyd.sim import det  # type: ignore

    RE(scan([mock_sampleAngleStage.theta, det], xyz_motor.y, -1, 1, 10))

    p.terminate()
    p.wait()
