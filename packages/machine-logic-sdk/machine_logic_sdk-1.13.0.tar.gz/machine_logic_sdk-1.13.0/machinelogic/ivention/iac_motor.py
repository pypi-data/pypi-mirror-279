from abc import ABC, abstractmethod


class ACMotorConfiguration:
    """Representation of a ACMotor configuration."""

    def __init__(
        self,
        uuid: str,
        name: str,
        ip_address: str,
        device: int,
        output_pin_direction: int,
        output_pin_move: int,
    ) -> None:
        self._uuid: str = uuid
        self._name: str = name
        self._ip_address: str = ip_address
        self._device: int = device
        self._output_pin_direction: int = output_pin_direction
        self._output_pin_move: int = output_pin_move

    @property
    def uuid(self) -> str:
        """str: The ID of the Pneumatic."""
        return self._uuid

    @property
    def name(self) -> str:
        """str: The name of the Pneumatic."""
        return self._name

    @property
    def ip_address(self) -> str:
        """str: The IP address of the axis."""
        return self._ip_address

    @property
    def device(self) -> int:
        """int: The device of the axis."""
        return self._device

    @property
    def output_pin_direction(self) -> int:
        """int: The push out pin of the axis."""
        return self._output_pin_direction

    @property
    def output_pin_move(self) -> int:
        """int: The pull out pin of the axis."""
        return self._output_pin_move


class IACMotor(ABC):
    """
    A software representation of an AC Motor. It is not recommended that you
    construct this object yourself. Rather, you should query it from a Machine instance:

    E.g.:
        machine = Machine()
        my_ac_motor = machine.get_ac_motor("AC Motor")

    In this example, "AC Motor" is the friendly name assigned to an AC Motor in the
    MachineLogic configuration page.
    """

    def __init__(self, configuration: ACMotorConfiguration) -> None:
        """
        Args:
            configuration (ACMotorConfiguration): Configuration of the AC Motor.
        """
        self._configuration = configuration

    @property
    def configuration(self) -> ACMotorConfiguration:
        """
        ACMotorConfiguration: The configuration of the ACMotor.
        """
        return self._configuration

    @abstractmethod
    def move_forward(self) -> None:
        """
        Begins moving the AC Motor forward.

        Raises:
            ACMotorException: If the move was unsuccessful.
        """

    @abstractmethod
    def move_reverse(self) -> None:
        """
        Begins moving the AC Motor in reverse.

        Raises:
            ACMotorException: If the move was unsuccessful.
        """

    @abstractmethod
    def stop(self) -> None:
        """
        Stops the movement of the AC Motor.

        Raises:
            ACMotorException: If the stop was unsuccessful.
        """
