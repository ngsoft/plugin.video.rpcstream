# -*- coding: utf-8 -*-

from .utils import debug, alert, confirm, notify, b64load, waitForPlayback, isPlaying, get_string, refresh_ui
from .settings import show_settings, get_setting, get_setting, get_setting_as_bool, get_setting_as_float, get_setting_as_int

from . import router, logger, subs

getLocalizedString = get_string

__all__ = [
    'debug', 'alert', 'confirm', 'notify', 'b64load', 'waitForPlayback', 'isPlaying', 'getLocalizedString', 'refresh_ui',
    'show_settings',  'get_setting', 'get_setting_as_bool', 'get_setting_as_float', 'get_setting_as_int',
    'router', 'logger', 'subs'
]
