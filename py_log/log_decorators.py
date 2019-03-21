# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 12:28:14 2016

@author: lstanevich
"""

import datetime
from py_log.logger import logMain


class EnterExitLog:
    def __init__(self, func_name):
        self.funcName = func_name

    def __enter__(self):
        logMain.indent_raise()
        logMain.INFO('Started: ' + self.funcName)
        logMain.indent_raise()
        self.init_time = datetime.datetime.now()
        return self

    def __exit__(self, type, value, tb):
        logMain.indent_lower()
        logMain.INFO('Finished: %s in: %s seconds' % (self.funcName, datetime.datetime.now() - self.init_time))
        logMain.indent_lower()


def dec_log_entry_exit(func):
    def func_wrapper(*args, **kwargs):
        with EnterExitLog(func.__name__):
            return func(*args, **kwargs)

    return func_wrapper


class LogDebugOverride:
    def __init__(self, func_name):
        self.funcName = func_name
        self._currLoggingLevel = logMain.logging_level

    def __enter__(self):
        logMain.logging_level = 'DEBUG'
        logMain.indent_raise()
        # logMain.DEBUG('DEBUG OVERRIDE: ' + self.funcName, padBefore=1)
        self.init_time = datetime.datetime.now()
        return self

    def __exit__(self, type, value, tb):
        # logMain.DEBUG('FINISHED DEBUG OVERRIDE:
        #                %s in: %s seconds' % (self.funcName, datetime.datetime.now() - self.init_time))
        logMain.indent_lower()
        logMain.logging_level = self._currLoggingLevel


def dec_log_debug_override(func):
    def func_wrapper(*args, **kwargs):
        with LogDebugOverride(func.__name__):
            return func(*args, **kwargs)

    return func_wrapper


if __name__ == '__main__':

    #    from py_log.logger import ClsLogger

    logMain.logging_level = 'DEBUG'

    @dec_log_entry_exit
    def test_func():
        print("TESTING")

    test_func()
