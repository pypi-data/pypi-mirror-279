from abc import ABC, abstractmethod
from typing import Callable, Union
from uuid import UUID

EstopEventCallback = Callable[[Union[bool, None]], None]


class IEstop(ABC):
    """
    Represents the Estop module. An Estop module can be either triggered, in which case no motion can occur, or released, allowing motions to take place.
    """

    @property
    @abstractmethod
    def is_triggered(self) -> Union[bool, None]:
        """
        Indicates if the Estop is currently triggered.

        Returns:
            Union[bool, None]: True if the Estop is currently triggered, False if it is currently released, None if the estop state is unknown.
        """

    @abstractmethod
    def add_estop_listener(self, callback: EstopEventCallback) -> UUID:
        """
        Adds an Estop listener to execute when the Estop trigger state changes.

        Args:
            callback (EstopEventCallback): A callback for when the Estop trigger state changes, where the argument is the current estop trigger state.

        Returns:
            UUID: A handle on the added listener. Can be provided to 'remove_event_listener' to remove the listener.
        """

    @abstractmethod
    def remove_estop_listener(self, handle: UUID) -> bool:
        """
        Removes an already added estop listener via its handle.

        Args:
            handle (UUID): The handle of the listener to remove.

        Returns:
            bool: True if the handle was removed, False otherwise.
        """
