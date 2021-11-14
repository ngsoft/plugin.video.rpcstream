
# -*- coding: utf-8 -*-

from kodi_six import xbmc
from .constants import ADDON_ID

DEBUG = xbmc.LOGDEBUG
INFO = xbmc.LOGINFO
NOTICE = INFO
WARNING = xbmc.LOGWARNING
ERROR = xbmc.LOGERROR
FATAL = xbmc.LOGFATAL
NONE = xbmc.LOGNONE


def log(text, log_level=DEBUG, addon_id=ADDON_ID):
    log_line = '[' + str(addon_id) + '] ' + str(text)
    xbmc.log(msg=log_line, level=log_level)


def debug(text, addon_id=ADDON_ID):
    log(text, DEBUG, addon_id)


def info(text, addon_id=ADDON_ID):
    log(text, INFO, addon_id)


def notice(text, addon_id=ADDON_ID):
    log(text, NOTICE, addon_id)


def warn(text, addon_id=ADDON_ID):
    log(text, WARNING, addon_id)


def error(text, addon_id=ADDON_ID):
    log(text, ERROR, addon_id)
