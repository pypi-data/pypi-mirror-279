# pylint: disable=protected-access
import json
import warnings
from os import environ
from typing import Optional, Union

from ..ivention.iactuator import IActuator
from ..ivention.icamera import ICameraConfiguration
from ..ivention.idigital_input import IDigitalInput
from ..ivention.idigital_output import IDigitalOutput
from ..ivention.imachine import IMachine
from ..ivention.imachine_motion import IMachineMotion
from ..ivention.machine_configuration import MachineConfiguration
from ..ivention.mqtt_client import MqttClient
from ..ivention.util.inheritance import inherit_docstrings  # type: ignore
from .ac_motor import ACMotor
from .actuator import Actuator
from .api import Api
from .bag_gripper import BagGripper
from .camera import Camera
from .digital_input import DigitalInput
from .digital_output import DigitalOutput
from .estop import Estop
from .machine_motion import MachineMotion
from .pneumatic import Pneumatic
from .robot import Robot

# Global variables specifying the URL of the execution engine and the MQTT broker
# This is probably only going to be used in the cloud when spawning remote execution engines and the user doesn't control the ips
# Otherwise, users would provide the machines IP strings through the constructor argument.

MM_EXECUTION_ENGINE_DEFAULT_PORT = "3100"
MQTT_DEFAULT_PORT = "9001"

MM_EXECUTION_ENGINE_CONNECTION_STR = environ.get(
    "EXECUTION_ENGINE_CONN_STR", "http://localhost:3100"
)
MQTT_CONNECTION_STR = environ.get("MQTT_CONN_STR", "ws://localhost:9001")


@inherit_docstrings
class Machine(IMachine):
    def __init__(self, ip_address: Union[str, None] = None) -> None:
        if ip_address:
            api_connection_string = (
                f"http://{ip_address}:{MM_EXECUTION_ENGINE_DEFAULT_PORT}"
            )
            mqtt_connection_string = f"ws://{ip_address}:{MQTT_DEFAULT_PORT}"
        else:
            api_connection_string = MM_EXECUTION_ENGINE_CONNECTION_STR
            mqtt_connection_string = MQTT_CONNECTION_STR

        api = Api(api_connection_string)
        machine_configuration = api.get_machine_configuration()

        mqtt_client = MqttClient(mqtt_connection_string)

        machine_motions = _create_machine_motions(
            machine_configuration, api, mqtt_client
        )
        estop = Estop(mqtt_client)

        super().__init__(
            machine_motions,
            mqtt_client,
            estop,
        )

        mqtt_client.internal_subscribe(
            "execution-engine/input/+", self._on_input_update
        )
        mqtt_client.internal_subscribe(
            "execution-engine/output/+", self._on_output_update
        )
        mqtt_client.internal_subscribe(
            "execution-engine/axis/+/is_motion_complete",
            self._on_actuator_motion_complete,
        )
        mqtt_client.internal_subscribe(
            "execution-engine/axis/+/sensor_state",
            self._on_actuator_sensor_state,
        )

    def _on_actuator_sensor_state(self, topic: str, message: Optional[str]) -> None:
        # eg:
        # t: execution-engine/axis/c0329c46-3836-44b2-8015-19416019388c/sensor_state
        # message: {"home":true,"end":false}
        if message is None:
            return

        actuator_uuid = topic.split("/")[2]
        actuator = self._get_actuator_by_uuid(actuator_uuid)
        if actuator is None:
            return

        try:
            payload = json.loads(message)
            actuator.state._end_sensors = (payload["home"], payload["end"])
        except Exception as parse_error:  # pylint: disable=broad-except
            warnings.warn(f"bad payload {topic}: {parse_error}")

    def _on_actuator_motion_complete(self, topic: str, message: Optional[str]) -> None:
        # eg.
        # execution-engine/axis/3c4b20dc-9f1f-42e8-a517-eb7da08a228d/is_motion_complete	0
        # execution-engine/axis/3c4b20dc-9f1f-42e8-a517-eb7da08a228d/is_motion_complete	1

        if message is None:
            return

        actuator_uuid = topic.split("/")[2]
        actuator = self._get_actuator_by_uuid(actuator_uuid)
        if actuator is None:
            return

        motion_complete = bool(int(message))
        actuator.state._move_in_progress = not motion_complete

    def _on_input_update(self, topic: str, message: Optional[str]) -> None:
        split_topic = topic.split("/")
        if len(split_topic) != 3:
            return

        if message is None:
            return

        value = int(message)
        input_uuid = split_topic[2]
        found_input = self._get_input_by_uuid(input_uuid)
        if found_input is None:
            return

        found_input._set_value(value == 1)

    def _get_input_by_uuid(self, input_uuid: str) -> Optional[IDigitalInput]:
        for machine_motion in self._machine_motions:
            for input_item in machine_motion._input_list:
                if input_item.configuration.uuid == input_uuid:
                    return input_item

        return None

    def _get_actuator_by_uuid(self, actuator_uuid: str) -> Optional[IActuator]:
        for machine_motion in self._machine_motions:
            for actuator in machine_motion._actuator_list:
                if actuator.configuration.uuid == actuator_uuid:
                    return actuator
        return None

    def _on_output_update(self, topic: str, message: Optional[str]) -> None:
        split_topic = topic.split("/")
        if len(split_topic) != 3:
            return

        if message is None:
            return

        value = int(message)
        output_uuid = split_topic[2]
        output = self._get_output_by_uuid(output_uuid)
        if output is None:
            return

        output._set_value(value == 1)

    def _get_output_by_uuid(self, input_uuid: str) -> Optional[IDigitalOutput]:
        for machine_motion in self._machine_motions:
            for output in machine_motion._output_list:
                if output.configuration.uuid == input_uuid:
                    return output

        return None


def _create_machine_motions(
    machine_configuration: MachineConfiguration, api: Api, mqtt_client: MqttClient
) -> list[IMachineMotion]:
    """
    Creates a machine motion list from the provided machine configuration.

    Args:
        machine_configuration (MachineConfiguration): The machine configuration to build from.
        api (Api): The api used to execute hardware commands and queries.
        mqtt_connection_string (str): Mqtt connection string, used to determine mqtt transport

    Returns:
        list[IMachineMotion]: The list of available machine motions.
    """
    machine_motion_list: list[IMachineMotion] = []

    for controller_config in machine_configuration.machine_motion_configurations:
        machine_motion = MachineMotion(
            controller_config,
            api,
        )

        for robot_config in controller_config._robot_configuration_list:
            machine_motion._robot_list.append(Robot(robot_config, api))

        for axis_config in controller_config._actuator_configuration_list:
            machine_motion._actuator_list.append(Actuator(axis_config, api))

        for input_config in controller_config._input_configuration_list:
            new_input = DigitalInput(input_config, api)
            machine_motion._input_list.append(new_input)

        for output_config in controller_config._output_configuration_list:
            new_output = DigitalOutput(output_config, api)
            machine_motion._output_list.append(new_output)

        for pneumatic_config in controller_config._pneumatic_configuration_list:
            machine_motion._pneumatic_list.append(
                Pneumatic(pneumatic_config, api, mqtt_client)
            )

        for ac_motor_config in controller_config._ac_motor_configuration_list:
            machine_motion._ac_motor_list.append(ACMotor(ac_motor_config, api))

        for bag_gripper_config in controller_config._bag_gripper_configuration_list:
            machine_motion._bag_gripper_list.append(
                BagGripper(bag_gripper_config, api, mqtt_client)
            )

        if api.camera_service_present():
            new_camera = Camera(ICameraConfiguration("uuid", "camera"), api)
            machine_motion._camera_list.append(new_camera)

        machine_motion_list.append(machine_motion)

    return machine_motion_list
