"""_summary_
"""
from abc import ABC, abstractmethod
from typing import Callable, Literal, Optional, Tuple

from .types.actuator_details import ActuatorType

DEFAULT_MOVEMENT_TIMEOUT_SECONDS = 300


class ActuatorState:
    """
    Representation of the current state of an Actuator instance. The values
    in this class are updated in real time to match the physical reality
    of the Actuator.
    """

    def __init__(self) -> None:
        self._position: float = 0
        self._speed: float = 0
        self._desired_position: float = 0
        self._desired_speed: float = 0
        self._output_torque: dict[str, float] = {}
        self._brakes: float = 0
        self._end_sensors: Tuple[bool, bool] = (False, False)
        self._move_in_progress: bool = False

    @property
    def position(self) -> float:
        """float: The current position of the Actuator."""
        return self._position

    @property
    def speed(self) -> float:
        """float: The current speed of the Actuator."""
        return self._speed

    @property
    def output_torque(self) -> dict[str, float]:
        """dict[str, float]: The current torque output of the Actuator."""
        return self._output_torque

    @property
    def brakes(self) -> float:
        """float: The current state of the brakes of the Actuator. Set to 1 if locked, otherwise 0."""
        return self._brakes

    @property
    def end_sensors(self) -> Tuple[bool, bool]:
        """Tuple[bool, bool]: A tuple representing the state of the [ home, end ] sensors."""
        return self._end_sensors

    @property
    def move_in_progress(self) -> bool:
        """bool: The boolean is True if a move is in progress, otherwise False."""
        return self._move_in_progress


class ActuatorConfiguration:
    """
    Representation of the configuration of an Actuator instance.
    This configuration defines what your Actuator is and how it
    should behave when work is requested from it.
    """

    def __init__(
        self,
        uuid: str,
        name: str,
        ip_address: str,
        actuator_type: ActuatorType,
        home_sensor: Literal["A", "B"],
        units: Literal["mm", "deg"],
        brake_present: bool,
        controller_id: str,
    ) -> None:
        self._uuid: str = uuid
        self._name: str = name
        self._ip_address: str = ip_address
        self._actuator_type: ActuatorType = actuator_type
        self._units: Literal["mm", "deg"] = units
        self._home_sensor: Literal["A", "B"] = home_sensor
        self._brake_present: bool = brake_present
        self._controller_id: str = controller_id
        self.sensor_event_listener: Optional[Callable[[Tuple[bool, bool]], None]] = None
        self.drive_error_event_listener: Optional[Callable[[int, str], None]] = None

    @property
    def uuid(self) -> str:
        """str: The Actuator's ID."""
        return self._uuid

    @property
    def actuator_type(self) -> ActuatorType:
        """ActuatorType: The type of the Actuator."""
        return self._actuator_type

    @property
    def name(self) -> str:
        """str: The name of the Actuator."""
        return self._name

    @property
    def ip_address(self) -> str:
        """str: The IP address of the Actuator."""
        return self._ip_address

    @property
    def home_sensor(self) -> Literal["A", "B"]:
        """Literal["A", "B"]: The home sensor port, either A or B."""
        return self._home_sensor

    @property
    def units(self) -> Literal["deg", "mm"]:
        """Literal["deg", "mm"]: The units that the Actuator functions in."""
        return self._units

    @property
    def controller_id(self) -> str:
        """str: The controller id of the Actuator"""
        return self._controller_id


class IActuator(ABC):
    """
    A software representation of an Actuator. An Actuator is defined as a motorized
    axis that can move by discrete distances. It is not recommended that you
    construct this object yourself. Rather, you should query it from a Machine instance:

    E.g.:
        machine = Machine()
        my_actuator = machine.get_actuator("Actuator")

    In this example, "New actuator" is the friendly name assigned to the Actuator in the
    MachineLogic configuration page.
    """

    def __init__(self, configuration: ActuatorConfiguration) -> None:
        """
        Args:
            configuration (ActuatorConfiguration): Configuration for this Actuator.
        """
        self._state = ActuatorState()
        self._configuration = configuration

    @property
    def state(self) -> ActuatorState:
        """ActuatorState: The representation of the current state of this MachineMotion."""
        return self._state

    @property
    def configuration(self) -> ActuatorConfiguration:
        """ActuatorConfiguration: The representation of the configuration associated with this MachineMotion."""
        return self._configuration

    @abstractmethod
    def move_relative(
        self, distance: float, timeout: float = DEFAULT_MOVEMENT_TIMEOUT_SECONDS
    ) -> None:
        """
        Moves relative synchronously by the specified distance.

        Args:
            distance (float): The distance to move.
            timeout (float): The timeout in seconds.
        Raises:
            ActuatorException: If the move was unsuccessful.
        """

    @abstractmethod
    def move_relative_async(self, distance: float) -> None:
        """
        Moves relative asynchronously by the specified distance.

        Args:
            distance (float): The distance to move.

        Raises:
            ActuatorException: If the move was unsuccessful.
        """

    @abstractmethod
    def move_absolute(
        self, position: float, timeout: float = DEFAULT_MOVEMENT_TIMEOUT_SECONDS
    ) -> None:
        """
        Moves absolute synchronously to the specified position.

        Args:
            position (float): The position to move to.
            timeout (float): The timeout in seconds.

        Raises:
            ActuatorException: If the move was unsuccessful.
        """

    @abstractmethod
    def move_absolute_async(self, position: float) -> None:
        """
        Moves absolute asynchronously.

        Args:
            position (float): The position to move to.

        Raises:
            ActuatorException: If the move was unsuccessful.
        """

    @abstractmethod
    def move_continuous_async(
        self,
        speed: float = 100.0,
        acceleration: float = 100.0,
    ) -> None:
        """
        Starts a continuous move. The Actuator will keep moving until it is stopped.

        Args:
            speed (float, optional): The speed to move with. Defaults to 100.0.
            acceleration (float, optional): The acceleration to move with. Defaults to 100.0.

        Raises:
            ActuatorException: If the move was unsuccessful.
        """

    @abstractmethod
    def wait_for_move_completion(
        self, timeout: float = DEFAULT_MOVEMENT_TIMEOUT_SECONDS
    ) -> None:
        """
        Waits for motion to complete before commencing the next action.

        Args:
            timeout (float): The timeout in seconds, after which an exception will be thrown.

        Raises:
            ActuatorException: If the request fails or the move did not complete in the allocated amount of time.
        """

    @abstractmethod
    def home(self, timeout: float = DEFAULT_MOVEMENT_TIMEOUT_SECONDS) -> None:
        """
        Home the Actuator synchronously.

        Args:
            timeout (float): The timeout in seconds.

        Raises:
            ActuatorException: If the home was unsuccessful or request timed out.
        """

    @abstractmethod
    def set_speed(self, speed: float) -> None:
        """
        Sets the max speed for the Actuator.

        Args:
            speed (float): The new speed.

        Raises:
            ActuatorException: If the request was unsuccessful.
        """

    @abstractmethod
    def set_acceleration(self, acceleration: float) -> None:
        """
        Sets the max acceleration for the Actuator.

        Args:
            acceleration (float): The new acceleration.

        Raises:
            ActuatorException: If the request was unsuccessful.
        """

    @abstractmethod
    def lock_brakes(self) -> None:
        """
        Locks the brakes on this Actuator.

        Raises:
            ActuatorException: If the brakes failed to lock.
        """

    @abstractmethod
    def unlock_brakes(self) -> None:
        """
        Unlocks the brakes on this Actuator.

        Raises:
            ActuatorException: If the brakes failed to unlock.
        """

    @abstractmethod
    def stop(self, acceleration: Optional[float] = None) -> None:
        """
        Stops movement on this Actuator. If no argument is provided, then a quickstop is emitted which will
        abruptly stop the motion. Otherwise, the actuator will decelerate following the provided acceleration.

        Args:
            acceleration (float, optional): Deceleration speed.

        Raises:
            ActuatorException: If the Actuator failed to stop.
        """
