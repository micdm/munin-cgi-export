#!/usr/bin/python
# coding=utf-8

from stuff.data.nodes import NodesDataGenerator
from stuff.data.rrd import RrdDataGenerator
from stuff.errors import InvalidActionException
from stuff.http import Request, NoDataResponse, DataAvailableResponse
from stuff.munin import Node

def get_nodes_response(request):
    '''
    Обрабатывает запрос списка нод.
    '''
    generator = NodesDataGenerator()
    return DataAvailableResponse(generator.get_data())


def get_report_response(request):
    '''
    Обрабатывает запрос отчета.
    '''
    node = Node(request.get_node_name())
    generator = RrdDataGenerator(node, request.get_data_type(), request.get_period())
    return DataAvailableResponse(generator.get_data())


def get_action_handler(action):
    '''
    Возвращает обработчик для указанного действия.
    @param action: string
    @return: function
    '''
    if action == 'nodes':
        return get_nodes_response
    if action == 'report':
        return get_report_response
    raise InvalidActionException()


if __name__ == '__main__':
    try:
        request = Request()
        action = request.get_action()
        handler = get_action_handler(action)
        response = handler(request)
    except Exception as e:
        response = NoDataResponse()
    print str(response)
