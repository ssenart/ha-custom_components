import copy


# --------------------------------------------------------------------------------------------
# Documentation : # see https://data.home-assistant.io/docs/states
class State:

    __STATE_ID = "state_id"
    __DOMAIN = "domain"
    __ENTITY_ID = "entity_id"
    __STATE = "state"
    __ATTRIBUTES = "attributes"
    __EVENT_ID = "event_id"
    __LAST_CHANGED = "last_changed"
    __LAST_UPDATED = "last_updated"
    __CREATED = "created"
    __CONTEXT_ID = "context_id"
    __CONTEXT_USER_ID = "context_user_id"
    __OLD_STATE_ID = "old_state_id"

    # ----------------------------------
    def __init__(self):
        self.__state_dict = {}

    # ----------------------------------
    @classmethod
    def create(cls, state_dict: dict):
        res = cls()
        res.__state_dict = state_dict

        return res

    # ----------------------------------
    @property
    def state_id(self) -> int:
        return self.__state_dict.get(State.__STATE_ID)

    # ----------------------------------
    @state_id.setter
    def state_id(self, value: int):
        self.__state_dict[State.__STATE_ID] = value

    # ----------------------------------
    @property
    def domain(self) -> str:
        return self.__state_dict.get(State.__DOMAIN)

    # ----------------------------------
    @domain.setter
    def domain(self, value: str):
        self.__state_dict[State.__DOMAIN] = value

    # ----------------------------------
    @property
    def entity_id(self) -> str:
        return self.__state_dict.get(State.__ENTITY_ID)

    # ----------------------------------
    @entity_id.setter
    def entity_id(self, value: str):
        self.__state_dict[State.__ENTITY_ID] = value

    # ----------------------------------
    @property
    def state(self) -> str:
        return self.__state_dict.get(State.__STATE)

    # ----------------------------------
    @state.setter
    def state(self, value: str):
        self.__state_dict[State.__STATE] = value

    # ----------------------------------
    @property
    def attributes(self) -> str:
        return self.__state_dict.get(State.__ATTRIBUTES)

    # ----------------------------------
    @attributes.setter
    def attributes(self, value: str):
        self.__state_dict[State.__ATTRIBUTES] = value

    # ----------------------------------
    @property
    def event_id(self) -> str:
        return self.__state_dict.get(State.__EVENT_ID)

    # ----------------------------------
    @event_id.setter
    def event_id(self, value: str):
        self.__state_dict[State.__EVENT_ID] = value

    # ----------------------------------
    @property
    def last_changed(self) -> str:
        return self.__state_dict.get(State.__LAST_CHANGED)

    # ----------------------------------
    @last_changed.setter
    def last_changed(self, value: str):
        self.__state_dict[State.__LAST_CHANGED] = value

    # ----------------------------------
    @property
    def last_updated(self) -> str:
        return self.__state_dict.get(State.__LAST_UPDATED)

    # ----------------------------------
    @last_updated.setter
    def last_updated(self, value: str):
        self.__state_dict[State.__LAST_UPDATED] = value

    # ----------------------------------
    @property
    def created(self) -> str:
        return self.__state_dict.get(State.__CREATED)

    # ----------------------------------
    @created.setter
    def created(self, value: str):
        self.__state_dict[State.__CREATED] = value

    # ----------------------------------
    @property
    def context_id(self) -> str:
        return self.__state_dict.get(State.__CONTEXT_ID)

    # ----------------------------------
    @context_id.setter
    def context_id(self, value: str):
        self.__state_dict[State.__CONTEXT_ID] = value

    # ----------------------------------
    @property
    def context_user_id(self) -> str:
        return self.__state_dict.get(State.__CONTEXT_USER_ID)

    # ----------------------------------
    @context_user_id.setter
    def context_user_id(self, value: str):
        self.__state_dict[State.__CONTEXT_USER_ID] = value

    # ----------------------------------
    @property
    def old_state_id(self) -> str:
        return self.__state_dict.get(State.__OLD_STATE_ID)

    # ----------------------------------
    @old_state_id.setter
    def old_state_id(self, value: str):
        self.__state_dict[State.__OLD_STATE_ID] = value

    # ----------------------------------
    def to_dict(self) -> dict:
        return self.__state_dict.copy()

    # ----------------------------------
    def copy(self):
        return copy.deepcopy(self)
