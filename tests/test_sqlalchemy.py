from sqlalchemy import create_engine
from sqlalchemy.sql import text
import datetime
import traceback

# see https://data.home-assistant.io/docs/states
# see https://data.home-assistant.io/docs/events

# see https://www.plus2net.com/python/mysql-insert-sqlalchemy.php


# --------------------------------------------------------------------------------------------
class TestSqlAlchemy:

    CONNECTION_STRING = "sqlite:///tests/resources/homeassistant.db"
    # CONNECTION_STRING = "mariadb+mariadbconnector://homeassistant:*******@192.168.1.210:3306/home_assistant?charset=utf8mb4"

    def test_select(self):

        engine = create_engine(TestSqlAlchemy.CONNECTION_STRING, echo=True)

        with engine.connect() as connection:

            query = text("select * from states where entity_id='sensor.gazpar_daily_energy'")

            result = connection.execute(query)

            rows = result.fetchall()

            for row in rows:
                print(row)

    def test_insert(self):

        engine = create_engine(TestSqlAlchemy.CONNECTION_STRING, echo=True)

        with engine.connect() as connection:
            with connection.begin() as transaction:

                try:
                    insert_query = text("insert into events (event_type, event_data, origin, time_fired, created, context_id) values (:event_type, :event_data, :origin, :time_fired, :created, :context_id)")

                    now = datetime.datetime.now()

                    # context_id = uuid.uuid4().hex
                    context_id = "mon contexte"

                    row = {
                        "event_type": "state_changed",
                        "event_data": "{}",
                        "origin": "LOCAL",
                        "time_fired": now,
                        "created": now,
                        "context_id": context_id,
                    }

                    connection.execute(insert_query, row)

                    select_query = text("select LAST_INSERT_ROWID()")

                    result = connection.execute(select_query)

                    row = result.fetchone()

                    transaction.rollback()

                except Exception:
                    transaction.rollback()
                    raise
