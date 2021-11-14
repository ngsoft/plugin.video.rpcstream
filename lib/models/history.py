# -*- coding: utf-8 -*-

from ..db import *
from ..constants import SETTING_HISTORY


class History(SQLiteDataBase, object):

    def __init__(self):
        SQLiteDataBase.__init__(self, 'history')
        self._max = SETTING_HISTORY
        self._enabled = self._max > 0
        self.create()

    def close(self):
        if self._connection != None:
            self.clean()
            SQLiteDataBase.close(self)

    def create(self):
        self.execQuery(
            'CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, path TEXT)')

    def clean(self):
        result = self.fetchOne('SELECT id FROM history ORDER BY id DESC LIMIT ? OFFSET ?', [
                               self._max, self._max])
        if result != None:
            (id) = result
            if int(id) > 0:
                self.execQuery('DELETE FROM history WHERE id < ?', [id])

    def clear(self):
        if self._enabled:
            self.execQuery('DROP TABLE IF EXISTS history')

    def add(self, title, path):
        if self._enabled:
            result = self.execQuery(
                'INSERT INTO history (title, path) VALUES (?, ?)', [title, path])
            return result.lastrowid

    def has(self, path):
        if self._enabled:
            result = self.fetchOne(
                'SELECT id FROM history WHERE path = ?', [path])
            if result == None:
                return False
            return True
        return False

    def delete(self, id):
        if self._enabled:
            self.execQuery('DELETE FROM history WHERE id = ?', [id])

    def getIterator(self):
        if self._enabled:
            for (id, title, path) in self.fetchMany('SELECT id, title, path FROM history ORDER BY id DESC', max=self._max):
                yield id, title, path
