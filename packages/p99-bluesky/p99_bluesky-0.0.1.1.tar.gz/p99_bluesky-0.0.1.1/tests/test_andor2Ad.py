from collections import defaultdict
from pathlib import Path, PosixPath

import pytest
from bluesky import plan_stubs as bps
from bluesky import preprocessors as bpp
from bluesky.run_engine import RunEngine
from bluesky.utils import new_uid, short_uid
from ophyd_async.core import (
    DetectorTrigger,
    DeviceCollector,
    StaticDirectoryProvider,
    TriggerInfo,
    assert_emitted,
    set_mock_value,
)
from ophyd_async.core._providers import DirectoryInfo

from p99_bluesky.devices.andor2Ad import Andor2Ad, Andor3Ad, StaticDirectoryProviderPlus

CURRENT_DIRECTORY = "."  # str(Path(__file__).parent)


async def make_andor2(prefix: str = "") -> Andor2Ad:
    dp = StaticDirectoryProvider(CURRENT_DIRECTORY, f"test-{new_uid()}")

    async with DeviceCollector(mock=True):
        detector = Andor2Ad(prefix, dp, "andor2")
    return detector


async def make_andor3(prefix: str = "") -> Andor3Ad:
    dp = StaticDirectoryProvider(CURRENT_DIRECTORY, f"test-{new_uid()}")

    async with DeviceCollector(mock=True):
        andor3 = Andor3Ad(prefix, dp, "andor2")
    return andor3


def count_mock(det: Andor2Ad | Andor3Ad, times: int = 1):
    """Test plan to do the equivalent of bp.count for a mock detector."""

    yield from bps.stage_all(det)
    yield from bps.open_run()
    yield from bps.declare_stream(det, name="primary", collect=False)
    for _ in range(times):
        read_value = yield from bps.rd(det._writer.hdf.num_captured)
        yield from bps.trigger(det, wait=False, group="wait_for_trigger")

        yield from bps.sleep(0.001)
        set_mock_value(det._writer.hdf.num_captured, read_value + 1)

        yield from bps.wait(group="wait_for_trigger")
        yield from bps.create()
        yield from bps.read(det)
        yield from bps.save()

    yield from bps.close_run()
    yield from bps.unstage_all(det)


@pytest.fixture
async def andor2() -> Andor2Ad:
    andor2 = await make_andor2(prefix="TEST")

    set_mock_value(andor2._controller.driver.array_size_x, 10)
    set_mock_value(andor2._controller.driver.array_size_y, 20)
    set_mock_value(andor2.hdf.file_path_exists, True)
    set_mock_value(andor2._writer.hdf.num_captured, 0)
    return andor2


@pytest.fixture
async def andor3() -> Andor3Ad:
    andor3 = await make_andor3(prefix="TEST")

    set_mock_value(andor3._controller.driver.array_size_x, 10)
    set_mock_value(andor3._controller.driver.array_size_y, 20)
    set_mock_value(andor3.hdf.file_path_exists, True)
    set_mock_value(andor3._writer.hdf.num_captured, 0)
    return andor3


def takeImg(
    det: Andor2Ad | Andor3Ad,
    exposure: float,
    n_img: int,
    det_trig: DetectorTrigger,
):
    """Test plan to trigger the prepare part of the detect this is asynco/flyable."""
    grp = short_uid("prepare")
    tg = TriggerInfo(n_img, det_trig, exposure + 4, exposure)

    @bpp.stage_decorator([det])
    @bpp.run_decorator()
    def innerTakeImg():
        yield from bps.declare_stream(det, name="primary", collect=False)
        yield from bps.prepare(det, tg, group=grp, wait=True)
        yield from bps.kickoff(det, group=grp, wait=True)
        for n in range(1, n_img + 2):
            yield from bps.sleep(0.001)
            set_mock_value(det._writer.hdf.num_captured, n)
        yield from bps.complete(det, group=grp, wait=True)

    return (yield from innerTakeImg())


async def test_Andor(RE: RunEngine, andor2: Andor2Ad):
    docs = defaultdict(list)

    def capture_emitted(name, doc):
        docs[name].append(doc)

    RE.subscribe(capture_emitted)
    RE(count_mock(andor2))

    assert_emitted(
        docs, start=1, descriptor=1, stream_resource=2, stream_datum=2, event=1, stop=1
    )
    docs = defaultdict(list)
    RE(takeImg(andor2, 0.2, 2, det_trig=DetectorTrigger.internal))
    # since it is external stream nothing comes back here
    assert_emitted(docs, start=1, descriptor=1, stop=1)


async def test_Andor3(RE: RunEngine, andor3: Andor3Ad):
    docs = defaultdict(list)

    def capture_emitted(name, doc):
        docs[name].append(doc)

    RE.subscribe(capture_emitted)
    RE(count_mock(andor3))

    assert_emitted(
        docs, start=1, descriptor=1, stream_resource=2, stream_datum=2, event=1, stop=1
    )
    docs = defaultdict(list)
    RE(takeImg(andor3, 0.2, 2, det_trig=DetectorTrigger.internal))
    # since it is external stream nothing comes back here
    assert_emitted(docs, start=1, descriptor=1, stop=1)


@pytest.fixture
def mock_staticDP(
    dir: Path = Path("/what/dir/"), filename_prefix: str = "p99"
) -> StaticDirectoryProviderPlus:
    mock_staticDP = StaticDirectoryProviderPlus(dir, filename_prefix)
    return mock_staticDP


def test_StaticDirectoryProviderPlus():
    dir: Path = Path("/what/dir/")
    filename_prefix: str = "p99"
    mock_staticDP = StaticDirectoryProviderPlus(dir, filename_prefix)
    assert mock_staticDP.__call__() == DirectoryInfo(
        root=Path("/what/dir/"), resource_dir=PosixPath("."), prefix="p99", suffix="0"
    )

    assert mock_staticDP.__call__() == DirectoryInfo(
        root=Path("/what/dir/"), resource_dir=PosixPath("."), prefix="p99", suffix="1"
    )
