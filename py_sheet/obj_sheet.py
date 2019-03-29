# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 19:32:59 2016

@author: lstanevich
"""

import pandas as pd

from py_frame.frame_manager import objFrame
from py_sheet.url_manager import urlHandler

from py_log.logger import logMain
# from py_log.log_decorators import dec_log_entry_exit  # , dec_log_debug_override


# @dec_log_entry_exit
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
        logMain.indent_raise
        self._urlHandler = urlHandler(sheetInfo)
        # self._dataTable = pd.read_csv(self.url, **sheetInfo[2])
        # #TODO: This is a really sloppy fix
        logMain.indent_lower

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

    from py_util.url_manager import listURLs

    logMain.open(fileName='obj_sheet')
    logMain.console_mirror = True
    logMain.logging_level = 'INFO'

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
