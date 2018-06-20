# -*- coding: utf-8 -*-
"""
Created on 7/13/17 9:56 PM

@author: lstanevich
"""

from py_log import logMain

if __name__ == "__main__":
    logMain.open(fileName='py_timer')
    logMain.loggingLevel = "INFO"
    logMain.consoleMirror = True

    testUnits = {}
    testUnits['py_timer'] = True

    if testUnits['py_timer']:
        logMain.INFO('Testing')

    logMain.INFO('py_timer completed')