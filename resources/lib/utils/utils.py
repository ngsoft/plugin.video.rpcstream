# -*- coding: utf-8 -*-
import base64
import json
from kodi_six import xbmc, xbmcgui
from .constants import ADDON, ADDON_NAME, ADDON_ICON, SETTING_DEBUG, SETTING_NOTIFY
from . import logger
import time
from six import PY2
import codecs


def notify(message=None, header=ADDON_NAME,  time=5000, icon=ADDON_ICON, sound=True):
    if (message != None and SETTING_NOTIFY == True):
        xbmcgui.Dialog().notification(header, message, icon, time, sound)


def get_string(string_id):
    value = ADDON.getLocalizedString(string_id)
    try:
        value = value.encode('utf-8', 'ignore')
    except:
        pass
    return value


def debug(message):
    if SETTING_DEBUG == True:
        logger.warn(text=message, addon_id=ADDON_NAME)


def decode(string, mode='utf-8'):
    try:
        string = codecs.decode(codecs.encode(string), mode)
    except:
        debug('cannot decode %s' % (str(string)))
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
