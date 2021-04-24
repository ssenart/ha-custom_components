from datetime import datetime


# --------------------------------------------------------------------------------------------
# Documentation : https://data.home-assistant.io/docs/events
class Event:

    __EVENT_ID = "event_id"
    __EVENT_TYPE = "event_type"
    __EVENT_DATA = "event_data"
    __ORIGIN = "origin"
    __TIME_FIRED = "time_fired"
    __CREATED = "created"
    __CONTEXT_ID = "context_id"
    __CONTEXT_USER_ID = "context_user_id"
    __CONTEXT_PARENT_ID = "context_parent_id"

    # ----------------------------------
    def __init__(self):
        self.__event_dict = {}

    # ----------------------------------
    @classmethod
    def create(cls, event_dict: dict):
        res = cls()
        res.__event_dict = event_dict

        return res

    # ----------------------------------
    @property
    def event_id(self) -> int:
        return self.__event_dict.get(Event.__EVENT_ID)

    # ----------------------------------
    @event_id.setter
    def event_id(self, value: int):
        self.__event_dict[Event.__EVENT_ID] = value

    # ----------------------------------
    @property
    def event_type(self) -> str:
        return self.__event_dict.get(Event.__EVENT_TYPE)

    # ----------------------------------
    @event_type.setter
    def event_type(self, value: str):
        self.__event_dict[Event.__EVENT_TYPE] = value

    # ----------------------------------
    @property
    def event_data(self) -> str:
        return self.__event_dict.get(Event.__EVENT_DATA)

    # ----------------------------------
    @event_data.setter
    def event_data(self, value: str):
        self.__event_dict[Event.__EVENT_DATA] = value

    # ----------------------------------
    @property
    def origin(self) -> str:
        return self.__event_dict.get(Event.__ORIGIN)

    # ----------------------------------
    @origin.setter
    def origin(self, value: str):
        self.__event_dict[Event.__ORIGIN] = value

    # ----------------------------------
    @property
    def time_fired(self) -> datetime:
        return self.__event_dict.get(Event.__TIME_FIRED)

    # ----------------------------------
    @time_fired.setter
    def time_fired(self, value: datetime):
        self.__event_dict[Event.__TIME_FIRED] = value

    # ----------------------------------
    @property
    def created(self) -> datetime:
        return self.__event_dict.get(Event.__CREATED)

    # ----------------------------------
    @created.setter
    def created(self, value: datetime):
        self.__event_dict[Event.__CREATED] = value

    # ----------------------------------
    @property
    def context_id(self) -> str:
        return self.__event_dict.get(Event.__CONTEXT_ID)

    # ----------------------------------
    @context_id.setter
    def context_id(self, value: str):
        self.__event_dict[Event.__CONTEXT_ID] = value

    # ----------------------------------
    def to_dict(self) -> dict:
        return self.__event_dict.copy()
