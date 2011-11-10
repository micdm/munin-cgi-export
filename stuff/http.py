# coding=utf-8

import os

class Request(object):
    '''
    Запрос клиента.
    '''
    
    def __init__(self):
        path_info = os.environ.get('PATH_INFO') or ''
        self._parts = path_info.strip('/').split('/')
    
    def _get_part(self, index):
        '''
        Возвращает кусочек запроса.
        @param index: int
        @return: string
        '''
        return self._parts[index] if len(self._parts) > index else None
    
    def get_action(self):
        '''
        Возвращает действие.
        @return: string
        '''
        return self._get_part(0)
    
    def get_node_name(self):
        '''
        Возвращает имя запрошенной ноды.
        @return: string
        '''
        return self._get_part(1)
        
    def get_data_type(self):
        '''
        Возвращает тип запрошенных данных.
        @return: string
        '''
        return self._get_part(2)
    
    def get_period(self):
        '''
        Возвращает период.
        @return: string
        '''
        return self._get_part(3)


class Response(object):
    '''
    Абстрактный ответ сервера.
    '''
        
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
        Возвращает тело сообщения.
        @return: string
        '''
        return ''


class NoDataResponse(Response):
    '''
    Ответ о недоступности данных.
    '''

    def _get_body(self):
        return '<no_data/>'


class DataAvailableResponse(Response):
    '''
    Ответ с данными.
    '''
    
    def __init__(self, data):
        '''
        @param data: string
        '''
        self._data = data
    
    def _get_body(self):
        return self._data
