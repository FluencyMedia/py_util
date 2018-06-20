# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 19:32:59 2016

@author: lstanevich
"""

import pandas as pd

from py_frame import objFrame
from py_sheet import urlHandler

from py_log import logMain
# from py_log.log_decorators import dec_logEntryExit  # , dec_logDebugOverride


# @dec_logEntryExit
class objSheet(objFrame):
    """
    Handles base 'objSheet' dataFrames that are acquired directly from Google Sheets

    Required Parameters
    --------------------
    sheetID: ID of the Google Sheet
    tabID: ID of the specific tab within the Google Sheet

    Optional Parameters
    -------------------
    Various 'dataFrame' parameters, such as:
    usecols: The set of columns to be extracted from the specified Sheet and tab
    index_col: The specific column to be used as the table index
    """

    def __init__(self, sheetInfo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logMain.INFO("Constructing objSheet")
        logMain.indentRaise
        self._urlHandler = urlHandler(sheetInfo)
        # self._dataTable = pd.read_csv(self.url, **sheetInfo[2])
        # #TODO: This is a really sloppy fix
        logMain.indentLower

    @property
    def url(self):
        return self._urlHandler.url


def loadSheet(currURL: urlHandler, urlName=None):

    if urlName is not None:
        logMain.INFO("Loading: " + urlName)
    frameTemp = objFrame(pd.read_csv(currURL.url, **currURL.kwargs))
    if urlName is not None:
        logMain.INFO("Loaded: " + urlName)

    return frameTemp


#%% Unit tests

if __name__ == '__main__':

    from py_file import listURLs

    logMain.open(fileName='obj_sheet')
    logMain.consoleMirror = True
    logMain.loggingLevel = 'INFO'

    testUnits = {}

    testUnits['urlHandler'] = False
    testUnits['objSheet'] = False
    testUnits['testInheritance'] = True

    if testUnits['testInheritance']:
        tempURL = urlHandler(listURLs['urlDA'])
        sheetDA = pd.read_csv(tempURL.url)

    if testUnits['objSheet']:

        sheetDA = objSheet(listURLs['urlDA'])
        tableDA = sheetDA.dataTable

        sheetSources = objSheet(listURLs['urlSources'])
        tableSources = sheetDA.dataTable

        sheetMap = objSheet(listURLs['urlMap'])
        tableMap = sheetDA.dataTable
