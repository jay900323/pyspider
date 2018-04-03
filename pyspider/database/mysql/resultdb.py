#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<i@binux.me>
#         http://binux.me
# Created on 2014-10-13 22:02:57

import re
import six
import time
import json
import copy
import mysql.connector

from pyspider.libs import utils
from pyspider.database.base.resultdb import ResultDB as BaseResultDB
from pyspider.database.basedb import BaseDB
from .mysqlbase import MySQLMixin, SplitTableMixin


class ResultDB(MySQLMixin, SplitTableMixin, BaseResultDB, BaseDB):
    __tablename__ = ''

    def __init__(self, host='localhost', port=3306, database='resultdb',
                 user='root', passwd=None):
        self.database_name = database
        self.conn = mysql.connector.connect(user=user, password=passwd,
                                            host=host, port=port, autocommit=True)
        if database not in [x[0] for x in self._execute('show databases')]:
            self._execute('CREATE DATABASE %s' % self.escape(database))
        self.conn.database = database
        self._list_project()

    def _create_project(self, project, key, items):
        assert re.match(r'^\w+$', project) is not None
        tablename = self._tablename(project)
        if tablename in [x[0] for x in self._execute('show tables')]:
            return
        #`result` MEDIUMBLOB,
        columns = ''
        #items.extend(['taskid', 'url', 'updatetime'])
        for column, value in  items.items():
            if column in ['taskid', 'url', 'updatetime']:
                continue
            value_type = value[1] if isinstance(value, list) else 'TEXT'
            if column == key:
                columns+= '`{0}` {1} PRIMARY KEY, '.format(column, value_type)
            else:
                columns += '`{0}` {1}, '.format(column, value_type)
        print columns
        if key and key not in ['taskid', 'url']:
            self._execute('''CREATE TABLE %s (
                `taskid` varchar(64),
                `url` varchar(1024),
                %s
                `updatetime` double(16, 4)
                ) ENGINE=InnoDB CHARSET=utf8''' % (self.escape(tablename), columns))
        else:
            self._execute('''CREATE TABLE %s (
                `suid` varchar(64) PRIMARY KEY,
                `taskid` varchar(64) ,
                `url` varchar(1024),
                %s
                `updatetime` double(16, 4)
                ) ENGINE=InnoDB CHARSET=utf8''' % (self.escape(tablename), columns))
            
    def _parse(self, data):
        for key, value in list(six.iteritems(data)):
            if isinstance(value, (bytearray, six.binary_type)):
                data[key] = utils.text(value)
        if 'result' in data:
            data['result'] = json.loads(data['result'])
        return data

    def _stringify(self, data):
        if 'result' in data:
            data['result'] = json.dumps(data['result'])
        return data

    def save(self, project, taskid, url, result, capture_phase):
        tablename = self._tablename(project)
        #result[0] is primary key result[1] is the dictionary
        key = result[0]
        items = result[1]
        if project not in self.projects:
            self._create_project(project, key, items)
            self._list_project()
        obj = None
        obj_result = result[1]
        if key and key not in ['taskid', 'url']:
            obj = {
                key: str(obj_result[key][0] if isinstance(obj_result[key], list) else obj_result[key]),
                'taskid': taskid,
                'url': url,
                'updatetime': time.time(),
            }
            obj_result.update(obj)
            key_value = obj_result[key]
        else:
            obj = {
                'taskid': taskid,
                'url': url,
                'updatetime': time.time(),
            }
            suid = ''
            for k in obj_result.keys():
                suid += str(obj_result[k][0] if isinstance(obj_result[k], list) else obj_result[k])
            suid = utils.md5string(suid)
            obj_result.update(obj)
            obj_result['suid'] = suid
            key_value = suid
            key = 'suid'
            
        for o in obj_result.keys():
            if obj_result[o] == None:
                obj_result[o] = ''
            else:
                obj_result[o] = str(obj_result[o][0] if isinstance(obj_result[o], list) else obj_result[o] )
        try:
            obj_result_copy = copy.deepcopy(obj_result)
            del obj_result_copy['updatetime']
            
            fields = tuple(obj_result_copy.keys())
            tasks = self.get(project, key, key_value, fields)
            if tasks:
                print 'cunzai   ', obj_result_copy

                where = "%s = %s" % (self.escape(key), self.placeholder)
                where_values=[obj_result_copy[key]]
                return self._update(tablename, where=where, where_values=[obj_result_copy[key]], **self._stringify(obj_result_copy))
            else:
                print '不存在', obj_result
                return self._replace(tablename, **self._stringify(obj_result))
        except Exception, e:
            print str(e)
            
    def select(self, project, fields=None, offset=0, limit=None):
        if project not in self.projects:
            self._list_project()
        if project not in self.projects:
            return
        tablename = self._tablename(project)

        for task in self._select2dic(tablename, what=fields, order='updatetime DESC',
                                     offset=offset, limit=limit):
            yield self._parse(task)

    def count(self, project):
        if project not in self.projects:
            self._list_project()
        if project not in self.projects:
            return 0
        tablename = self._tablename(project)
        for count, in self._execute("SELECT count(1) FROM %s" % self.escape(tablename)):
            return count

    def get(self, project, key, key_value, fields=None):
        if project not in self.projects:
            self._list_project()
        if project not in self.projects:
            return
        tablename = self._tablename(project)
        where = "`%s` = %s" % (key, self.placeholder)
        for task in self._select2dic(tablename, what=fields,
                                     where=where, where_values=(key_value, )):
            return self._parse(task)
