from gazpar.entity import Entity
from gazpar.event_dao import EventDAO
from gazpar.state_dao import StateDAO
from sqlalchemy import create_engine
import logging


# --------------------------------------------------------------------------------------------
class EntityDAO:

    logger = logging.getLogger(__file__)

    # ----------------------------------
    def __init__(self, connectionString: str):
        self.__connectionString = connectionString

    # ----------------------------------
    def save(self, entity: Entity) -> None:

        engine = create_engine(self.__connectionString, echo=True)

        with engine.connect() as connection:
            with connection.begin() as transaction:

                try:
                    eventDAO = EventDAO(connection)
                    stateDAO = StateDAO(connection)

                    history = entity.history()

                    old_state_id = None

                    for (event, state) in history:

                        event_id = eventDAO.save(event)

                        state.event_id = event_id
                        state.old_state_id = old_state_id

                        old_state_id = stateDAO.save(state)

                    transaction.commit()

                    logging.info(f"{len(history)} records have been written in database")
                except Exception:
                    logging.error("An unexpected exception occured : ", exc_info=True)
                    transaction.rollback()
                    raise
