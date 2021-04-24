from gazpar.event_dao import EventDAO
from gazpar.event import Event
from sqlalchemy import create_engine
import datetime


# --------------------------------------------------------------------------------------------
class TestEventDAO:

    CONNECTION_STRING = "sqlite:///tests/resources/homeassistant.db"
    # CONNECTION_STRING = "mariadb+mariadbconnector://homeassistant:*******@192.168.1.210:3306/home_assistant?charset=utf8mb4"

    # ----------------------------------
    def test_load(self):

        engine = create_engine(TestEventDAO.CONNECTION_STRING, echo=True)

        with engine.connect() as connection:

            dao = EventDAO(connection)

            event = dao.load(1)

            assert(event.event_id == 1)

    # ----------------------------------
    def test_save(self):

        engine = create_engine(TestEventDAO.CONNECTION_STRING, echo=True)

        with engine.connect() as connection:

            dao = EventDAO(connection)

            event = Event()

            now = datetime.datetime.now()

            # context_id = uuid.uuid4().hex

            event.event_type = "state_changed"
            event.event_data = "{}"
            event.origin = "LOCAL"
            event.time_fired = now
            event.created = now
            event.context_id = "unit test context"

            event_id = dao.save(event)

            assert(event_id > 0)
