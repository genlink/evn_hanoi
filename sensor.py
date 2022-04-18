import logging

from . import evnhn
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle, dt

from datetime import datetime, timedelta

_LOGGER = logging.getLogger(__name__)


CONF_MA = "makhach"

ICON = "mdi:transmission-tower"

TIME_BETWEEN_UPDATES = timedelta(minutes=60)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_MA, default='xxx'): cv.string,
    }
)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the sensor platform."""
    makhach = config.get(CONF_MA)
    evnhanoi = EvnHanoiData(evnhn.SensorAttribute(makhach))
    async_add_entities([EvnHanoiSensor(evnhanoi, 'evn_hanoi_grid')], True)

class EvnHanoiData:
    def __init__(self, evnhanoi):
        """Initialize the data object."""
        self.evnhanoi = evnhanoi
    @Throttle(TIME_BETWEEN_UPDATES)
    def update(self):
        """Get the latest data and update the states."""
        self.evnhanoi.get_evnhanoi()


class EvnHanoiSensor(Entity):

    def __init__(self, haversion, name):
        """Initialize the sensor."""
        self.haversion = haversion
        self._name = name
        self._state = None

    def update(self):
        """Get the latest sensor information."""
        self.haversion.update()

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def device_class(self):
        """Return the class of the sensor."""
        return 'energy'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.haversion.evnhanoi.state

    @property
    def extra_state_attributes(self):
        """Return attributes for the sensor."""
        return self.haversion.evnhanoi.attribute

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return ICON

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return 'kWh'

