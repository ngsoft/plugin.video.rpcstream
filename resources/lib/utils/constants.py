# -*- coding: utf-8 -*-
import os
from kodi_six import xbmc, xbmcaddon
from . import settings

##### ADDON ####
ADDON = xbmcaddon.Addon(os.environ.get('ADDON_ID', ''))
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_VERSION = ADDON.getAddonInfo('version')
ADDON_NAME = ADDON.getAddonInfo('name')
ADDON_PATH = xbmc.translatePath(ADDON.getAddonInfo('path'))
ADDON_PROFILE = xbmc.translatePath(ADDON.getAddonInfo('profile'))
ADDON_ICON = ADDON.getAddonInfo('icon')
ADDON_FANART = ADDON.getAddonInfo('fanart')
ADDON_DEV = bool(int(os.environ.get('ADDON_DEV', '0')))

##### Kodi #####
try:
    KODI_VERSION = int(xbmc.getInfoLabel("System.BuildVersion").split('.')[0])
except:
    KODI_VERSION = 16

##### INPUTSTREAM ADAPTIVE #####
IA_ADDON_TYPE = 'inputstream'
IA_ADDON = 'inputstream.adaptive'
IA_TESTING_ID = 'inputstream.adaptive.testing'
IA_VERSION_KEY = '_version'
IA_HLS_MIN_VER = '2.0.0'
IA_PR_MIN_VER = '2.2.19'
IA_MPD_MIN_VER = '2.2.19'
IA_WV_MIN_VER = '2.2.27'

if KODI_VERSION < 19:
    IA_ADDON_TYPE = 'inputstreamaddon'

    #IA_ADDON = IA_TESTING_ID


USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'

##### ADDON SPECIFICS #####

PLAY_MODE_DEFAULT = 0
PLAY_MODE_DASH = 1
PLAY_MODE_HLS = 2


##### SETTINGS #####

# <setting id="rpcstream.notify" type="bool" label="Enable Notifications" default="true"/>
SETTING_NOTIFY = settings.get_setting_as_bool('rpcstream.notify')
# <setting id="rpcstream.ia" type="bool" label="Use InputStream Adaptive if available" default="true"/>
SETTING_IA = settings.get_setting_as_bool('rpcstream.ia')
# <setting id="rpcstream.debug" type="bool" label="Debug Mode" default="false"/>
SETTING_DEBUG = settings.get_setting_as_bool('rpcstream.debug')
# <setting id="rpcstream.history" label="History Size" type="slider" default="50" range="0,10,500" option="int"/>
SETTING_HISTORY = settings.get_setting_as_int('rpcstream.history')
