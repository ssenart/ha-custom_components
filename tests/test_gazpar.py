from gazpar.sensor import setup_platform
from gazpar.sensor import CONF_USERNAME, CONF_PASSWORD, CONF_WEBDRIVER, CONF_WAITTIME, CONF_TMPDIR, CONF_SCAN_INTERVAL
import os


class TestGazpar:

    _entities = []

    def add_entities(self, entities: list, flag: bool):
        self._entities.extend(entities)

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
            CONF_SCAN_INTERVAL: 600
        }

        setup_platform(None, config, self.add_entities, True)

        for entity in self._entities:
            entity.update()

    def test_dummy(self):

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
            CONF_SCAN_INTERVAL: 600
        }

        setup_platform(None, config, self.add_entities, False)

        for entity in self._entities:
            entity.update()
