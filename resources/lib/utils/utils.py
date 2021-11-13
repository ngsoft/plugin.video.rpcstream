from .constants import *
import logger

from kodi_six import xbmc, xbmcaddon, xbmcgui


def notify(message=None, header=ADDON_NAME,  time=5000, icon=ADDON.getAddonInfo('icon'), sound=True):
    if (message != None):
        xbmcgui.Dialog().notification(header, message, icon, time, sound)


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


def get_string(string_id):
    value = ADDON.getLocalizedString(string_id)
    try:
        value = value.encode('utf-8', 'ignore')
    except:
        pass
    return value


def log(message):
    logger.warn(text=message)
