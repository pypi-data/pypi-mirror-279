class EventExternal:
    def __init__(self, external_event_id: int = 0, system_id: int = 0,
                 subsystem_id: int = 0, url: str = "", environment_id: int = 0,
                 external_event_identifier: str = "") -> None:
        self._external_event_id = external_event_id
        self._system_id = system_id
        self._subsystem_id = subsystem_id
        self._url = url
        self._external_event_identifier = external_event_identifier
        self._environment_id = environment_id

    @property
    def external_event_id(self) -> int:
        return self._external_event_id

    @property
    def system_id(self) -> int:
        return self._system_id

    @property
    def subsystem_id(self) -> int:
        return self._subsystem_id

    @property
    def url(self) -> str:
        return self._url

    @property
    def external_event_identifier(self) -> str:
        return self._external_event_identifier

    @property
    def environment_id(self) -> int:
        return self._environment_id

    # Setter methods (optional)
    @external_event_id.setter
    def external_event_id(self, value: int):
        self._external_event_id = value

    @system_id.setter
    def system_id(self, value: int):
        self._system_id = value

    @subsystem_id.setter
    def subsystem_id(self, value: int):
        self._subsystem_id = value

    @url.setter
    def url(self, value: str):
        self._url = value

    @external_event_identifier.setter
    def external_event_identifier(self, value: str):
        self._external_event_identifier = value

    @environment_id.setter
    def environment_id(self, value: int):
        self._environment_id = value
