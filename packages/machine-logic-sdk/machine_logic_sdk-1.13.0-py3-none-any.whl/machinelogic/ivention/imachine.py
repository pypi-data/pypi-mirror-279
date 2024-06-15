"""_summary_"""
from abc import ABC
from typing import Callable, Optional, Union
from uuid import UUID

from ..decorators.future_api import future_api
from .exception import MachineException, MachineMotionException
from .iac_motor import IACMotor
from .iactuator import IActuator
from .ibag_gripper import IBagGripper
from .icamera import ICamera
from .idigital_input import IDigitalInput
from .idigital_output import IDigitalOutput
from .iestop import EstopEventCallback, IEstop
from .imachine_motion import IMachineMotion
from .ipneumatic import IPneumatic
from .irobot import IRobot
from .mqtt_client import MqttClient


class IMachine(ABC):
    """
    A software representation of the entire Machine. A Machine is defined as any number of
    MachineMotions, each containing their own set of axes, outputs, inputs, pneumatics,
    bag grippers, and AC Motors. The Machine class offers a global way to retrieve these
    various components using the friendly names that you've defined in your MachineLogic
    configuration.

    To create a new Machine with default settings, you can simply write:
        machine = Machine()
    
    If you need to connect to services running on a different machine or IP address, 
    you can specify the IP address as follows:
        machine = Machine("192.168.7.2")
    
    You should only ever have a single instance of this object in your program.
    """

    def __init__(
        self,
        machine_motions: list[IMachineMotion],
        mqtt_client: MqttClient,
        estop: IEstop,
    ) -> None:
        """
        Args:
            machine_motions (list[IMachineMotion]): The list of MachineMotions.
            mqtt_client (MqttClient): The Mqtt client.
            estop (IEstop): The Estop module.
        """
        self._machine_motions = machine_motions
        self._mqtt_client = mqtt_client
        self._estop = estop

    def get_machine_motion(self, name: str) -> IMachineMotion:
        """
        Retrieves an IMachineMotion instance by name.

        Args:
            name (str): The name of the MachineMotion.

        Returns:
            IMachineMotion: The MachineMotion that was found.

        Raises:
            MachineException: If we cannot find the MachineMotion.
        """
        for machine_motion in self._machine_motions:
            if machine_motion.configuration.name == name:
                return machine_motion

        raise MachineException(f"Unable to find MachineMotion with name: {name}")

    def get_actuator(self, name: str) -> IActuator:
        """
        Retrieves an Actuator by name.

        Args:
            name (str): The name of the Actuator.

        Returns:
            IActuator: The Actuator that was found.

        Raises:
            MachineException: If we cannot find the Actuator.
        """
        for machine_motion in self._machine_motions:
            try:
                return machine_motion.get_actuator(name)
            except MachineMotionException:
                pass

        raise MachineException(f"Unable to find actuator with name: {name}")

    @future_api
    def get_camera(self) -> ICamera:
        """
        Retrieves a Camera by name. If no name is specified, then returns the first Camera.

        Args:
            name (str): The Camera name. If it's `None`, then the first Camera in the Camera list is returned.

        Returns:
            ICamera: The Camera requested or the one that was found.

        Raises:
            MachineException: If the Camera is not found.
        """
        if len(self._machine_motions) == 0:
            raise MachineException("No machine motion found")

        camera = None
        for machine_motion in self._machine_motions:
            try:
                camera = machine_motion.get_camera()
            except MachineMotionException:
                pass

        if camera:
            return camera
        raise MachineException("Unable to find the camera")

    def get_robot(self, name: Union[str, None] = None) -> IRobot:
        """
        Retrieves a Robot by name. If no name is specified, then returns the first Robot.

        Args:
            name (str): The Robot name. If it's `None`, then the first Robot in the Robot list is returned.

        Returns:
            IRobot: The Robot that was found.

        Raises:
            MachineException: If the Robot is not found.
        """
        if len(self._machine_motions) == 0:
            raise MachineException("No robots found")

        robot = None
        for machine_motion in self._machine_motions:
            try:
                robot = machine_motion.get_robot(name)
            except MachineMotionException:
                pass

        if robot:
            return robot
        raise MachineException(f"Unable to find robot with name: {name}")

    def get_input(self, name: str) -> IDigitalInput:
        """
        Retrieves an DigitalInput by name.

        Args:
            name (str): The name of the DigitalInput.

        Returns:
            IDigitalInput: The DigitalInput that was found.

        Raises:
            MachineException: If we cannot find the DigitalInput.
        """
        for machine_motion in self._machine_motions:
            try:
                return machine_motion.get_input(name)
            except MachineMotionException:
                pass

        raise MachineException(f"Unable to find input with name: {name}")

    def get_output(self, name: str) -> IDigitalOutput:
        """
        Retrieves an Output by name.

        Args:
            name (str): The name of the Output

        Returns:
            IOutput: The Output that was found.

        Raises:
            MachineException: If we cannot find the Output.
        """
        for machine_motion in self._machine_motions:
            try:
                return machine_motion.get_output(name)
            except MachineMotionException:
                pass

        raise MachineException(f"Unable to find output with name: {name}")

    def get_pneumatic(self, name: str) -> IPneumatic:
        """
        Retrieves a Pneumatic by name.

        Args:
            name (str): The name of the Pneumatic.

        Returns:
            IPneumatic: The Pneumatic that was found.

        Raises:
            MachineException: If we cannot find the Pneumatic.
        """
        for machine_motion in self._machine_motions:
            try:
                return machine_motion.get_pneumatic(name)
            except MachineMotionException:
                pass

        raise MachineException(f"Unable to find pneumatic with name: {name}")

    def get_ac_motor(self, name: str) -> IACMotor:
        """
        Retrieves an AC Motor by name.

        Args:
            name (str): The name of the AC Motor.

        Returns:
            IACMotor: The AC Motor that was found.

        Raises:
            MachineMotionException: If it is not found.
        """
        for machine_motion in self._machine_motions:
            try:
                return machine_motion.get_ac_motor(name)
            except MachineMotionException:
                pass

        raise MachineException(f"Unable to find AC Motor with name: {name}")

    def get_bag_gripper(self, name: str) -> IBagGripper:
        """
        Retrieves a Bag Gripper by name.

        Args:
            name (str): The name of the Bag Gripper

        Returns:
            IBagGripper: The Bag Gripper that was found.

        Raises:
            MachineMotionException: If it is not found.
        """
        for machine_motion in self._machine_motions:
            try:
                return machine_motion.get_bag_gripper(name)
            except MachineMotionException:
                pass

        raise MachineException(f"Unable to find Bag Gripper with name: {name}")

    @future_api
    def add_estop_listener(self, callback: EstopEventCallback) -> UUID:
        """
        Adds an Estop listener to execute when the Estop trigger state changes.

        Args:
            callback (Callable[[bool], None]): A callback for when the Estop trigger state changes, where the argument is the current estop trigger state.

        Returns:
            UUID: A handle on the added listener. Can be provided to 'remove_event_listener' to remove the listener.
        """
        return self._estop.add_estop_listener(callback)

    @future_api
    def remove_estop_listener(self, handle: UUID) -> bool:
        """
        Removes an already added estop listener via its handle.

        Args:
            handle (UUID): The handle of the listener to remove.

        Returns:
            bool: True if the handle was removed, False otherwise.
        """
        return self._estop.remove_estop_listener(handle)

    @property
    @future_api  # The decorator doesn't work with @property, so we had to rename the property to make it internal
    def _is_in_estop(self) -> Union[bool, None]:
        """bool: The boolean is True if Estop is triggered, otherwise False."""
        return self._estop.is_triggered

    def on_mqtt_event(
        self, topic: str, callback: Callable[[str, Optional[str]], None]
    ) -> None:
        """
        Attach a callback function to an MQTT topic.

        Args:
            topic (str): The topic to listen on.
            callback (Union[Callable[[str, str], None], None]): A callback where the first argument is the topic and the second is the message.

        """
        self._mqtt_client.subscribe(topic, callback)

    def publish_mqtt_event(self, topic: str, message: Optional[str] = None) -> None:
        """
        Publish an MQTT event.

        Args:
            topic (str): Topic to publish.
            message (Optional[str], optional): Optional message. Defaults to None.
        """
        self._mqtt_client.publish(topic, message)
