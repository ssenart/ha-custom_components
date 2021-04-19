"""Support for Gazpar."""
from datetime import timedelta
import json
import logging
import traceback

from pygazpar.client import Client, DummyClient
from pygazpar.enum import PropertyName
from pygazpar.enum import Frequency

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    ATTR_ATTRIBUTION, CONF_PASSWORD, CONF_USERNAME, CONF_SCAN_INTERVAL,
    ENERGY_KILO_WATT_HOUR, TEMP_CELSIUS)
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import track_time_interval, call_later

_LOGGER = logging.getLogger(__name__)

CONF_WEBDRIVER = "webdriver"
CONF_WAITTIME = "wait_time"
CONF_TMPDIR = "tmpdir"
DEFAULT_SCAN_INTERVAL = timedelta(hours=4)
DEFAULT_WAITTIME = 30
ICON_GAS = "mdi:fire"

HA_VOLUME_M3 = "m³"
HA_CONVERTOR_FACTOR_KWH_M3 = "kWh/m³"
HA_ATTRIBUTION = "Data provided by GrDF"
HA_TIME = "time"
HA_TIMESTAMP = "timestamp"
HA_TYPE = "type"

GAZPAR_DATE_FORMAT = "%d/%m/%Y"

HA_LAST_PERIOD_START_TIME = "Gazpar last period start time"
HA_LAST_PERIOD_END_TIME = "Gazpar last period end time"
HA_LAST_START_INDEX = "Gazpar last start index"
HA_LAST_END_INDEX = "Gazpar last end index"
HA_LAST_VOLUME_M3 = "Gazpar last volume"
HA_LAST_ENERGY_KWH = "Gazpar last energy"
HA_LAST_CONVERTER_FACTOR = "Gazpar last converter factor"
HA_LAST_TEMPERATURE = "Gazpar last temperature"

HA_LAST_ENERGY_KWH_BY_FREQUENCY = {
    Frequency.HOURLY: "Gazpar last hourly energy",
    Frequency.DAILY: "Gazpar last daily energy",
    Frequency.WEEKLY: "Gazpar last weekly energy",
    Frequency.MONTHLY: "Gazpar last monthly energy"
}

LAST_INDEX = -1
BEFORE_LAST_INDEX = -2

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Required(CONF_WEBDRIVER): cv.string,
    vol.Optional(CONF_WAITTIME, default=DEFAULT_WAITTIME): int,
    vol.Required(CONF_TMPDIR): cv.string,
    vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): cv.time_period
})


# --------------------------------------------------------------------------------------------
def setup_platform(hass, config, add_entities, liveData: bool = True):
    """Configure the platform and add the Gazpar sensor."""

    _LOGGER.debug("Initializing Gazpar platform...")

    try:
        username = config[CONF_USERNAME]
        password = config[CONF_PASSWORD]
        webdriver = config[CONF_WEBDRIVER]
        wait_time = config[CONF_WAITTIME]
        tmpdir = config[CONF_TMPDIR]
        scan_interval = config[CONF_SCAN_INTERVAL]

        account = GazparAccount(hass, username, password, webdriver, wait_time, tmpdir, scan_interval, liveData)
        add_entities(account.sensors, True)
        _LOGGER.debug("Gazpar platform initialization has completed successfully")
    except BaseException:
        _LOGGER.error("Gazpar platform initialization has failed with exception : %s", traceback.format_exc())
        raise


# --------------------------------------------------------------------------------------------
class GazparAccount:
    """Representation of a Gazpar account."""

    # ----------------------------------
    def __init__(self, hass, username, password, webdriver, wait_time, tmpdir, scan_interval, liveData: bool):
        """Initialise the Gazpar account."""
        self._username = username
        self._password = password
        self._webdriver = webdriver
        self._wait_time = wait_time
        self._tmpdir = tmpdir
        self._scan_interval = scan_interval
        self._dataByFrequency = {}
        self.sensors = []

        if hass is not None:
            call_later(hass, 5, self.update_gazpar_data, hass)

        self.sensors.append(
            GazparSensor(HA_LAST_PERIOD_START_TIME, PropertyName.DATE.value, None, BEFORE_LAST_INDEX, Frequency.DAILY, self))
        self.sensors.append(
            GazparSensor(HA_LAST_PERIOD_END_TIME, PropertyName.DATE.value, None, LAST_INDEX, Frequency.DAILY, self))
        self.sensors.append(
            GazparSensor(HA_LAST_START_INDEX, PropertyName.START_INDEX_M3.value, HA_VOLUME_M3, LAST_INDEX, Frequency.DAILY, self))
        self.sensors.append(
            GazparSensor(HA_LAST_END_INDEX, PropertyName.END_INDEX_M3.value, HA_VOLUME_M3, LAST_INDEX, Frequency.DAILY, self))
        self.sensors.append(
            GazparSensor(HA_LAST_VOLUME_M3, PropertyName.VOLUME_M3.value, HA_VOLUME_M3, LAST_INDEX, Frequency.DAILY, self))
        self.sensors.append(
            GazparSensor(HA_LAST_ENERGY_KWH, PropertyName.ENERGY_KWH.value, ENERGY_KILO_WATT_HOUR, LAST_INDEX, Frequency.DAILY, self))
        self.sensors.append(
            GazparSensor(HA_LAST_CONVERTER_FACTOR, PropertyName.CONVERTER_FACTOR.value, HA_CONVERTOR_FACTOR_KWH_M3, LAST_INDEX, Frequency.DAILY, self))
        self.sensors.append(
            GazparSensor(HA_LAST_TEMPERATURE, PropertyName.LOCAL_TEMPERATURE.value, TEMP_CELSIUS, LAST_INDEX, Frequency.DAILY, self))

        for frequency in Frequency:
            self.sensors.append(
                GazparSensor(HA_LAST_ENERGY_KWH_BY_FREQUENCY[frequency], PropertyName.ENERGY_KWH.value, ENERGY_KILO_WATT_HOUR, LAST_INDEX, frequency, self))

        if hass is not None:
            track_time_interval(hass, self.update_gazpar_data, hass)
        else:
            self.update_gazpar_data(None, liveData)

    # ----------------------------------
    def update_gazpar_data(self, hass, liveData: bool = False):
        """Fetch new state data for the sensor."""

        _LOGGER.debug("Querying PyGazpar library for new data...")

        try:
            for frequency in Frequency:
                if liveData:
                    client = Client(self._username, self._password, self._webdriver, 30, self._tmpdir, 1, True, frequency)
                else:
                    client = DummyClient(1, frequency)
                client.update()
                self._dataByFrequency[frequency] = client.data()
                _LOGGER.debug(f"data[{frequency}]={json.dumps(self._dataByFrequency[frequency], indent=2)}")

            if hass is not None:
                for sensor in self.sensors:
                    sensor.async_schedule_update_ha_state(True)
                    _LOGGER.debug("HA notified that new data is available")
            _LOGGER.debug("New data have been retrieved successfully from PyGazpar library")
        except BaseException:
            _LOGGER.error("Failed to query PyGazpar library with exception : %s", traceback.format_exc())

    # ----------------------------------
    @property
    def username(self):
        """Return the username."""
        return self._username

    # ----------------------------------
    @property
    def webdriver(self):
        """Return the webdriver."""
        return self._webdriver

    # ----------------------------------
    @property
    def tmpdir(self):
        """Return the tmpdir."""
        return self._tmpdir

    # ----------------------------------
    @property
    def dataByFrequency(self):
        """Return the data dictionary by frequency."""
        return self._dataByFrequency


# --------------------------------------------------------------------------------------------
class GazparSensor(Entity):
    """Representation of a sensor entity for Linky."""

    # ----------------------------------
    def __init__(self, name, identifier, unit, index, meterReadingFrequency: Frequency, account: GazparAccount):
        """Initialize the sensor."""
        self._name = name
        self._identifier = identifier
        self._unit = unit
        self._index = index
        self._account = account
        self._username = account.username
        self._meterReadingFrequency = meterReadingFrequency
        self._data = None

    # ----------------------------------
    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    # ----------------------------------
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._data[self._identifier]

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit

    # ----------------------------------
    @property
    def icon(self):
        """Return the icon of the sensor."""
        return ICON_GAS

    # ----------------------------------
    @property
    def device_state_attributes(self):
        """Return the state attributes of the sensor."""

        res = {
            ATTR_ATTRIBUTION: HA_ATTRIBUTION,
            CONF_USERNAME: self._username
        }

        for propertyName in PropertyName:
            res[propertyName] = self._data[propertyName]

        return res

    # ----------------------------------
    def update(self):
        """Retrieve the new data for the sensor."""

        _LOGGER.debug(f"HA requests its {self._meterReadingFrequency} data to be updated...")
        try:
            data = self._account.dataByFrequency.get(self._meterReadingFrequency)

            if data is not None and len(data) > 0:
                self._data = data[self._index]
                _LOGGER.debug(f"HA {self._meterReadingFrequency} data have been updated successfully")
            else:
                _LOGGER.debug(f"No {self._meterReadingFrequency} data available yet for update")
        except BaseException:
            _LOGGER.error(f"Failed to update {self._meterReadingFrequency} HA data with exception : %s", traceback.format_exc())
