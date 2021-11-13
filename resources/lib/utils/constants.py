import os
from kodi_six import xbmc, xbmcaddon

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


##### IA #####
IA_ADDON_TYPE = 'inputstream'
IA_ADDON = 'inputstream.adaptive'
IA_VERSION_KEY = '_version'
IA_HLS_MIN_VER = '2.0.0'
IA_PR_MIN_VER = '2.2.19'
IA_MPD_MIN_VER = '2.2.19'
IA_WV_MIN_VER = '2.2.27'

if KODI_VERSION < 19:
    IA_ADDON_TYPE = 'inputstreamaddon'
    IA_ADDON = 'inputstream.adaptive.testing'
