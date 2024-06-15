from typing import Any, Optional

from miros import Event, return_status

from .state_transition import StateTransition


class StateNode:
    """Base StateNode class that an implementer will extend to create their State."""

    def __init__(self, name: str, parentName: Optional[str] = None):
        """
        Args:
            name: Name of the node
            parentName (Optional): Name of the parent node state
        """
        self._name = name
        self._parentName = parentName
        self._rawState = None
        self._chart: Any = None
        self._lastHandle = return_status.HANDLED

    # Internal use only
    def setChart(self, chart: Any) -> None:
        """Internal use only. Set the Miros chart.

        :param chart: Miros chart
        :param chart: Any:

        """
        self._chart = chart

    def getName(self) -> str:
        """


        :returns: The name of the node.

        :rtype: str

        """
        return self._name

    def setRawState(self, rawState: Any) -> None:
        """Internal use only. Set the Miros state.

        :param rawState: Miros state
        :param rawState: Any:

        """
        self._rawState = rawState

    def getRawState(self) -> Any:
        """Internal use only. Get the Miros state.


        :returns: The Miros state

        """
        return self._rawState

    def internalOnEnter(self, chart: Any, e: Any) -> return_status:
        """Internal use only. onEnter handler

        :param chart: Any:
        :param e: Any:
        :returns: A valid return_status, most likely HANDLED

        """
        self._lastHandle = return_status.HANDLED
        self.onEnter()
        return self._lastHandle

    def internalOnUpdate(self, chart: Any, e: Any) -> return_status:
        """Internal use only. onUpdate handler

        :param chart: Any:
        :param e: Any:
        :returns: A valid return_status, most likely HANDLED

        """
        self._lastHandle = return_status.HANDLED
        self.onUpdate()
        return self._lastHandle

    def internalOnExit(self, chart: Any, e: Any) -> return_status:
        """Internal use only. onExit handler

        :param chart: Any:
        :param e: Any:
        :returns: A valid return_status, most likely HANDLED

        """
        self._lastHandle = return_status.HANDLED
        self.onExit()
        return self._lastHandle

    def publish(self, signal: str, payload: Any = None) -> None:
        """Publish a signal to the state machine

        :param signal: The signal that you would like to publish
        :param payload: The payload that will accompany the signal
        :param signal: str:
        :param payload: Any:  (Default value = None)

        """
        self._chart.getRawFactory().publish(Event(signal=signal, payload=payload))

    # User implmented section
    def onEnter(self) -> None:
        """Action called when this state is entered."""
        return

    def onExit(self) -> None:
        """Action called when this state is exited."""
        return

    def onUpdate(self) -> None:
        """When your state machine specified an "updateInterval", this function will be called every tick."""
        return

    def getTransitions(self) -> list[StateTransition]:
        """


        :returns: list of state transitions from this node.

        """
        return []
