# -*- coding: utf-8 -*-
import sys
import six
from kodi_six import xbmc, xbmcplugin
from ..constants import *
from ..utils import *
from .item import Item

urllib_parse = six.moves.urllib_parse

if IA_ADDON_EXISTS == True:
    debug('%s is enabled.' % (IA_ADDON))


class VideoItem(Item, object):

    def __init__(self, title=None, path=None, subtitles=None, headers={}):
        Item.__init__(self, title=title, path=path)
        self._subtitles = subtitles
        self._headers = headers
        self._isIA = False

    def addHeader(self, key, value):
        if key != None and value != None:
            self._headers[key] = value

    def setHeaders(self, headers):
        if isinstance(headers, dict) or isinstance(headers, str):
            self._headers = headers

    def getHeaders(self):
        return self._headers

    def getHeaderLine(self):
        if isinstance(self._headers, str):
            return self._headers
        string = ''
        if isinstance(self._headers, dict):
            string = router.get_query_string(self._headers)
        return string

    def setSubtitles(self, subtitles):
        self._subtitles = subtitles

    def setPlot(self, plot):
        self.setInfo('plot', plot)

    def getTitle(self):
        return self._title

    def getPlot(self):
        if 'plot' in self._info:
            return self._info['plot']
        return None

    def getListItem(self):
        if self._title != None:
            self.setInfo('title', self._title)
            if 'plot' not in self._info:
                self.setInfo('plot', self._title)

        li = Item.getListItem(self)
        headers = self.getHeaderLine()
        if self._path != None and len(headers) > 0:
            li.setPath('%s|%s' % (self._path, headers))
        return li

    def getInputStreamAdaptiveListItem(self, manifest_type, mimetype):
        li = self.getListItem()
        if SETTING_IA == True:
            if IA_ADDON_EXISTS == True:
                debug('enabling %s to play %s' % (IA_ADDON, manifest_type))
                li.setProperty(IA_ADDON_TYPE,  IA_ADDON)
                li.setProperty('%s.manifest_type' % (IA_ADDON), manifest_type)
                li.setProperty('%s.mimetype' % (IA_ADDON), mimetype)
                li.setProperty('%s.stream_headers' %
                               (IA_ADDON), self.getHeaderLine())
                self._isIA = True
            else:
                debug('%s not present, functionality disabled.' % (IA_ADDON))
        else:
            debug('%s disabled in settings.' % (IA_ADDON))
        return li

    def playHLS(self):
        li = self.getInputStreamAdaptiveListItem(
            'hls', 'application/vnd.apple.mpegurl')
        if self._isIA == True:
            li.setProperty('%s.minversion' % (IA_ADDON), IA_HLS_MIN_VER)
        return self.play()

    def playDash(self):
        li = self.getInputStreamAdaptiveListItem(
            'mpd', 'application/dash+xml')
        if self._isIA == True:
            li.setProperty('%s.minversion' % (IA_ADDON), IA_MPD_MIN_VER)
        return self.play()

    def play(self):
        li = self.getListItem()
        li.setProperty('IsPlayable', 'true')
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)
        waitresult = waitForPlayback(10)
        if waitresult == False:
            if self._isIA == True:
                debug('playback timeout, disabling %s' % (IA_ADDON))
                li.setProperty(IA_ADDON_TYPE, '')
                self._isIA = False
                xbmc.Player().play(self._path, li)
                waitresult = waitForPlayback(10)
            if waitresult == False:
                debug('playback timeout, removing headers')
                li.setPath(self._path)
                xbmc.Player().play(self._path, li)
                if not waitForPlayback(10):
                    li.setProperty('IsPlayable', 'false')
                    debug('Cannot play %s: %s' % (self._title, self._path))
                    notify('Cannot play %s' % (self._title))
                    return False

        notify('Playing %s' % (self._title))

        if self._subtitles != None:
            set = False
            contents = subs.download(self._subtitles)
            if contents != None:
                file = subs.save(contents)
                if file != None:
                    set = subs.set(file)

            if set == False:
                debug('Cannot set subtitles %s' % (self._subtitles))
                notify('Cannot load subtitles.')

        return True
