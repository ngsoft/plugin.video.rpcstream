# -*- coding: utf-8 -*-
import sys
from kodi_six import xbmcplugin

from .item import Item
from ..utils import debug


class Directory(object):

    def __init__(self, content=None, sort=False):
        self._content = content
        self._sort = bool(sort)
        self._items = []
        self._handle = int(sys.argv[1])
        self._displayed = False

    def getContent(self):
        return self._content

    def getItems(self):
        return self._items

    def setContent(self, content):
        if isinstance(content, str):
            self._content = content

    def addItem(self, item):
        if isinstance(item, Item):
            self._items.append(item)

    def render(self):
        if self._displayed == True:
            return
        total = len(self._items)
        if total < 1:
            debug('Cannot render directory, no items.')
            return

        if isinstance(self._content, str):
            xbmcplugin.setContent(self._handle, self._content)

        if self._sort == True:
            xbmcplugin.addSortMethod(
                self._handle, xbmcplugin.SORT_METHOD_TITLE)
            xbmcplugin.addSortMethod(
                self._handle, xbmcplugin.SORT_METHOD_VIDEO_YEAR)
            xbmcplugin.addSortMethod(
                self._handle, xbmcplugin.SORT_METHOD_DATEADDED)

        for item in self._items:
            xbmcplugin.addDirectoryItem(
                self._handle, item.getPath(), item.getListItem(), True, total)
        self._displayed = True
        xbmcplugin.endOfDirectory(self._handle)
