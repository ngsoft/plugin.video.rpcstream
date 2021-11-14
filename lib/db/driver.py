# -*- coding: utf-8 -*-
import os
import sqlite3
from ..constants import ADDON_PATH


class SQLiteDataBase(object):

    def __init__(self, dbname='db'):
        self._connection = None
        self._db = os.path.join(ADDON_PATH, 'resources/data/%s.db' % (dbname))

    def connect(self):
        if self._connection is None:
            self._connection = sqlite3.connect(self._db)

    def close(self):
        if self._connection is not None:
            self._connection.commit()
            self._connection.close()
            self._connection = None

    def execQuery(self, query, bindings=None):
        if bindings == None:
            return self.getConnection().execute(query)
        return self.getConnection().execute(query, bindings)

    def fetchMany(self, query, bindings=None, size=1):
        cursor = self.execQuery(query, bindings)
        return cursor.fetchmany(size)

    def fetchAll(self, query, bindings=None):
        cursor = self.execQuery(query, bindings)
        return cursor.fetchall()

    def fetchOne(self, query, bindings=None):
        cursor = self.execQuery(query, bindings)
        return cursor.fetchone()

    def getConnection(self):
        self.connect()
        return self._connection
