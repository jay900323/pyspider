#coding=utf-8
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<roy@binux.me>
#         http://binux.me
# Created on 2014-12-04 18:48:15

import re
import six
import time
import json
import sqlalchemy.exc
import logging
import copy

from sqlalchemy import (create_engine, MetaData, Table, Column, Integer,
                        String, Float, LargeBinary, CLOB, PrimaryKeyConstraint)
from sqlalchemy.engine.url import make_url
from pyspider.database.base.resultdb import ResultDB as BaseResultDB
from pyspider.libs import utils
from .sqlalchemybase import SplitTableMixin, result2dict
import copy

class ResultDB(SplitTableMixin, BaseResultDB):
    __tablename__ = ''
    placeholder = '%s'
    
    def __init__(self, url):
        self.table = None
        self.tables = {}
        self.url = make_url(url)

        if self.url.database:
            database = self.url.database
            self.url.database = None
            try:
                engine = create_engine(self.url, convert_unicode=True)
                engine.execute("CREATE DATABASE IF NOT EXISTS %s" % database)
            except sqlalchemy.exc.SQLAlchemyError:
                pass
            self.url.database = database
        self.engine = create_engine(url, convert_unicode=True)

        self._list_project()
    
    def get_datatype(self, type):
        if isinstance(type, str):
            if type.startswith('String'):
                vl = type.split('_')
                if len(vl) == 2:
                    length = int(vl[1]) if int(vl[1]) <= 4000 else 4000
                    length =length if length > 0 else 4000
                    return String(length)
            elif type == 'CLOB':
                return CLOB
            elif type == 'Float':
                return Float
            elif type == 'TIMESTAMP': #时间格式为 01-5月-2007 12:51:00
                return TIMESTAMP
            elif type == 'INTEGER':
                return Integer
        return String(4000)
        
    #返回的items数据格式如下
    {'c0':['xxxx', 'SmallString'],
     'c1': ['xxxxx', 'MiddleString'],
     'c1': ['xxxxx', 'BigString'],
     'c3': ['xxxxx', 'CLOB']} 
    def _init_table(self, project, key, items):
        #columns = ''
        #param = copy.copy(items)
        #items.extend(['taskid', 'url', 'updatetime'])
        if key and key not in ['taskid', 'url']:
            self.table = Table('__tablename__', MetaData(),
                               Column(key, String(128), primary_key=True, nullable=False),
                               Column('taskid', String(64), nullable=False),
                               Column('url', String(1024)),
                               Column('updatetime', Float(32)),
                               Column('recently', Integer)
                               )
            for column, value in  items.items():
                if column in ['taskid', 'url', 'updatetime', 'recently', key]:
                    continue
                datatype = self.get_datatype(value[1] if isinstance(value, list) else None)
                self.table.append_column(Column(column, datatype))
            self.table.name = self._tablename(project)
        #如果不知道主键即key为None则根据多个字段的内容来创建主键 blob字段不允许创建主键
        else:
            self.table = Table('__tablename__', MetaData(),
                   Column('suid', String(64), primary_key=True, nullable=False),      
                   Column('taskid', String(64), nullable=False),
                   Column('url', String(1024)),
                   Column('updatetime', Float(32)),
                   Column('recently', Integer)
                   )
            for column, value in  items.items():
                if column in ['taskid', 'url', 'updatetime', 'recently', key]:
                    continue
                datatype = self.get_datatype(value[1] if isinstance(value, list) else None)
                self.table.append_column(Column(column, datatype))
            self.table.name = self._tablename(project)
            
    def _create_project(self, project, key, items):
        assert re.match(r'^\w+$', project) is not None
        if project in self.projects:
            return
        #self.table.name = self._tablename(project)
        #self.table.create(self.engine)

        self._init_table(project, key, items)
        if self.table is not None:
            try:
                self.table.create(self.engine)
            except Exception, e:
                logging.error('create database %s failed, error: %s', (project, e))
                
    @staticmethod
    def _parse(data):
        for key, value in list(six.iteritems(data)):
            if isinstance(value, six.binary_type):
                data[key] = utils.text(value)
        if 'result' in data:
            if isinstance(data['result'], bytearray):
                data['result'] = str(data['result'])
            data['result'] = json.loads(data['result'])
        return data

    @staticmethod
    def _stringify(data):
        if 'result' in data:
            data['result'] = utils.utf8(json.dumps(data['result']))
        return data

    def save(self, project, taskid, url, result, capture_phase):
        key = result[0]
        key_value = None
        items = result[1]
        if project not in self.projects:
            self._create_project(project, key, items)
            self._list_project()
            self.tables[project]= copy.deepcopy(self.table)
            
        #if self.table is None:
        if not self.tables.has_key(project):
            self._init_table(project, key, items)
            self.tables[project]= copy.deepcopy(self.table)
            
        table = self.tables[project]
        table.name = self._tablename(project)
        
        obj_result = result[1]
        if key and key not in ['taskid', 'url']:
            obj = {
                key: result[1][key][0] if isinstance(result[1][key], list) else result[1][key],
                'taskid': taskid,
                'url': url,
                'updatetime': time.time(),
            }
            obj_result.update(obj)
            key_value = result[1][key][0] if isinstance(result[1][key], list) else result[1][key]
        else:
            key = 'suid'
            obj = {
                'taskid': taskid,
                'url': url,
                'updatetime': time.time(),
            }
            #计算suid
            suid = ''
            for k in obj_result.keys():
                suid += str(obj_result[k][0] if isinstance(obj_result[k], list) else obj_result[k])
            suid = utils.md5string(suid)
            
            obj_result.update(obj)
            obj_result['suid'] = suid
            key_value = suid
            
        #将unicode转换成utf-8
        for o in obj_result.keys():
            if obj_result[o] == None:
                obj_result[o] = ''
            else:
                obj_result[o] = str(obj_result[o][0] if isinstance(obj_result[o], list) else obj_result[o] )
        
        obj_result['recently'] = 0
        try:
            obj_result_copy = copy.deepcopy(obj_result)
            del obj_result_copy['updatetime']
            
            fields = tuple(obj_result_copy.keys())
            tasks = self.get(project, key, key_value, fields)
            if tasks:
                need_update = False
                for key in fields:
                    if str(obj_result_copy[key]) != str(tasks[key.upper()]):
                         #need update
                         need_update = True
                column = None
                for x in table.c:
                    if key in str(x):
                        column = x
                if column is not None and need_update:
                    try:
                        sql = table.update().where(column == key_value).values(**self._stringify(obj_result))
                        return self.engine.execute(sql)
                    except Exception, e:
                        logging.error('update data failed. error: %s  %s' %(e, str(obj_result)))
            else:
                if not capture_phase:
                    obj_result['recently'] = 1
                try:
                    sql = table.insert().values(**self._stringify(obj_result))
                    return self.engine.execute(sql)
                except Exception, e:
                    logging.error('insert data failed. error: %s - %s' %(e, str(obj_result)))
        except Exception, e:
            logging.error('save failed. error: %s - %s' %(str(e), str(obj_result)))
            
    @staticmethod
    def escape(string):
        return '%s' % string
    
    def _select2dic(self, tablename=None, what="*", where="", where_values=[],
                    order=None, offset=0, limit=None):
        tablename = self.escape(tablename or self.__tablename__)
        if isinstance(what, list) or isinstance(what, tuple) or what is None:
            what = ','.join(self.escape(f) for f in what) if what else '*'

        sql_query = "SELECT %s FROM \"%s\"" % (what, tablename)
        if where:
            sql_query += " WHERE %s" % where
        if order:
            sql_query += ' ORDER BY %s' % order
        if limit:
            #only for mysql
            #sql_query += " LIMIT %d, %d" % (offset, limit)
            #分页查询
            columns = what.split(',')
            columns_new = []
            for column in columns:
                columns_new.append('A.'+column)
            what = ','.join(columns_new)
            sql_query = "SELECT * FROM (SELECT %s, ROWNUM r FROM \"%s\" A " % (what, tablename)
            if where:
                sql_query +=" WHERE %s" % where
            if order:
                sql_query += ' ORDER BY %s' % order
            sql_query += ") B"
            sql_query +=" WHERE B.r BETWEEN %d and %d" % (offset+1, offset+limit)

        where_valuess = []
        for item in where_values:
            where_valuess.append(str(item))
        sql = sql_query % tuple(where_valuess)

        dbcur = self.engine.execute(sql)
        fields = [f[0] for f in dbcur._cursor_description()]
        
        if 'R' in fields:
            fields.remove('R')

        for row in dbcur:
            yield dict(zip(fields, row))
            
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
        for count, in self.engine.execute("SELECT count(1) FROM \"%s\"" % tablename):
            return count
    
    def get(self, project, key, key_value, fields=None):
        if project not in self.projects:
            self._list_project()
        if project not in self.projects:
            return
        #if self.table is None:
        #    return

        tablename = self._tablename(project)
        where = "%s = '%s'" % (key, self.placeholder)
        for task in self._select2dic(tablename, what=fields,
                                     where=where, where_values=(key_value, )):
            return self._parse(task)
    
