from gazpar.entity_recorder import EntityRecorder, PyGazparOptions
from pygazpar.enum import Frequency


# --------------------------------------------------------------------------------------------
class TestEntityRecorder:

    CONNECTION_STRING = "sqlite:///tests/resources/homeassistant.db"

    # ----------------------------------
    def test_load_hourly(self):

        pygazparOptions = PyGazparOptions()
        pygazparOptions.testMode = True

        entityRecorder = EntityRecorder("unit test context", pygazparOptions, TestEntityRecorder.CONNECTION_STRING)

        entity = entityRecorder.load(Frequency.HOURLY, 0)

        assert(entity is None)

    # ----------------------------------
    def test_load_daily(self):

        pygazparOptions = PyGazparOptions()
        pygazparOptions.testMode = True

        entityRecorder = EntityRecorder("unit test context", pygazparOptions, TestEntityRecorder.CONNECTION_STRING)

        entity = entityRecorder.load(Frequency.DAILY, 0)

        assert(711 == len(entity.history()))

    # ----------------------------------
    def test_load_weekly(self):

        pygazparOptions = PyGazparOptions()
        pygazparOptions.testMode = True

        entityRecorder = EntityRecorder("unit test context", pygazparOptions, TestEntityRecorder.CONNECTION_STRING)

        entity = entityRecorder.load(Frequency.WEEKLY, 0)

        assert(102 == len(entity.history()))

    # ----------------------------------
    def test_load_monthly(self):

        pygazparOptions = PyGazparOptions()
        pygazparOptions.testMode = True

        entityRecorder = EntityRecorder("unit test context", pygazparOptions, TestEntityRecorder.CONNECTION_STRING)

        entity = entityRecorder.load(Frequency.MONTHLY, 0)

        assert(24 == len(entity.history()))

    # ----------------------------------
    def test_save_hourly(self):

        pygazparOptions = PyGazparOptions()
        pygazparOptions.testMode = True

        entityRecorder = EntityRecorder("unit test context", pygazparOptions, TestEntityRecorder.CONNECTION_STRING)

        entity = entityRecorder.load(Frequency.HOURLY, 0)

        entityRecorder.save(entity)

    # ----------------------------------
    def test_save_daily(self):

        pygazparOptions = PyGazparOptions()
        pygazparOptions.testMode = True

        entityRecorder = EntityRecorder("unit test context", pygazparOptions, TestEntityRecorder.CONNECTION_STRING)

        entity = entityRecorder.load(Frequency.DAILY, 0)

        entityRecorder.save(entity)

    # ----------------------------------
    def test_save_weekly(self):

        pygazparOptions = PyGazparOptions()
        pygazparOptions.testMode = True

        entityRecorder = EntityRecorder("unit test context", pygazparOptions, TestEntityRecorder.CONNECTION_STRING)

        entity = entityRecorder.load(Frequency.WEEKLY, 0)

        entityRecorder.save(entity)

    # ----------------------------------
    def test_save_monthly(self):

        pygazparOptions = PyGazparOptions()
        pygazparOptions.testMode = True

        entityRecorder = EntityRecorder("unit test context", pygazparOptions, TestEntityRecorder.CONNECTION_STRING)

        entity = entityRecorder.load(Frequency.MONTHLY, 0)

        entityRecorder.save(entity)

    # ----------------------------------
    def test_save_statistics(self):

        pygazparOptions = PyGazparOptions()
        # pygazparOptions.testMode = True
        pygazparOptions.username = "stephane.senart@gmail.com"
        pygazparOptions.password = "IfkDMMmrvrH27HjVovKh"

        entityRecorder = EntityRecorder("unit test context", pygazparOptions, TestEntityRecorder.CONNECTION_STRING)

        entity = entityRecorder.load(Frequency.DAILY, 0, 1095)

        entityRecorder.saveAsStatistics(entity)
