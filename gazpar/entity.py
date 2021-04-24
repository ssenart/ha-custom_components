from gazpar.state import State
from gazpar.event import Event
from datetime import datetime


# --------------------------------------------------------------------------------------------
class Entity:

    # ----------------------------------
    def __init__(self, domain: str, entity_id: str):

        self.__domain = domain
        self.__entity_id = entity_id
        self.__event_state_history = []

    # ----------------------------------
    def addRecord(self, context_id: str, record_time: datetime, value: str, attributes: dict) -> State:

        state = State()

        state.state_id = None
        state.domain = self.__domain
        state.entity_id = self.__entity_id
        state.state = value
        state.attributes = attributes
        state.event_id = 0
        state.last_changed = record_time
        state.last_updated = record_time
        state.created = record_time
        state.context_id = None
        state.context_user_id = None

        if len(self.__event_state_history) > 0:
            state.old_state_id = self.__event_state_history[-1][1].state_id
        else:
            state.old_state_id = None

        event = Event()
        event.event_id = 0
        event.event_type = "state_changed"
        event.event_data = "{}"
        event.origin = "LOCAL"
        event.time_fired = record_time
        event.created = record_time
        event.context_id = context_id

        self.__event_state_history.append((event, state))

        return state

    # ----------------------------------
    def state(self) -> str:

        if len(self.__event_state_history) > 0:
            return self.__event_state_history[-1][1].state
        else:
            return None

    # ----------------------------------
    def attributes(self) -> dict:

        if len(self.__event_state_history) > 0:
            return self.__event_state_history[-1][1].attributes
        else:
            return None

    # ----------------------------------
    def history(self) -> list:

        return self.__event_state_history
