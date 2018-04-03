#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<i@binux.me>
#         http://binux.me
# Created on 2014-07-17 21:06:43

import time
import cx_Oracle

from pyspider.database.base.projectdb import ProjectDB as BaseProjectDB
from pyspider.database.basedb import BaseDB
from .oraclebase import OracleMixin


class ProjectDB(OracleMixin, BaseProjectDB, BaseDB):
    __tablename__ = 'projectdb'

    def __init__(self, host='localhost', port=3306, database='projectdb',
                 user='root', passwd=None):
        self.database_name = database
        self.username = user
        
        tns=cx_Oracle.makedsn(host,port,database)
        self.conn=cx_Oracle.connect(user,passwd,tns)

        #if database not in [x[0] for x in self._execute('show databases')]:
        #    self._execute('CREATE DATABASE %s' % self.escape(database))
        #self.conn.database = database

        self._execute('''CREATE TABLE %s (
            name varchar2(64) PRIMARY KEY,
            "GROUP" varchar2(64),
            status varchar2(16),
            script CLOB,
            comments varchar2(1024),
            rate number(11, 4),
            burst number(11, 4),
            updatetime number(16, 4)
            )''' % self.escape(self.__tablename__))

    def insert(self, name, obj={}):
        obj = dict(obj)
        obj['name'] = name
        obj['updatetime'] = time.time()
        return self._insert(**obj)

    def update(self, name, obj={}, **kwargs):
        obj = dict(obj)
        obj.update(kwargs)
        obj['updatetime'] = time.time()
        ret = self._update(where="name = %s" % self.placeholder, where_values=(name, ), **obj)
        return ret.rowcount

    def get_all(self, fields=None):
        return self._select2dic(what=fields)

    def get(self, name, fields=None):
        where = "name = %s" % self.placeholder
        for each in self._select2dic(what=fields, where=where, where_values=(name, )):
            return each
        return None

    def drop(self, name):
        where = "name = %s" % self.placeholder
        return self._delete(where=where, where_values=(name, ))

    def check_update(self, timestamp, fields=None):
        where = "updatetime >= %f" % timestamp
        return self._select2dic(what=fields, where=where)
