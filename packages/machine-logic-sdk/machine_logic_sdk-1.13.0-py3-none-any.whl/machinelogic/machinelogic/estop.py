import json
from typing import Optional, Union
from uuid import UUID, uuid4

from ..ivention.exception import EstopException
from ..ivention.iestop import EstopEventCallback, IEstop
from ..ivention.mqtt_client import MqttClient


class Estop(IEstop):
    """
    Represents the Estop module. An Estop module can be either triggered, in which case no motion can occur, or released, allowing motions to take place.
    """

    def __init__(self, mqtt: MqttClient):
        self._mqtt_client = mqtt
        self._is_in_estop: Union[bool, None] = None
        self._listeners: dict[UUID, EstopEventCallback] = {}
        self._mqtt_client.internal_subscribe("execution-engine/estop", self._on_estop)

    def _on_estop(self, topic: str, payload: Optional[str]) -> None:
        """
        Sets _is_in_estop to True if currently triggered and False if released.

        Args:
            payload (Optional[str]): estop JSON payload.
        """
        if payload is None:
            return  # to silence pylint

        try:
            parsed = json.loads(payload)
            value = parsed["estop"]
            if value == "Triggered":
                self._is_in_estop = True
            elif value == "Unknown":
                self._is_in_estop = None
            else:
                self._is_in_estop = False
            self._notify_listeners(self._is_in_estop)
        except Exception as error:
            raise EstopException(f"failed to parse {topic}: {payload}") from error

    @property
    def is_triggered(self) -> Union[bool, None]:
        return self._is_in_estop

    def add_estop_listener(self, callback: EstopEventCallback) -> UUID:
        uuid = uuid4()
        self._listeners[uuid] = callback
        return uuid

    def remove_estop_listener(self, handle: UUID) -> bool:
        return self._listeners.pop(handle, None) is not None

    def _notify_listeners(self, triggered: Union[bool, None]) -> None:
        """
        Calls the callback on all estop listeners interested in the provided topic.

        Args:
            triggered (bool): True if triggered, otherwise False.
        """
        for listener in self._listeners.values():
            listener(triggered)
