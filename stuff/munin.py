# coding=utf-8

from settings import NODES
from stuff.errors import InvalidNodeException

class Node(object):
    '''
    Нода.
    '''
    
    def __init__(self, name):
        '''
        @param name: string
        '''
        self._info = self._get_info(name)
        
    def _get_info(self, name):
        '''
        Находит и возвращает информацию о ноде из настроек.
        @param name: string
        @return: dict
        '''
        for node in NODES:
            if node['name'] == name:
                return node
        raise InvalidNodeException()
    
    def get_domain(self):
        '''
        Возвращает домен.
        @return: string
        '''
        return self._info['domain']
    
    def get_name(self):
        '''
        Возвращает название.
        @return: string
        '''
        return self._info['name']
    
    def has_report(self, report_type):
        '''
        Возвращает, есть ли отчет для данной ноды.
        @param report_type: string
        @return: bool
        '''
        return report_type in self._info['reports']
