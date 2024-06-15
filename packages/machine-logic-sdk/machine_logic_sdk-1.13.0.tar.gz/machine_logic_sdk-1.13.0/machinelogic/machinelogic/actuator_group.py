from typing import Tuple

from ..ivention.exception import ActuatorException, ActuatorGroupException
from ..ivention.iactuator_group import DEFAULT_MOVEMENT_TIMEOUT_SECONDS, IActuatorGroup
from ..ivention.util.inheritance import inherit_docstrings  # type: ignore
from .actuator import Actuator
from .api import Api


@inherit_docstrings
class ActuatorGroup(IActuatorGroup):
    def __init__(self, *axes: Actuator):
        super().__init__(*axes)
        self._api: Api = axes[0]._api  # pylint: disable=protected-access

    def move_absolute(
        self,
        position: Tuple[float, ...],
        timeout: float = DEFAULT_MOVEMENT_TIMEOUT_SECONDS,
    ) -> None:
        self._does_tuple_match_axes_length(position)

        move_to_position_payload = []
        for i in range(0, self._length):
            axis = self._actuators[i]
            axis_position = position[i]
            move_to_position_payload.append((axis.configuration.uuid, axis_position))

        if not self._api.move_to_position_combined(
            move_to_position_payload, True, timeout
        ):
            raise ActuatorGroupException("Unable to move_absolute on ActuatorGroup")

    def move_relative(
        self,
        distance: Tuple[float, ...],
        timeout: float = DEFAULT_MOVEMENT_TIMEOUT_SECONDS,
    ) -> None:
        self._does_tuple_match_axes_length(distance)

        move_relative_payload = []
        for i in range(0, self._length):
            axis = self._actuators[i]
            axis_distance = distance[i]
            move_relative_payload.append((axis.configuration.uuid, axis_distance))

        if not self._api.move_relative_combined(move_relative_payload, True, timeout):
            raise ActuatorGroupException("Unable to move_relative on ActuatorGroup")

    def move_absolute_async(self, position: Tuple[float, ...]) -> None:
        self._does_tuple_match_axes_length(position)

        move_to_position_payload = []
        for i in range(0, self._length):
            axis = self._actuators[i]
            axis_position = position[i]
            move_to_position_payload.append((axis.configuration.uuid, axis_position))

        if not self._api.move_to_position_combined(move_to_position_payload, False):
            raise ActuatorGroupException(
                "Unable to move_absolute_async on ActuatorGroup"
            )

    def move_relative_async(self, distance: Tuple[float, ...]) -> None:
        self._does_tuple_match_axes_length(distance)

        move_relative_payload = []
        for i in range(0, self._length):
            axis = self._actuators[i]
            axis_distance = distance[i]
            move_relative_payload.append((axis.configuration.uuid, axis_distance))

        if not self._api.move_relative_combined(move_relative_payload, False):
            raise ActuatorGroupException("Unable to move_relative on ActuatorGroup")

    def wait_for_move_completion(
        self, timeout: float = DEFAULT_MOVEMENT_TIMEOUT_SECONDS
    ) -> None:
        wait_for_move_completion_payload: list[str] = []

        for axis in self._actuators:
            wait_for_move_completion_payload.append(axis.configuration.uuid)
        if not self._api.wait_for_motion_completion(
            wait_for_move_completion_payload, timeout=timeout
        ):
            raise ActuatorGroupException("Failed to wait_for_move_completion")

    def lock_brakes(self) -> None:
        for axis in self._actuators:
            try:
                axis.lock_brakes()
            except ActuatorException as error:
                raise ActuatorGroupException(  # pylint: disable=raise-missing-from
                    f"Failed to lock brakes on axis with name {axis.configuration.name}: {str(error)}"
                )

    def unlock_brakes(self) -> None:
        for axis in self._actuators:
            try:
                axis.unlock_brakes()
            except ActuatorException as error:
                raise ActuatorGroupException(  # pylint: disable=raise-missing-from
                    f"Failed to unlock brakes on axis with name {axis.configuration.name}: {str(error)}"
                )

    def set_speed(self, speed: float) -> None:
        for actuator in self._actuators:
            try:
                actuator.set_speed(speed)
            except ActuatorException as error:
                raise ActuatorGroupException(  # pylint: disable=raise-missing-from
                    f"Failed to set speed on actuator with name {actuator.configuration.name}: {str(error)}"
                )

    def set_acceleration(self, acceleration: float) -> None:
        for actuator in self._actuators:
            try:
                actuator.set_acceleration(acceleration)
            except ActuatorException as error:
                raise ActuatorGroupException(  # pylint: disable=raise-missing-from
                    f"Failed to set acceleration on actuator with name {actuator.configuration.name}: {str(error)}"
                )

    def stop(self) -> None:
        actuator_uuids_to_stop = [
            actuator.configuration.uuid for actuator in self._actuators
        ]

        if not self._api.stop_motion_combined(actuator_uuids_to_stop):
            raise ActuatorGroupException("Unable to stop on ActuatorGroup")
