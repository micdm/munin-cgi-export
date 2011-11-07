# coding=utf-8

from settings import NODES
from stuff.errors import InvalidNodeException

class Node(object):
    '''
    Нода.
    '''
    
    def __init__(self, domain, name):
        '''
        @param domain: string
        @param name: string
        '''
        self._info = self._get_info(domain, name)
        if self._info is None:
            raise InvalidNodeException()
        
    def _get_info(self, domain, name):
        '''
        Находит и возвращает информацию о ноде из настроек.
        @param domain: string
        @param name: string
        @return: dict
        '''
        for node in NODES:
            if node['domain'] == domain and node['name'] == name:
                return node
        return None
    
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
