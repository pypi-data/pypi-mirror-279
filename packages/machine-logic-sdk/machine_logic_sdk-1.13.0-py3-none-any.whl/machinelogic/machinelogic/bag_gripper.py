# pylint: disable=duplicate-code
import json
from typing import List, Optional

from ..ivention.exception import BagGripperException
from ..ivention.ibag_gripper import BagGripperConfiguration, IBagGripper
from ..ivention.mqtt_client import MqttClient
from ..ivention.util.inheritance import inherit_docstrings  # type: ignore
from .api import Api


@inherit_docstrings
class BagGripper(IBagGripper):
    def __init__(
        self, configuration: BagGripperConfiguration, api: Api, mqtt_client: MqttClient
    ) -> None:
        super().__init__(configuration)
        self._api = api
        self._pin_state: dict[str, bool] = {
            "input_pin_close": False,
            "input_pin_open": False,
        }
        mqtt_client.internal_subscribe(
            f"execution-engine/controller/{self.configuration._controller_id}/io",
            lambda _, payload: self._on_digital_input(payload),
        )

    def _on_digital_input(self, payload: Optional[str]) -> None:
        if payload is None:
            raise BagGripperException(
                f"Lacking digital input bag gripper with name {self.configuration.name}"
            )
        payload_json = json.loads(payload)
        filtered_for_device = [
            deviceState
            for deviceState in payload_json
            if (int(deviceState["device"]) == int(self.configuration.device))
            and (deviceState["deviceType"] == "io-expander")
        ]
        if len(filtered_for_device) == 0:
            return
        pin_states = filtered_for_device[0]["pinStates"]
        self._update_pin_state(pin_states)

    def _update_pin_state(self, pin_states: List[int]) -> None:
        self._pin_state["input_pin_open"] = bool(
            pin_states[self.configuration.input_pin_open]
        )
        self._pin_state["input_pin_close"] = bool(
            pin_states[self.configuration.input_pin_close]
        )
        self._update_pneumatic_state()

    def _update_pneumatic_state(self) -> None:
        pin_open = self._pin_state["input_pin_open"]
        pin_close = self._pin_state["input_pin_close"]
        # https://github.com/VentionCo/mm-programmatic-sdk/issues/478
        if pin_close is False and pin_open is False:
            self._state = "unknown"
        elif pin_close is True and pin_open is True:
            self._state = "transition"
        elif pin_close is False:
            self._state = "closed"
        elif pin_open is False:
            self._state = "open"
        else:
            self._state = "unknown"

    def open_async(self) -> None:
        if not self._api.open_bag_gripper(self.configuration.uuid):
            raise BagGripperException(
                f"Failed to open bag gripper with name {self.configuration.name}"
            )

    def close_async(self) -> None:
        if not self._api.close_bag_gripper(self.configuration.uuid):
            raise BagGripperException(
                f"Failed to close bag gripper with name {self.configuration.name}"
            )
