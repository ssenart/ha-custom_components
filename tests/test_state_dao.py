from gazpar.state_dao import StateDAO
from gazpar.state import State
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

            dao = StateDAO(connection)

            state = dao.load(1)

            assert(state.state_id == 1)

    # ----------------------------------
    def test_save(self):

        engine = create_engine(TestEventDAO.CONNECTION_STRING, echo=True)

        with engine.connect() as connection:

            dao = StateDAO(connection)

            state = State()

            now = datetime.datetime.now()

            # context_id = uuid.uuid4().hex

            state.state_id = 0
            state.domain = "sensor"
            state.entity_id = "gazpar_daily_energy"
            state.state = "45"
            state.attributes = """{
                "attr name 1": "attr value 1",
                "attr name 2": "attr value 2"
            }"""
            state.event_id = 1
            state.last_changed = now
            state.last_updated = now
            state.created = now
            state.context_id = "unit test context"
            state.context_user_id = None
            state.old_state_id = None

            state_id = dao.save(state)

            assert(state_id > 0)
