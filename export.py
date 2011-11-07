#!/usr/bin/python
# coding=utf-8

from stuff.data import DataReceiver
from stuff.errors import InvalidNodeException, InvalidReportTypeException, InvalidPeriodException
from stuff.http import Request, NoDataResponse, DataAvailableResponse
from stuff.munin import Node

if __name__ == '__main__':
    try:
        request = Request()
        node = Node(request.get_node_domain(), request.get_node_name())
        data_receiver = DataReceiver(node, request.get_data_type(), request.get_period())
        response = DataAvailableResponse(data_receiver.get_data())
    except (InvalidNodeException, InvalidReportTypeException, InvalidPeriodException):
        response = NoDataResponse()
    print str(response)
