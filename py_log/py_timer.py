# -*- coding: utf-8 -*-
"""
Created on 7/13/17 9:56 PM

@author: lstanevich
"""

from py_log.logger import logMain

if __name__ == "__main__":
    logMain.open(fileName='py_timer')
    logMain.logging_level = "INFO"
    logMain.console_mirror = True

    testUnits = {}
    testUnits['py_timer'] = True

    if testUnits['py_timer']:
        logMain.INFO('Testing')

    logMain.INFO('py_timer completed')
