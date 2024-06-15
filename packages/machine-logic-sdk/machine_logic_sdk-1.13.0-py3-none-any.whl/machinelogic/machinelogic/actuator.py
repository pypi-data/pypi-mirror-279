# pylint: disable=protected-access
from typing import Optional

from ..ivention.exception import ActuatorException
from ..ivention.iactuator import (
    DEFAULT_MOVEMENT_TIMEOUT_SECONDS,
    ActuatorConfiguration,
    ActuatorState,
    IActuator,
)
from ..ivention.util.inheritance import inherit_docstrings  # type: ignore
from .api import Api, BrakeState

# TODO: One day, we will have high-speed streams in the execution
# engine, and then we can just update the ModifiedAxisState without
# a worry in the world, a cold beer in our hands.

# We purposefully override the traditional ActuatorState while we do
# not yet have access to the "high-powered streams" that Doug knows
# and loves


@inherit_docstrings
class ModifiedActuatorState(ActuatorState):
    def __init__(self, configuration: ActuatorConfiguration, api: Api):
        super().__init__()
        self._configuration = configuration
        self._api = api

    @property
    def speed(self) -> float:
        return self._api.get_speed(self._configuration.uuid)

    @property
    def position(self) -> float:
        return self._api.get_axis_position(self._configuration.uuid)

    @property
    def brakes(self) -> float:
        brake_state = self._api.get_brake_state(self._configuration.uuid)
        if brake_state == BrakeState.LOCKED:
            return 1

        return 0

    def _sync_move_in_progress(self) -> None:
        # get updated values after starting moves.
        self._move_in_progress = not self._api.get_axis_motion_completion(
            self._configuration.uuid
        )

    @property
    def output_torque(self) -> dict[str, float]:
        return self._api.get_axis_actual_torque(self._configuration.uuid)


@inherit_docstrings
class Actuator(IActuator):
    """Representation of a Vention Actuator"""

    def __init__(self, configuration: ActuatorConfiguration, api: Api):
        super().__init__(configuration)
        self._api = api
        self._state: ModifiedActuatorState = ModifiedActuatorState(configuration, api)

    def move_relative(
        self, distance: float, timeout: float = DEFAULT_MOVEMENT_TIMEOUT_SECONDS
    ) -> None:
        if not self._api.move_relative(
            self.configuration.uuid, distance, True, timeout
        ):
            raise ActuatorException(
                f"Failed to move_relative on actuator with name {self.configuration.name} by a distance of {distance}"
            )
        self._state._sync_move_in_progress()

    def move_relative_async(self, distance: float) -> None:
        if not self._api.move_relative(self.configuration.uuid, distance, False):
            raise ActuatorException(
                f"Failed to move_relative_async on actuator with name {self.configuration.name} by a distance of {distance}"
            )
        self._state._sync_move_in_progress()

    def move_absolute(
        self, position: float, timeout: float = DEFAULT_MOVEMENT_TIMEOUT_SECONDS
    ) -> None:
        if not self._api.move_absolute(
            self.configuration.uuid, position, True, timeout
        ):
            raise ActuatorException(
                f"Failed to move_absolute on actuator with name {self.configuration.name} to position {position}"
            )
        self._state._sync_move_in_progress()

    def move_absolute_async(self, position: float) -> None:
        if not self._api.move_absolute(self.configuration.uuid, position, False):
            raise ActuatorException(
                f"Failed to move_absolute_async on actuator with name {self.configuration.name} to position {position}"
            )
        self._state._sync_move_in_progress()

    def move_continuous_async(
        self,
        speed: float = 100.0,
        acceleration: float = 100.0,
    ) -> None:
        if not self._api.set_continuous_move(
            self.configuration.uuid, False, speed, acceleration
        ):
            raise ActuatorException(
                f"Failed to start_continuous_move on actuator with name {self.configuration.name}"
            )
        self._state._sync_move_in_progress()

    def wait_for_move_completion(
        self, timeout: float = DEFAULT_MOVEMENT_TIMEOUT_SECONDS
    ) -> None:
        if not self._api.wait_for_motion_completion(
            self.configuration.uuid, timeout=timeout
        ):
            raise ActuatorException(
                f"Failed to wait_for_move_completion on actuator with name {self.configuration.name}"
            )

    def home(self, timeout: float = DEFAULT_MOVEMENT_TIMEOUT_SECONDS) -> None:
        if not self._api.home(self.configuration.uuid, True, timeout):
            raise ActuatorException(
                f"Failed to home on actuator with name {self.configuration.name}"
            )

    def set_speed(self, speed: float) -> None:
        if not self._api.set_speed(self.configuration.uuid, speed):
            raise ActuatorException(
                f"Failed to set_speed on actuator with name {self.configuration.name}"
            )

    def set_acceleration(self, acceleration: float) -> None:
        if not self._api.set_acceleration(self.configuration.uuid, acceleration):
            raise ActuatorException(
                f"Failed to set_acceleration on actuator with name {self.configuration.name}"
            )

    def lock_brakes(self) -> None:
        if not self._api.lock_brakes(self.configuration.uuid):
            raise ActuatorException(
                f"Failed to lock on actuator with name {self.configuration.name}"
            )

    def unlock_brakes(self) -> None:
        if not self._api.unlock_brakes(self.configuration.uuid):
            raise ActuatorException(
                f"Failed to lock on actuator with name {self.configuration.name}"
            )

    def stop(self, acceleration: Optional[float] = None) -> None:
        if acceleration is None:
            was_motion_stopped = self._api.stop_motion(self.configuration.uuid)
        else:
            was_motion_stopped = self._api.stop_continuous_move(
                self.configuration.uuid, acceleration
            )

        if not was_motion_stopped:
            raise ActuatorException(
                f"Failed to stop on actuator with name {self.configuration.name}"
            )
