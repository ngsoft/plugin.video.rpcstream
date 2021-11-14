# -*- coding: utf-8 -*-
import os
from kodi_six import xbmcaddon

ADDON = xbmcaddon.Addon(os.environ.get('ADDON_ID', ''))


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
