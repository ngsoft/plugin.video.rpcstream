
import xbmc
import xbmcaddon
from .constants import ADDON_ID

DEBUG = xbmc.LOGDEBUG
INFO = xbmc.LOGINFO
NOTICE = INFO
WARNING = xbmc.LOGWARNING
ERROR = xbmc.LOGERROR
FATAL = xbmc.LOGFATAL
NONE = xbmc.LOGNONE


def log(text, log_level=WARNING, addon_id=ADDON_ID):
    if not addon_id:
        addon_id = xbmcaddon.Addon().getAddonInfo('id')
    log_line = '[%s] %s' % (addon_id, text)
    xbmc.log(msg=log_line, level=log_level)


def debug(text, addon_id=ADDON_ID):
    log(text, DEBUG, addon_id)


def info(text, addon_id=ADDON_ID):
    log(text, INFO, addon_id)


def notice(text, addon_id=ADDON_ID):
    log(text, NOTICE, addon_id)


def warning(text, addon_id=ADDON_ID):
    log(text, WARNING, addon_id)


def error(text, addon_id=ADDON_ID):
    log(text, ERROR, addon_id)
