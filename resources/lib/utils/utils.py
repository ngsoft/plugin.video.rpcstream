# -*- coding: utf-8 -*-
import base64
import json
from kodi_six import xbmc
from .constants import ADDON, ADDON_NAME, ADDON_ICON
from . import logger
import time

from kodi_six import xbmcgui


def notify(message=None, header=ADDON_NAME,  time=5000, icon=ADDON_ICON, sound=True):
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
    logger.warn(text=message, addon_id=ADDON_NAME)


def decode(string, mode='utf8'):
    try:
        string = str.decode(mode)
    except:
        pass
    return string


def waitForPlayback(timeout=30):
    timer = time.time() + timeout
    while not xbmc.getCondVisibility("Player.HasMedia"):
        xbmc.sleep(50)
        if time.time() > timer:
            return False
    return xbmc.getCondVisibility("Player.HasMedia")


def b64load(string=None):

    if string != None:
        try:
            decoded = base64.b64decode(string)
            result = json.loads(decoded)
            return result
        except:
            pass
    return None
