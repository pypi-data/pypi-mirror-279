"""
Representation of a transition between two StateNodes.
"""
from typing import Any, Callable, Optional

from miros import return_status


class StateTransition:
    """Representation of a transition between two StateNodes."""

    def __init__(
        self,
        stateName: str,
        signal: str,
        guardFunc: Optional[Callable[[Any], bool]] = None,
    ):
        """
        Args:
            stateName: Target state
            signal: Signal that triggers the state change
            guardFunc (Optional): Function called to check whether or not we can change states.
        """
        self._stateName = stateName
        self._signal = signal
        self._guardFunc = guardFunc
        self._machine: Any = None

    def setStateMachine(self, machine: Any) -> None:
        """Internal use only.

        Set the state machine.

        :param machine: StateMachine
        :param machine: Any:

        """
        self._machine = machine

    def getSignal(self) -> str:
        """Returns the signal that this transition waits on


        :returns: The transition

        :rtype: str

        """
        return self._signal

    def executeTransition(self, chart: Any, e: Any) -> return_status:
        """Internal use only.

        Transitions to the new state if the guard function passes, otherwise it does not.

        :param chart: Miros Factory
        :param e: Miros Event
        :param Return:
        :param chart: Any:
        :param e: Any:

        """
        if self._guardFunc is None or self._guardFunc(e.payload) is True:
            state = self._machine.getRawStateByName(self._stateName)
            return self._machine.getRawFactory().trans(state)
        else:
            return return_status.HANDLED
