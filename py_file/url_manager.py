# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 14:02:59 2016

@author: lstanevich
"""

from py_log import logMain
from py_log import dec_logEntryExit  # , dec_logDebugOverride


@dec_logEntryExit
class urlHandler():
    """
    Handles components of the URL that points to a given Google Sheet

    Arguments
    ---------
    sheetInfo: item within listURLs
        sheetInfo[0] -> 'sheetID': ID of the Google sheet
        sheetInfo[1] -> 'tabID': ID of the specific tab
    """
    _urlPrefix = 'https://docs.google.com/spreadsheets/d/'
    _urlInfix = '/pub?gid='
    _urlSuffix = '&single=true&output=csv'

    def __init__(self, sheetInfo):
        logMain.INFO("Sheet Details:")
        logMain.indentRaise
        self._sheetID = sheetInfo[0]
        logMain.INFO('Sheet ID: ' + self._sheetID)
        self._tabID = sheetInfo[1]
        logMain.INFO('Tab ID: ' + self._tabID)
        self._kwargs = sheetInfo[2]
        if self.kwargs:
            logMain.INFO("KW Arguments")
            logMain.indentRaise
            for kw in self.kwargs:
                logMain.INFO(kw + ": " + str(self.kwargs[kw]))
            logMain.indentLower
        logMain.indentLower

    @property
    def url(self):
        """ Returns a complete URL constructed from component elements """
        return self._urlPrefix + self.sheetID + self._urlInfix + self.tabID + self._urlSuffix

    @property
    def sheetID(self):
        """ Returns the specific 'sheetID' that was passed in """
        return self._sheetID

    @property
    def tabID(self):
        """ Returns the specific 'tabID' that was passed in"""
        return self._tabID

    @property
    def kwargs(self):
        return self._kwargs

#%% Unit test data


listURLs = {}

listURLs['urlDA'] = ['1gYfWH2YraNia61cCAPKhsGudApyES7CqTSydcPvFl0w',
                        '1787259869',
                        {'usecols': ['Page ID', 'Code', 'Level', 'Parent', 'OrigPos', 'Content Type', 'Page Title', 'URL', 'H1', 'Priority', 'Wave', 'Status', 'Assigned', 'Relative URL'],
                        'index_col': 'Page ID'}]

listURLs['urlSources'] = ['1koHUvWRovwoW53nclnkYnLTUze4G9aEXL_fYkRJVhcc',
                        '953166969',
                        {'index_col': 'Source ID'}]

listURLs['urlMap'] = ['1koHUvWRovwoW53nclnkYnLTUze4G9aEXL_fYkRJVhcc',
                        '1617683662',
                        {'usecols': ['Page ID Fill', 'Source ID', 'Action', 'Status', 'Notes', 'Exists', 'Status']}]


if __name__ == '__main__':

    logMain.open(fileName='obj_url')
    logMain.consoleMirror = True
    logMain.loggingLevel = 'INFO'

    testUnits = {}

    testUnits['urlHandler'] = False

    if testUnits['urlHandler']:

        for url in listURLs:
            currURL = urlHandler(listURLs[url])
            logMain.write(url + ": " + currURL.url, padAfter=2)
