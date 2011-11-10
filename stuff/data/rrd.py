# coding=utf-8

from subprocess import Popen, PIPE

from settings import DATA_DIR
from stuff.errors import InvalidReportTypeException, InvalidPeriodException

class RrdDataGenerator(object):
    '''
    Получатель данных из RRD.
    '''

    def __init__(self, node, data_type, period):
        '''
        @param node: Node
        @param data_type: string
        @param period: string
        '''
        filename = self._get_filename_for_type(node, data_type)
        start = self._get_start(period)
        self._data = self._get_data(filename, start, 'now')
    
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
        raise InvalidReportTypeException()
        
    def _get_filename_for_type(self, node, data_type):
        '''
        Возвращает название файла с БД для запрошенного типа данных.
        @param node: Node
        @param data_type: string
        @return: string
        '''
        db_name = self._get_db_name_for_type(data_type)
        return '%s/%s/%s-%s.rrd'%(DATA_DIR, node.get_domain(), node.get_name(), db_name)
    
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
        raise InvalidPeriodException()
    
    def _get_data(self, filename, start, end):
        '''
        Непосредственно добывает данные.
        @param filename: string
        @param start: string
        @param end: string
        '''
        var_def = 'DEF:x=%s:42:AVERAGE'%filename
        args = ['rrdtool', 'xport', '--start', start, '--end', end, var_def, 'XPORT:x']
        process = Popen(args, stdout=PIPE)
        stdout, _ = process.communicate()
        return stdout

    def get_data(self):
        '''
        Возвращает данные.
        @return: string
        '''
        return self._data
