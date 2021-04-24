from gazpar.sensor import CONF_TESTMODE, setup_platform
from gazpar.sensor import CONF_USERNAME, CONF_PASSWORD, CONF_WEBDRIVER, CONF_WAITTIME, CONF_TMPDIR, CONF_SCAN_INTERVAL
import os
import logging
import json


# --------------------------------------------------------------------------------------------
class TestGazparSensor:

    logger = logging.getLogger(__name__)

    _entities = []

    # ----------------------------------
    def add_entities(self, entities: list, flag: bool):
        self._entities.extend(entities)

    # ----------------------------------
    def test_live(self):

        if os.name == 'nt':
            webdriver = "./drivers/geckodriver.exe"
        else:
            webdriver = "./drivers/geckodriver"

        config = {
            CONF_USERNAME: os.environ["GRDF_USERNAME"],
            CONF_PASSWORD: os.environ["GRDF_PASSWORD"],
            CONF_WEBDRIVER: webdriver,
            CONF_WAITTIME: 30,
            CONF_TMPDIR: "./tmp",
            CONF_SCAN_INTERVAL: 600,
            CONF_TESTMODE: False
        }

        setup_platform(None, config, self.add_entities)

        for entity in self._entities:
            entity.update()
            attributes = entity.device_state_attributes

            TestGazparSensor.logger.info(f"attributes={json.dumps(attributes, indent=2)}")

    # ----------------------------------
    def test_sample(self):

        if os.name == 'nt':
            webdriver = "./drivers/geckodriver.exe"
        else:
            webdriver = "./drivers/geckodriver"

        config = {
            CONF_USERNAME: os.environ["GRDF_USERNAME"],
            CONF_PASSWORD: os.environ["GRDF_PASSWORD"],
            CONF_WEBDRIVER: webdriver,
            CONF_WAITTIME: 30,
            CONF_TMPDIR: "./tmp",
            CONF_SCAN_INTERVAL: 600,
            CONF_TESTMODE: True
        }

        setup_platform(None, config, self.add_entities)

        for entity in self._entities:
            entity.update()
            attributes = entity.device_state_attributes

            TestGazparSensor.logger.info(f"attributes={json.dumps(attributes, indent=2)}")
