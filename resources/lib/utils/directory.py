# -*- coding: utf-8 -*-
import sys
from kodi_six import xbmcplugin, xbmcgui


def addItem():
    return


def show():
    return


class Item(object):

   def __init__(self, label=None, icon=None):
        self._label = None
        self._icon = None
        self._listItem = xbmcgui.ListItem(label)
        self.setLabel(label)
        self.setIcon(icon)


    def setLabel(self, label):
        self._label = label
        self._listItem.setLabel(label)

    def setIcon(self, icon):
        self._icon = icon
        if icon != None:
            self._listItem.setArt({'icon': icon})


_handle = int(sys.argv[1])
_items = []
_contents = []
