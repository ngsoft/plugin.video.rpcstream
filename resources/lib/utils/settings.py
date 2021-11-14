# -*- coding: utf-8 -*-

from .constants import ADDON

from . import logger


def show_settings():
    ADDON.openSettings()


def get_setting(name):
    value = ADDON.getSetting(name).strip()
    try:
        value = value.decode('utf-8')
    except:
        pass
    return value


def set_setting(name, value):
    ADDON.setSetting(name, str(value))


def get_setting_as_bool(setting):
    return get_setting(setting).lower() == "true"


def get_setting_as_float(setting):
    try:
        return float(get_setting(setting))
    except ValueError:
        return 0


def get_setting_as_int(setting):
    try:
        return int(get_setting_as_float(setting))
    except ValueError:
        return 0


# <setting id="rpcstream.notify" type="bool" label="Enable Notifications" default="true"/>
SETTING_NOTIFY = get_setting_as_bool('rpcstream.notify')
# <setting id="rpcstream.ia" type="bool" label="Use InputStream Adaptive if available" default="true"/>
SETTING_IA = get_setting_as_bool('rpcstream.ia')
# <setting id="rpcstream.debug" type="bool" label="Debug Mode" default="false"/>
SETTING_DEBUG = get_setting_as_bool('rpcstream.debug')


logger.warn('notify %s' % (SETTING_NOTIFY))
logger.warn('ia %s' % (SETTING_IA))
logger.warn('debug %s' % (SETTING_DEBUG))
