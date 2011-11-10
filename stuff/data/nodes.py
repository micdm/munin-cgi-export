# coding=utf-8

from xml.etree.ElementTree import Element, tostring

from settings import NODES

class NodesDataGenerator(object):
    '''
    Генератор списка нод.
    '''
    
    def __init__(self):
        self._data = tostring(self._generate_data())
    
    def _generate_report_data(self, report):
        '''
        Генерирует данные об отчете.
        @param report: string
        @return: Element
        '''
        return Element('report', {'type': report})
    
    def _generate_node_data(self, node):
        '''
        Генерирует данные о конкретной ноде.
        @param node: dict
        @return: Element
        '''
        node_element = Element('node', {'domain': node['domain'], 'name': node['name']})
        for report in node['reports']:
            report_element = self._generate_report_data(report)
            node_element.append(report_element)
        return node_element
    
    def _generate_data(self):
        '''
        Генерирует данные о нодах.
        @return: Element
        '''
        nodes_element = Element('nodes')
        for node in NODES:
            node_element = self._generate_node_data(node)
            nodes_element.append(node_element)
        return nodes_element

    def get_data(self):
        '''
        Возвращает сгенерированные данные.
        @return: string
        '''
        return self._data
