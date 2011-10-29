#!/usr/bin/python
# coding=utf-8

import cgi
from subprocess import Popen, PIPE

class DataReceiver(object):
    '''
    Получатель данных из RRD.
    '''
    
    DATA_DIR = '/var/lib/munin/localdomain'
    DATA_PREFIX = 'localhost.localdomain'
    
    def __init__(self, data_type, period):
        '''
        @param data_type: string
        @param period: string
        '''
        filename = self._get_filename_for_type(data_type)
        start = self._get_start(period)
        self._data = self._get_data(filename, start, 'now')
    
    def __str__(self):
        return self._data
    
    def _get_db_name_for_type(self, data_type):
        '''
        Возвращает название БД для запрошенного типа данных.
        @param data_type: string
        @return: string
        '''
        if data_type == 'load':
            return 'load-load-g'
        if data_type == 'users':
            return 'users-pts-g'
        return None
        
    def _get_filename_for_type(self, data_type):
        '''
        Возвращает название файла с БД для запрошенного типа данных.
        @param data_type: string
        @return: string
        '''
        db_name = self._get_db_name_for_type(data_type)
        if db_name is None:
            return None
        return '%s/%s-%s.rrd'%(self.DATA_DIR, self.DATA_PREFIX, db_name)
    
    def _get_start(self, period):
        '''
        Возвращает начало интервала.
        @param period: string
        @return: string
        '''
        if period == 'hour':
            return 'now-1h'
        if period == 'day':
            return 'now-1d'
        return None
    
    def _get_data(self, filename, start, end):
        '''
        Непосредственно добывает данные.
        @param filename: string
        @param start: string
        @param end: string
        '''
        if filename is None or start is None or end is None:
            return 'no data'
        var_def = 'DEF:x=%s:42:AVERAGE'%filename
        process = Popen(['rrdtool', 'xport', '--start', start, '--end', end, var_def, 'XPORT:x'], stdout=PIPE)
        stdout, _ = process.communicate()
        return stdout


class Request(object):
    '''
    Запрос клиента.
    '''
    
    def __init__(self):
        self._query_string = cgi.parse()
    
    def get_data_type(self):
        '''
        Возвращает тип запрошенных данных.
        @return: string
        '''
        if 'type' not in self._query_string:
            return None
        result = self._query_string['type'][0]
        if result not in ('load', 'users'):
            return None
        return result
    
    def get_period(self):
        '''
        Возвращает период.
        @return: string
        '''
        if 'period' not in self._query_string:
            return None
        result = self._query_string['period'][0]
        if result not in ('hour', 'day'):
            return None
        return result 


class Response(object):
    '''
    Ответ сервера.
    '''

    def __init__(self, request):
        self._request = request

    def __str__(self):
        result = []
        result.append(self._get_content_type_header())
        result.append('')
        result.append(self._get_body())
        return '\r\n'.join(result)

    def _get_content_type_header(self):
        '''
        Возвращает заголовок с типом.
        @return: string
        '''
        return 'Content-Type: text/xml'

    def _get_body(self):
        '''
        Возвращает тело ответа.
        @return: string
        '''
        data_type = self._request.get_data_type()
        period = self._request.get_period()
        if data_type and period:
            return str(DataReceiver(data_type, period))
        return 'incorrect request'


request = Request()
print str(Response(request))
