class DigitalIOState:
    """
    Representation of the current state of an DigitalInput/DigitalOutput instance.
    """

    def __init__(self, configuration: "DigitalIOConfiguration") -> None:
        # we pass a ref to configuration, so that we can access the active high
        # attribute (and have it work throughout the application).
        self._configuration = configuration
        self._value: bool = False  # honest value, ignoring "active_high" flips.

    @property
    def value(self) -> bool:
        """
        bool: The current value of the IO pin. True means high, while False means low. This is different from
        active/inactive, which depends on the active_high configuration.
        """
        if not self._configuration.active_high:
            return not self._value
        return self._value


class DigitalIOConfiguration:
    """
    Representation of the configuration of an DigitalInput/DigitalOutput. This
    configuration is established by the configuration page in
    MachineLogic.
    """

    def __init__(
        self,
        uuid: str,
        name: str,
        device: int,
        pin: int,
        ip_address: str,
        active_high: bool,
    ) -> None:
        self._uuid: str = uuid
        self._name: str = name
        self._device: int = device
        self._port: int = pin
        self._ip_address: str = ip_address
        self._active_high: bool = active_high

    @property
    def name(self) -> str:
        """str: The name of the DigitalInput/DigitalOutput."""
        return self._name

    @property
    def active_high(self) -> bool:
        """bool: The value that needs to be set to consider the DigitalInput/DigitalOutput as active."""
        return self._active_high

    @active_high.setter
    def active_high(self, active_high: bool) -> None:
        """bool: Set active high to true/false on the DigitalInput/DigitalOutput."""
        self._active_high = active_high

    @property
    def device(self) -> int:
        """int: The device number of the DigitalInput/DigitalOutput."""
        return self._device

    @property
    def port(self) -> int:
        """int: The port number of the DigitalInput/DigitalOutput."""
        return self._port

    @property
    def ip_address(self) -> str:
        """str: The ip address of the DigitalInput/DigitalOutput."""
        return self._ip_address

    @property
    def uuid(self) -> str:
        """str: The unique ID of the DigitalInput/DigitalOutput."""
        return self._uuid
