# -*- coding: utf-8 -*-

from kodi_six import xbmc
from six.moves import urllib_request, urllib_parse
from .constants import USER_AGENT, ADDON_ID
from .utils import waitForPlayback, debug
import time


def download(url, headers={'User-Agent': USER_AGENT}):
    if url != None:
        try:
            debug('downloading subtitle %s' % (url))
            req = urllib_request.Request(url)
            for key in headers:
                req.add_header(key, headers[key])
            response = urllib_request.urlopen(req)
            contents = response.read()
            response.close()
            return contents
        except:
            pass
    return None


def save(contents=None, filename='%s.srt' % (ADDON_ID)):
    if contents != None:
        try:
            path = xbmc.translatePath('special://temp/%s' % (filename))
            debug('saving subtitle %s' % (path))
            with open(path, 'wb') as subfile:
                subfile.write(contents)
                subfile.close()
            return path

        except:
            pass
    return None


def set(file=None, timeout=30):
    if file != None:
        if waitForPlayback(10):
            timer = time.time() + timeout
            while not xbmc.Player().isPlaying():
                xbmc.sleep(1000)
                if time.time() > timer:
                    return False
            xbmc.Player().setSubtitles(file)
            return True
    return False
