# pylint: disable=duplicate-code
from abc import ABC, abstractmethod
from typing import Literal

BagGripperState = Literal["open", "closed", "transition", "unknown"]


class BagGripperConfiguration:
    """Representation of a Bag gripper configuration."""

    def __init__(
        self,
        uuid: str,
        name: str,
        controller_id: str,
        ip_address: str,
        device: int,
        output_pin_close: int,
        output_pin_open: int,
        input_pin_close: int,
        input_pin_open: int,
    ) -> None:
        self._uuid: str = uuid
        self._name: str = name
        self._controller_id: str = controller_id
        self._ip_address: str = ip_address
        self._device: int = device
        self._output_pin_close: int = output_pin_close
        self._output_pin_open: int = output_pin_open
        self._input_pin_close: int = input_pin_close
        self._input_pin_open: int = input_pin_open

    @property
    def uuid(self) -> str:
        """str: The ID of the Bag gripper."""
        return self._uuid

    @property
    def name(self) -> str:
        """str: The name of the Bag gripper."""
        return self._name

    @property
    def ip_address(self) -> str:
        """str: The IP address of the Bag gripper."""
        return self._ip_address

    @property
    def device(self) -> int:
        """int: The device of the Bag gripper."""
        return self._device

    @property
    def output_pin_close(self) -> int:
        """int: The close out pin of the Bag gripper."""
        return self._output_pin_close

    @property
    def output_pin_open(self) -> int:
        """int: The open out pin of the Bag gripper."""
        return self._output_pin_open

    @property
    def input_pin_close(self) -> int:
        """int: The close in pin of the Bag gripper."""
        return self._input_pin_close

    @property
    def input_pin_open(self) -> int:
        """int: The open in pin of the Bag gripper."""
        return self._input_pin_open


class IBagGripper(ABC):
    """
    A software representation of a Bag Gripper. It is not recommended that you
    construct this object yourself. Rather, you should query it from a Machine instance:

    E.g.:
        machine = Machine()
        my_bag_gripper = machine.get_bag_gripper("Bag Gripper")

    In this example, "Bag Gripper" is the friendly name assigned to a Bag Gripper in the
    MachineLogic configuration page.
    """

    def __init__(self, configuration: BagGripperConfiguration) -> None:
        """
        Args:
            configuration (PneumaticConfiguration): Configuration of the Pneumatic.
        """
        self._state: BagGripperState = "unknown"
        self._configuration = configuration

    @property
    def state(self) -> BagGripperState:
        """
        BagGripperState: The state of the actuator.
        """
        return self._state

    @property
    def configuration(self) -> BagGripperConfiguration:
        """
        BagGripperConfiguration: The configuration of the actuator.
        """
        return self._configuration

    @abstractmethod
    def open_async(self) -> None:
        """
        Opens the Bag Gripper.

        Raises:
            BagGripperException: If the Bag Gripper fails to open.
        """

    @abstractmethod
    def close_async(self) -> None:
        """
        Closes the Bag Gripper.

        Raises:
            BagGripperException: If the Bag Gripper fails to close.
        """
