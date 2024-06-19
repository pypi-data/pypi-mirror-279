import pytest
from ophyd_async.core import DeviceCollector

from p99_bluesky.devices.stages import ThreeAxisStage


@pytest.fixture
async def mock_three_axis_motor():
    async with DeviceCollector(mock=True):
        mock_three_axis_motor = ThreeAxisStage("BLxx-MO-xx-01:", "mock_three_axis_motor")
        # Signals connected here

    yield mock_three_axis_motor


async def test_there_axis_motor(mock_three_axis_motor: ThreeAxisStage) -> None:
    assert mock_three_axis_motor.name == "mock_three_axis_motor"
    assert mock_three_axis_motor.x.name == "mock_three_axis_motor-x"
    assert mock_three_axis_motor.y.name == "mock_three_axis_motor-y"
    assert mock_three_axis_motor.z.name == "mock_three_axis_motor-z"


"""
import asyncio
import subprocess


async def test_nothing():
    p = subprocess.Popen(
        [
            "python",
            "/workspaces/p99-bluesky/tests/epics/softioc/softsignal.py",
            "p99-motor",
            "AI",
            "AO",
        ],
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )

    # async with DeviceCollector():
    sig = epics_signal_rw(float, "p99-motor:AI")
    sig2 = epics_signal_rw(float, "p99-motor:AO")
    await asyncio.create_task(sig.connect())
    await asyncio.create_task(sig2.connect())
    await asyncio.gather(sig2.set(2))
        for i in range(20):
        result = asyncio.create_task(sig.get_value())
        await asyncio.wait_for(result, timeout=2)
        await asyncio.sleep(0.2)
        print(result)
    result = asyncio.create_task(sig.get_value())
    await asyncio.wait_for(result, timeout=2)
    # await asyncio.sleep(0.2)
    assert result.result() == pytest.approx(2.0, 0.1)
    p.communicate(b"exit")
"""
