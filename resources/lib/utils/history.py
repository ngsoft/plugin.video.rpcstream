# -*- coding: utf-8 -*-


from .db import SQLiteDataBase
from .constants import SETTING_HISTORY


class History(SQLiteDataBase, object):

    def __init__(self):
        SQLiteDataBase.__init__(self, 'history')
        self._enabled = SETTING_HISTORY > 0
        self._max = SETTING_HISTORY
        self.create()
        self.cleanUP()

    def create(self):
        self.execQuery(
            'CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, path TEXT)')

    def cleanUP(self):
        ids = self.fetchAll('SELECT id FROM history ORDER BY id DESC')
        cnt = 0
        if len(ids) > self._max:
            for id in ids:
                cnt += 1
                if cnt > self._max:
                    self.delete(id)

    def clear(self):
        if self._enabled:
            self.execQuery('DROP TABLE IF EXISTS history')

    def add(self, title, path):
        if self._enabled:
            self.execQuery(
                'INSERT INTO history (title, path) VALUES (?, ?)', (title, path))

    def has(self, path):
        if self._enabled:
            result = self.fetchOne(
                'SELECT id FROM history WHERE path = ?', (path))
            if result == None:
                return False
            return True
        return False

    def delete(self, id):
        if self._enabled:
            self.execQuery('DELETE FROM history WHERE id = ?', (id))

    def get(self):
        if self._enabled:
            for (id, title, path) in self.fetchMany('SELECT * FROM history ORDER BY id DESC', max=self._max):
                yield id, title, path
