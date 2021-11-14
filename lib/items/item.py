# -*- coding: utf-8 -*-

from kodi_six import xbmcplugin, xbmcgui
from ..icons import ICON_ADDON

# info labels
# genre 	string (Comedy) or list of strings (["Comedy", "Animation", "Drama"])
# country 	string (Germany) or list of strings (["Germany", "Italy", "France"])
# year 	integer (2009)
# episode 	integer (4)
# season 	integer (1)
# sortepisode 	integer (4)
# sortseason 	integer (1)
# episodeguide 	string (Episode guide)
# showlink 	string (Battlestar Galactica) or list of strings (["Battlestar Galactica", "Caprica"])
# top250 	integer (192)
# setid 	integer (14)
# tracknumber 	integer (3)
# rating 	float (6.4) - range is 0..10
# userrating 	integer (9) - range is 1..10 (0 to reset)
# watched 	deprecated - use playcount instead
# playcount 	integer (2) - number of times this item has been played
# overlay 	integer (2) - range is 0..7. See Overlay icon types for values
# cast 	list (["Michal C. Hall","Jennifer Carpenter"]) - if provided a list of tuples cast will be interpreted as castandrole
# castandrole 	list of tuples ([("Michael C. Hall","Dexter"),("Jennifer Carpenter","Debra")])
# director 	string (Dagur Kari) or list of strings (["Dagur Kari", "Quentin Tarantino", "Chrstopher Nolan"])
# mpaa 	string (PG-13)
# plot 	string (Long Description)
# plotoutline 	string (Short Description)
# title 	string (Big Fan)
# originaltitle 	string (Big Fan)
# sorttitle 	string (Big Fan)
# duration 	integer (245) - duration in seconds
# studio 	string (Warner Bros.) or list of strings (["Warner Bros.", "Disney", "Paramount"])
# tagline 	string (An awesome movie) - short description of movie
# writer 	string (Robert D. Siegel) or list of strings (["Robert D. Siegel", "Jonathan Nolan", "J.K. Rowling"])
# tvshowtitle 	string (Heroes)
# premiered 	string (2005-03-04)
# status 	string (Continuing) - status of a TVshow
# set 	string (Batman Collection) - name of the collection
# setoverview 	string (All Batman movies) - overview of the collection
# tag 	string (cult) or list of strings (["cult", "documentary", "best movies"]) - movie tag
# imdbnumber 	string (tt0110293) - IMDb code
# code 	string (101) - Production code
# aired 	string (2008-12-07)
# credits 	string (Andy Kaufman) or list of strings (["Dagur Kari", "Quentin Tarantino", "Chrstopher Nolan"]) - writing credits
# lastplayed 	string (Y-m-d h:m:s = 2009-04-05 23:16:04)
# album 	string (The Joshua Tree)
# artist 	list (['U2'])
# votes 	string (12345 votes)
# path 	string (/home/user/movie.avi)
# trailer 	string (/home/user/trailer.avi)
# dateadded 	string (Y-m-d h:m:s = 2009-04-05 23:16:04)
# mediatype 	string - "video", "movie", "tvshow", "season", "episode" or "musicvideo"


class Item(object):

    def __init__(self, title=None, path=None, icon='', isDir=False):

        self._title = title
        self._path = path

        self._icon = icon
        self._poster = ''
        self._fanart = ''
        self._thumb = ''
        self._banner = ''

        self._isDir = bool(isDir)
        self._info = {}
        self._listItem = xbmcgui.ListItem(offscreen=True)

    def setTitle(self, title):
        self._title = title

    def setIcon(self, icon):
        self._icon = icon

    def setPoster(self, poster):
        self._poster = poster

    def setFanart(self, fanart):
        self._fanart = fanart

    def setThumb(self, thumb):
        self._thumb = thumb

    def setBanner(self, banner):
        self._banner = banner

    def setPath(self, path):
        self._path = path

    def setInfo(self, key, value):
        self._info[key] = value

    def getTitle(self):
        return self._label

    def getIcon(self):
        return self._icon

    def getPoster(self):
        return self._poster

    def getFanart(self):
        return self._fanart

    def getThumb(self):
        return self._thumb

    def getBanner(self):
        return self._banner

    def getPath(self):
        return self._path

    def getInfo(self):
        return self._info

    def getIsDir(self):
        return self._isDir

    def getListItem(self):
        li = self._listItem
        li.setLabel(self._title)
        # li.setIsFolder(self._isDir)
        li.setArt({
            'thumb': self._thumb,
            'poster': self._poster,
            'banner': self._banner,
            'fanart': self._fanart,
            'icon': self._icon,
        })
        if len(self._info) > 0:
            li.setInfo('video', self._info)

        li.setPath(self._path)
        return li
