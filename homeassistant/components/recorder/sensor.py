"""Platform to retrieve statistics from the recorder for Home Assistant."""
import logging

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME, CONF_UNIT_OF_MEASUREMENT
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
import homeassistant.util.dt as dt_util
from .const import DATA_INSTANCE

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "recorder_queue"

ICON = "mdi:counter"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string
    }
)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the recorder statistics sensor platform."""
    name = config.get(CONF_NAME)

    async_add_entities([RecorderStatisticsSensor(name, hass)], True)


class RecorderStatisticsSensor(Entity):
    """Representation of recorder statistics."""

    def __init__(self, name, hass):
        """Initialize the recorder statistics sensor."""
        self._name = name
        self.initial = 0
        self._state = None
        self._hass = hass

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def icon(self):
        """Icon to display in the front end."""
        return ICON

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement the value is expressed in."""
        return "events"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    async def async_update(self):
        """Update the state of the sensor."""
        recorder_instance = self._hass.data[DATA_INSTANCE]
        qsize = recorder_instance.queue.qsize()
        self._state = qsize
        _LOGGER.debug("New value: %s", self._state)
