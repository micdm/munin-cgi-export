# coding=utf-8

class InvalidNodeException(Exception):
    '''
    Запрошена некорректная нода.
    '''


class InvalidReportTypeException(Exception):
    '''
    Запрошен некорректный отчет по ноде.
    '''


class InvalidPeriodException(Exception):
    '''
    Запрошен некорректный временной промежуток.
    '''
