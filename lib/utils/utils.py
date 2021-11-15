# -*- coding: utf-8 -*-
import base64
import json
from kodi_six import xbmc, xbmcgui
from ..constants import ADDON, ADDON_NAME, ADDON_ICON, SETTING_DEBUG, SETTING_NOTIFY
from . import logger
import time


def alert(message, title=ADDON_NAME):
    return xbmcgui.Dialog().ok(title, message)


def confirm(question, title=ADDON_NAME):
    return xbmcgui.Dialog().yesno(title, question)


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


def refresh_ui():
    xbmc.executebuiltin('Container.Refresh')


def debug(message):
    if SETTING_DEBUG == True:
        logger.warn(text=message)


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
