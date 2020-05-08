import appdaemon.plugins.hass.hassapi as hass
import voluptuous as vol
from datetime import datetime, timedelta

APP_FH = 'count_entities'
APP_CLASS = 'CountEntities'

CONF_MODULE = 'module'
CONF_CLASS = 'class'
CONF_PRIORITY = 'priority'
CONF_INCLUDE = 'include'
CONF_EXCLUDE = 'exclude'
CONF_LOG_LEVEL = 'log_level'
CONF_SCAN_INTERVAL = 'scan_interval'

ATTRIBUTE_FRIENDLY_NAME = 'friendly_name'
ATTRIBUTE_UNIT_OF_MEASUREMENT = 'unit_of_measurement'

# log levels
ERROR = 'ERROR'
DEBUG = 'DEBUG'
INFO = 'INFO'
WARNING = 'WARNING'

FILTER = 'filter'

APP_SCHEMA = vol.Schema({
    vol.Required(CONF_MODULE): APP_FH,
    vol.Required(CONF_CLASS): APP_CLASS,
    vol.Optional(CONF_PRIORITY): vol.Any(float, int),
    vol.Exclusive(CONF_INCLUDE, FILTER): [str],
    vol.Exclusive(CONF_EXCLUDE, FILTER): [str],
    vol.Optional(CONF_LOG_LEVEL, default=DEBUG): vol.Any(DEBUG, INFO),
    vol.Optional(CONF_SCAN_INTERVAL, default=3600): int,
})


class CountEntities(hass.Hass):
    def initialize(self):
        args = APP_SCHEMA(self.args)

        # Set Lazy Logging (to not have to restart appdaemon)
        self._level = args.get(CONF_LOG_LEVEL)
        self.log(args, level=self._level)

        include = args.get(CONF_INCLUDE, [])
        exclude = args.get(CONF_EXCLUDE, [])
        scan_interval = args.get(CONF_SCAN_INTERVAL)

        if include:
            self.get_domains(include)
        elif exclude:
            self.get_domains(exclude, False)
        else:
            self.get_domains()

        self.log(f"Tracking {len(self._track)} domains.", level = self._level)
        t = datetime.now() + timedelta(seconds=scan_interval)
        self.run_every(self.update_sensors, t, scan_interval)

    def get_domains(self, filtered=None, include=True):
        self._track = {}
        for entity_id in self.get_state().keys():
            domain = entity_id.split('.')[0]

            if domain not in self._track:
                sensor = None
                if filtered and domain in filtered and include:
                    sensor = AppDomain(domain)
                    filtered.pop(filtered.index(domain))
                elif filtered and domain not in filtered and not include:
                    sensor = AppDomain(domain)
                elif filtered is None:
                    sensor = AppDomain(domain)

                if sensor is not None:
                    self.log(f"counting entities in '{sensor.domain}' domain.", level = self._level)
                    self.update_sensor(sensor)
                    self._track[sensor.domain] = sensor

        if filtered and include:
            for domain in filtered:
                self.log(f"'{domain}' domain does not exist in Home Assistant", level = WARNING)

    def update_sensor(self, sensor):
        sensor.state = len(self.get_state(sensor.domain))
        self.log(f"updating {sensor.entity_id} state to {sensor.state}.", level = self._level)
        self.set_state(sensor.entity_id, state=sensor.state, attributes=sensor.attributes)

    def update_sensors(self, kwargs):
        for sensor in self._track.values():
            self.update_sensor(sensor)
            

class AppDomain(object):
    def __init__(self, domain):
        self.domain = domain
        self.name = domain.replace('_', ' ').title() + 's'
        self._count = 0
        self.entity_id = f'sensor.entity_counter_{domain}'

    @property
    def state(self):
        return str(self._count)

    @state.setter
    def state(self, value):
        self._count = value

    @property
    def attributes(self):
        return {
            ATTRIBUTE_FRIENDLY_NAME: self.name,
            ATTRIBUTE_UNIT_OF_MEASUREMENT: 'entities'
        }