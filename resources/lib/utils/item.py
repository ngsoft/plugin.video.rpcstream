# -*- coding: utf-8 -*-
from kodi_six import xbmcgui, xbmc, xbmcplugin
from six.moves import urllib_parse
from .constants import *
from .router import handle
from utils import *
import time
from . import subs


IA_ADDON_EXISTS = False

# checks if IA Addon exists
try:
    xbmcaddon.Addon(id=IA_ADDON)
    IA_ADDON_EXISTS = True
except:
    pass

# On leia using testing if available
if KODI_VERSION == 18:
    try:
        xbmcaddon.Addon(id=IA_TESTING_ID)
        IA_ADDON = IA_TESTING_ID
        IA_ADDON_EXISTS = True
    except:
        pass


class Item(object):

    def __init__(self, title=None, plot=None, url=None, subtitles=None, image='', fanart='', headers={}):
        self._listItem = xbmcgui.ListItem(offscreen=True)
        self._title = title
        self._plot = plot
        self._url = url
        self._subtitles = subtitles
        self._image = image
        self._fanart = fanart
        self._headers = headers
        self._isIA = False

    def setHeader(self, key, value):
        if key != None and value != None:
            self._headers[key] = value

    def getHeaders(self):
        return self._headers

    def getHeaderLine(self):
        string = ''
        for key in self._headers:
            value = self._headers[key]
            string += '%s=%s&' % (key, urllib_parse.quote_plus(value))
        return string.strip('&')

    def setSubtitles(self, subtitles):
        self._subtitles = subtitles

    def setTitle(self, title):
        self._title = title

    def setPlot(self, plot):
        self._plot = plot

    def setUrl(self, url):
        self._url = url

    def setImage(self, image):
        self._image = image

    def setFanart(self, fanart):
        self._fanart = fanart

    def getTitle(self):
        return self._title

    def getPlot(self):
        return self._plot

    def getUrl(self):
        return self._url

    def getImage(self):
        return self._image

    def getFanart(self):
        return self._fanart

    def getListItem(self):
        li = self._listItem
        title = self._title if self._title != None else ''
        plot = self._plot if self._plot != None else title
        headers = self.getHeaderLine()
        if self._url != None:
            url = '%s|%s' % (self._url, headers) if len(
                headers) > 0 else self._url
        li.setPath(url)
        li.setLabel(self._title)
        li.setInfo('video', {'title': title, 'plot': plot})
        li.setArt({'icon': self._image, 'thumb': self._image,
                  'fanart': self._fanart})

        return li

    def getInputStreamAdaptiveListItem(self, manifest_type, mimetype):
        li = self.getListItem()
        if IA_ADDON_EXISTS == True:
            li.setProperty(IA_ADDON_TYPE,  IA_ADDON)
            li.setProperty('%s.manifest_type' % (IA_ADDON), manifest_type)
            li.setProperty('%s.mimetype' % (IA_ADDON), mimetype)
            li.setProperty('%s.stream_headers' %
                           (IA_ADDON), self.getHeaderLine())
            self._isIA = True
        else:
            log('%s not present, functionality disabled.' % (IA_ADDON))
        return li

    def playHLS(self, notif=False):
        li = self.getInputStreamAdaptiveListItem(
            'hls', 'application/vnd.apple.mpegurl')
        if self._isIA == True:
            li.setProperty('%s.minversion' % (IA_ADDON), IA_HLS_MIN_VER)
        return self.play(notif)

    def playDash(self, notif=False):
        li = self.getInputStreamAdaptiveListItem(
            'mpd', 'application/dash+xml')
        if self._isIA == True:
            li.setProperty('%s.minversion' % (IA_ADDON), IA_MPD_MIN_VER)
        return self.play(notif)

    def play(self, notif=False):
        li = self.getListItem()
        li.setProperty('IsPlayable', 'true')
        xbmcplugin.setResolvedUrl(handle, True, li)

        if not waitForPlayback(10):
            li.setPath(self._url)
            if self._isIA == True:
                li.setProperty(IA_ADDON_TYPE, '')
                self._isIA = False
            xbmc.Player().play(self._url, li)
            if not waitForPlayback(10):
                li.setProperty('IsPlayable', 'false')
                log('Cannot play %s: %s' % (self._title, self._url))
                if notif == True:
                    notify('Cannot play %s' % (self._title))
            return False
        if notif == True:
            notify('Playing %s' % (self._title))

        if self._subtitles != None:
            set = False
            contents = subs.download(self._subtitles)
            if contents != None:
                file = subs.save(contents)
                if file != None:
                    set = subs.set(file)

            if set == False:
                log('Cannot set subtitles %s' % (self._subtitles))
                if notif == True:
                    notify('Cannot load subtitles.')

        return True
