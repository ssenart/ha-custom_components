from util.event import Event
from sqlalchemy.engine import Connection
from sqlalchemy.sql import text


# --------------------------------------------------------------------------------------------
class EventDAO:

    __QUERY_BY_ENGINE = {
        "last_insert_id":
        {
            "sqlite": "select LAST_INSERT_ROWID() as event_id",
            "mariadb": "select LAST_INSERT_ID() as event_id"
        }
    }

    # ----------------------------------
    def __init__(self, connection: Connection):
        self.__connection = connection

    # ----------------------------------
    def load(self, event_id: int) -> Event:

        query = text(f"select * from events where event_id={event_id}")

        result = self.__connection.execute(query)

        row = result.fetchone()

        res = Event.create(dict(row))

        return res

    # ----------------------------------
    def save(self, event: Event) -> int:

        insert_query = text("insert into events (event_type, event_data, origin, time_fired, created, context_id) values (:event_type, :event_data, :origin, :time_fired, :created, :context_id)")

        self.__connection.execute(insert_query, event.to_dict())

        select_query = text(EventDAO.__QUERY_BY_ENGINE["last_insert_id"][self.__connection.engine.name])

        result = self.__connection.execute(select_query)

        row = result.fetchone()

        event.event_id = row["event_id"]

        return event.event_id

    # ----------------------------------
    def delete(self, context_id: str) -> int:

        insert_query = text("delete from events where where context_id=:context_id")

        parameters = {
            "context_id": context_id
        }

        result = self.__connection.execute(insert_query, parameters)

        return result.rowcount
