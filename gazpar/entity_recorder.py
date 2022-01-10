from pygazpar.client import Client
from pygazpar.enum import PropertyName
from pygazpar.enum import Frequency
from gazpar.time_period import TimePeriod
from gazpar.entity import Entity
from gazpar.entity_dao import EntityDAO
from gazpar.util import Util
import json


# --------------------------------------------------------------------------------------------
class PyGazparOptions:

    # ----------------------------------
    def __init__(self):
        self.username = ""
        self.password = ""
        self.webdriver = "./drivers/geckodriver.exe"
        self.headlessMode = True
        self.wait_time = 20
        self.tmpdir = "./tmp"
        self.testMode = False


# --------------------------------------------------------------------------------------------
class EntityRecorder:

    # ----------------------------------
    def __init__(self, context_id: str, pygazparOptions: PyGazparOptions, databaseConnectionString: str):
        self.__context_id = context_id
        self.__pygazparOptions = pygazparOptions
        self.__databaseConnectionString = databaseConnectionString

    # ----------------------------------
    def load(self, meterReadingFrequency: Frequency, lastNRows: int, lastNDays: int) -> Entity:

        client = Client(self.__pygazparOptions.username, self.__pygazparOptions.password, self.__pygazparOptions.webdriver, self.__pygazparOptions.wait_time, self.__pygazparOptions.tmpdir, lastNRows, self.__pygazparOptions.headlessMode, meterReadingFrequency, lastNDays, self.__pygazparOptions.testMode)
        client.update()

        history = client.data()

        if len(history) > 0:

            entityIdByFrequency = {
                Frequency.HOURLY: "sensor.gazpar_hourly_energy",
                Frequency.DAILY: "sensor.gazpar_daily_energy",
                Frequency.WEEKLY: "sensor.gazpar_weekly_energy",
                Frequency.MONTHLY: "sensor.gazpar_monthly_energy"
            }

            entity = Entity("sensor", entityIdByFrequency[meterReadingFrequency])

            for i in range(len(history)):
                timePeriod = TimePeriod.parse(history[i][PropertyName.TIME_PERIOD.value], meterReadingFrequency)
                recordTime = timePeriod.endTime
                state = str(Util.toState(history[0:i + 1]))
                attributes = json.dumps(Util.toAttributes(self.__pygazparOptions.username, meterReadingFrequency, history[0:i + 1]))

                entity.addRecord(self.__context_id, recordTime, state, attributes)

            return entity
        else:
            return None

    # ----------------------------------
    def save(self, entity: Entity) -> None:

        if entity is not None:

            entityDAO = EntityDAO(self.__databaseConnectionString)

            entityDAO.save(entity)

    # ----------------------------------
    def saveAsStatistics(self, entity: Entity) -> None:

        if entity is not None:

            statisticEntity = Entity("sensor", "sensor.gas_test")

            for (event, state) in entity.history():

                attributes = {}
                attributes["unit_of_measurement"] = "m³"
                attributes["icon"] = "mdi:fire"
                attributes["state_class"] = "total_increasing"
                attributes["device_class"] = "gas"
                attributes["friendly_name"] = "Natural gas"

                attr = json.loads(state.attributes)

                state_value = attr.get("end_index_m3")

                if (state_value is not None):
                    statisticEntity.addRecord(self.__context_id, state.last_changed, str(state_value), json.dumps(attributes))

            entityDAO = EntityDAO(self.__databaseConnectionString)

            entityDAO.save(statisticEntity)
