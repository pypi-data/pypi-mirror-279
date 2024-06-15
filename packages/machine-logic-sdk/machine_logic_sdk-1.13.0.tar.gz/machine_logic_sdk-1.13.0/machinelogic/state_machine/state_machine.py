"""
This module is used to represent a Finite State Machine.
"""

from typing import Any

from miros import Event, Factory, return_status, signals

from .state_node import StateNode
from .state_transition import StateTransition


class StateMachineException(Exception):
    """ """


class StateMachine:
    """A Finite State Machine"""

    def __init__(
        self,
        name: str,
        liveTrace: bool = False,
        liveSpy: bool = False,
        updateInterval: float = 0,
    ):
        """
        Args:
            name: Name of the FSM
            liveTrace: If True, trace debug information will be printed to the console
            liveSpy: If True, state transition information will be printed to the console
            updateInterval: Interval in seconds. If greater than 0, StateNode::onUpdate will happen at the specified rate.
        """
        self._factory = Factory(name)
        self._factory.live_trace = False if liveTrace is None else liveTrace
        self._factory.live_spy = False if liveSpy is None else liveSpy

        self._ventionStates: list[StateNode] = []
        self._updateInterval = updateInterval

    def start(self, name: str) -> None:
        """Starts the state mahcine at the specified state.

        :param name: Name of the beginning state
        :param name: str:
        :raises StateMachineException: Raised if the state could not be found.

        """
        self._compile()
        state = self.getRawStateByName(name)
        if state is None:
            raise StateMachineException(f"Could not start at state with name: {name}")

        self._factory.start_at(state)

        if self._updateInterval != 0:
            self._factory.post_fifo(
                Event(signal=signals.UPDATE), period=self._updateInterval
            )

    def getRawFactory(self) -> Factory:
        """


        :returns: Miros factory

        :rtype: Factory

        """
        return self._factory

    def publish(self, signal: str, payload: Any = None) -> None:
        """Publish an event to the state machine.

        :param signal: The signal that you would like to publish
        :type signal: string
        :param payload: The payload that you would to be available by the catcher of the event.
        :type payload: any
        :param signal: str:
        :param payload: Any:  (Default value = None)

        """
        signalNumber = getattr(signals, signal)
        self._factory.publish(Event(signal=signalNumber, payload=payload))

    def getRawStateByName(self, name: str) -> Any:
        """Return the raw miros state given the name of the state.

        :param name: Name of state
        :param name: str:
        :returns: miros: Raw miros state, or None if not found

        """
        for state in self._ventionStates:
            if state.getName() is name:
                return state.getRawState()

        return None

    def hasState(self, name: str) -> bool:
        """Checks if the state with the provided name exists.

        :param name: The name of hte potential state.
        :param name: str:
        :returns: Whether or not the state exists.
        :rtype: bool

        """
        return self.getRawStateByName(name) is not None

    def getStatesList(self) -> list[StateNode]:
        """Returns the list of states have been added to this machine.


        :returns: List of states

        :rtype: list[StateNode]

        """
        return self._ventionStates

    def newState(self, state: StateNode) -> None:
        """Add the state node to the state machine.

        :param state: Node being added to the FSM.
        :param state: StateNode:
        :raises StateMachineException: If the name is a duplicate.

        """
        if self.hasState(state.getName()):
            raise StateMachineException(
                f"Cannot add two of the same state to the state machine. Trying to add: {state.getName()}"
            )

        def onEnter(chart: Factory, evnt: Event) -> return_status:
            """

            :param chart: Factory:
            :param evnt: Event:

            """
            return state.internalOnEnter(chart, evnt)

        def onUpdate(chart: Factory, evnt: Event) -> return_status:
            """

            :param chart: Factory:
            :param evnt: Event:

            """
            return state.internalOnUpdate(chart, evnt)

        def onExit(chart: Factory, evnt: Event) -> return_status:
            """

            :param chart: Factory:
            :param evnt: Event:

            """
            return state.internalOnExit(chart, evnt)

        mirosState = self._factory.create(state=state.getName())
        mirosState = mirosState.catch(signal=signals.INIT_SIGNAL, handler=onEnter)
        mirosState = mirosState.catch(signal=signals.UPDATE, handler=onUpdate)
        mirosState = mirosState.catch(signal=signals.EXIT_SIGNAL, handler=onExit)

        # Because a user can listen to the same signal more than once
        # but with different conditions, we combine them together
        # and select the first one that we can do.
        transitionMap: dict[str, list[StateTransition]] = {}
        for transition in state.getTransitions():
            if transition.getSignal() not in transitionMap:
                transitionMap[transition.getSignal()] = []

            transitionMap[transition.getSignal()].append(transition)
            transition.setStateMachine(self)

        for signal, transitionList in transitionMap.items():
            signalNumber = getattr(signals, signal)

            def handle(chart: Factory, e: Event) -> return_status:
                """

                :param chart: Factory:
                :param e: Event:

                """
                # For all transitions registered to this name, selct the first
                # one of them that works
                for transition in transitionList:
                    result = transition.executeTransition(chart, e)
                    if result == return_status.TRAN:
                        return result

                return return_status.HANDLED

            self._factory.subscribe(Event(signal=signalNumber))
            mirosState = mirosState.catch(signal=signalNumber, handler=handle)

        state.setRawState(mirosState.to_method())
        self._ventionStates.append(state)

    def _compile(self) -> None:
        """ """
        for state in self._ventionStates:
            # TODO: Include a parent name
            self._factory.nest(state.getRawState(), None)
            state.setChart(self)
