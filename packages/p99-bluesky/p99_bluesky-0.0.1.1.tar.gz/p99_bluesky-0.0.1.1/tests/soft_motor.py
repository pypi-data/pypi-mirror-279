import asyncio
from collections.abc import Callable

from bluesky.protocols import Movable, Stoppable
from ophyd_async.core import (
    ConfigSignal,
    Device,
    HintedSignal,
    StandardReadable,
    WatchableAsyncStatus,
)
from ophyd_async.core.signal import AsyncStatus, SignalR, T, observe_value, wait_for_value
from ophyd_async.core.utils import (
    DEFAULT_TIMEOUT,
    CalculatableTimeout,
    CalculateTimeout,
    WatcherUpdate,
)
from ophyd_async.epics.signal import epics_signal_r, epics_signal_rw, epics_signal_x


class SoftThreeAxisStage(Device):
    """

    Standard ophyd_async xyz motor stage, by combining 3 Motors.

    Parameters
    ----------
    prefix:
        EPICS PV (None common part up to and including :).
    name:
        name for the stage.
    infix:
        EPICS PV, default is the ["X", "Y", "Z"].
    Notes
    -----
    Example usage::
        async with DeviceCollector():
            xyz_stage = ThreeAxisStage("BLXX-MO-STAGE-XX:")
    Or::
        with DeviceCollector():
            xyz_stage = ThreeAxisStage("BLXX-MO-STAGE-XX:", suffix = [".any",
              ".there", ".motorPv"])

    """

    def __init__(self, prefix: str, name: str, infix: list[str] | None = None):
        if infix is None:
            infix = ["X", "Y", "Z"]
        self.x = SoftMotor(prefix + infix[0])
        self.y = SoftMotor(prefix + infix[1])
        self.z = SoftMotor(prefix + infix[2])
        super().__init__(name=name)


class SoftMotor(StandardReadable, Movable, Stoppable):
    """Device that moves a motor record
    ToDo: this should not be needed,
    rather I should try change the record in the softioc to match motor
    """

    def __init__(self, prefix: str, name="") -> None:
        # Define some signals
        with self.add_children_as_readables(ConfigSignal):
            self.motor_egu = epics_signal_r(str, prefix + ".EGU")
            self.velocity = epics_signal_rw(float, prefix + "VELO")

        with self.add_children_as_readables(HintedSignal):
            self.user_readback = epics_signal_r(float, prefix + "RBV")

        self.user_setpoint = epics_signal_rw(float, prefix + "VAL")
        self.max_velocity = epics_signal_r(float, prefix + "VMAX")
        self.acceleration_time = epics_signal_rw(float, prefix + "ACCL")
        self.precision = epics_signal_r(int, prefix + ".PREC")
        self.deadband = epics_signal_r(float, prefix + "RDBD")
        self.motor_done_move = epics_signal_r(bool, prefix + "DMOV")
        self.low_limit_travel = epics_signal_rw(float, prefix + "LLM")
        self.high_limit_travel = epics_signal_rw(float, prefix + "HLM")

        self.motor_stop = epics_signal_x(prefix + "STOP")
        # Whether set() should complete successfully or not
        self._set_success = True
        super().__init__(name=name)

    def set_name(self, name: str):
        super().set_name(name)
        # Readback should be named the same as its parent in read()
        self.user_readback.set_name(name)

    @AsyncStatus.wrap
    async def wait_for_value_with_status(
        self,
        signal: SignalR[T],
        match: T | Callable[[T], bool],
        timeout: float | None,
    ):
        """wrap wait for value so it return an asyncStatus"""
        await wait_for_value(signal, match, timeout)

    @WatchableAsyncStatus.wrap
    async def set(self, value: float, timeout: CalculatableTimeout = CalculateTimeout):
        self._set_success = True
        (
            old_position,
            units,
            precision,
            velocity,
            acceleration_time,
        ) = await asyncio.gather(
            self.user_setpoint.get_value(),
            self.motor_egu.get_value(),
            self.precision.get_value(),
            self.velocity.get_value(),
            self.acceleration_time.get_value(),
        )
        if timeout is CalculateTimeout:
            assert velocity > 0, "Motor has zero velocity"
            timeout = (
                abs(value - old_position) / velocity
                + 2 * acceleration_time
                + DEFAULT_TIMEOUT
            )
        # modified to actually wait for set point to be set
        await self.user_setpoint.set(value, wait=True, timeout=timeout)
        # changed this so that the watcher keep going until the motor is stopped
        move_status = self.wait_for_value_with_status(
            self.motor_done_move, True, timeout=None
        )
        async for current_position in observe_value(
            self.user_readback, done_status=move_status
        ):
            yield WatcherUpdate(
                current=current_position,
                initial=old_position,
                target=value,
                name=self.name,
                unit=units,
                precision=precision,
            )
        if not self._set_success:
            raise RuntimeError("Motor was stopped")

    async def stop(self, success=False):
        self._set_success = success
        # Put with completion will never complete as we are waiting for completion on
        # the move above, so need to pass wait=False
        await self.motor_stop.trigger(wait=False)
        # Trigger any callbacks
        # await self.user_setpoint.set(await self.user_readback.get_value())
