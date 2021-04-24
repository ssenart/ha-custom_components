from gazpar.state import State
from sqlalchemy.engine import Connection
from sqlalchemy.sql import text


# --------------------------------------------------------------------------------------------
class StateDAO:

    __QUERY_BY_ENGINE = {
        "last_insert_id":
        {
            "sqlite": "select LAST_INSERT_ROWID() as state_id",
            "mariadb": "select LAST_INSERT_ID() as state_id"
        }
    }

    # ----------------------------------
    def __init__(self, connection: Connection):
        self.__connection = connection

    # ----------------------------------
    def load(self, state_id: int) -> State:

        query = text(f"select * from states where state_id={state_id}")

        result = self.__connection.execute(query)

        row = result.fetchone()

        res = State.create(dict(row))

        return res

    # ----------------------------------
    def save(self, state: State) -> int:

        insert_query = text("insert into states (domain, entity_id, state, attributes, event_id, last_changed, last_updated, created, context_id, context_user_id, old_state_id) values (:domain, :entity_id, :state, :attributes, :event_id, :last_changed, :last_updated, :created, :context_id, :context_user_id, :old_state_id)")

        self.__connection.execute(insert_query, state.to_dict())

        select_query = text(StateDAO.__QUERY_BY_ENGINE["last_insert_id"][self.__connection.engine.name])

        result = self.__connection.execute(select_query)

        row = result.fetchone()

        state.state_id = row["state_id"]

        return state.state_id

    # ----------------------------------
    def delete(self, context_id: str) -> int:

        insert_query = text("delete from states where event_id in (select event_id from events where context_id=:context_id)")

        parameters = {
            "context_id": context_id
        }

        result = self.__connection.execute(insert_query, parameters)

        return result.rowcount
