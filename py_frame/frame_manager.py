"""
Created on Sat Sep 17 13:39:00 2016

@author: lstanevich
"""

import pandas as pd

from py_sheet.url_manager import urlHandler

from py_log.logger import logMain
# from py_log.log_decorators import dec_log_entry_exit  # , dec_log_debug_override


class objSeries(pd.Series):
    @property
    def _constructor(self):
        return objSeries


class objFrame():
    """
    Manages interaction logic (filters, etc.) around base 'objSheet' dataFrames

    Required Parameters
    --------------------
    myDF: Pandas DataFrame that is to be attached
    """

    def __init__(self, myDF, *args, **kwargs):
        # self._query = ""
        logMain.INFO("Constructing objFrame")
        logMain.indent_raise

        self._dataFrame = myDF
        self.dataFrame.columns = self.dataFrame.columns.map(lambda x: x.replace(' ', '_'))
        self.dataFrame.columns = self.dataFrame.columns.map(lambda x: x.replace('(', ''))
        self.dataFrame.columns = self.dataFrame.columns.map(lambda x: x.replace(')', ''))
        self.dataFrame.columns = self.dataFrame.columns.map(lambda x: x.replace('?', ''))

        logMain.indent_lower

    @property
    def dataFrame(self):
        return self._dataFrame

    # @property
    # def query(self):
    #     """ Stores the query string that will be used to filter the returned dataFrame """
    #     return str(self._query)
    #
    # @query.setter
    # def query(self, newQuery):
    #     self._query = newQuery
    #
    # @query.deleter
    # def query(self):
    #     self._query = ""


if __name__ == '__main__':

    from py_sheet.url_manager import listURLs

    logMain.open(fileName='obj_frame')

    testUnits = {}

    testUnits['objFrame'] = False
    testUnits['propQuery'] = False
    testUnits['testInheritance'] = True

    if testUnits['testInheritance']:
        urlDA = urlHandler(listURLs['urlDA'])
        frameDA = objFrame(pd.read_csv(urlDA.url)).dataFrame

    if testUnits['objFrame']:

        frameDA = objFrame(listURLs['urlDA'])
        tableDA = frameDA.dataFrame

        frameSources = objFrame(listURLs['urlSources'])
        tableSources = frameSources.dataFrame

        frameMap = objFrame(listURLs['urlMap'])
        tableMap = frameMap.dataFrame

    if testUnits['propQuery']:
        logMain.write('Testing Query Property', consoleMirror=True, padAfter=2)
        logMain.indent_raise()
        logMain.write('Current Query: ' + frameDA.query)
        frameDA.query = 'Code in ["CANCER", "ORTHO"] and Content_Type in ["Condition", "Treatment"]'
        logMain.write('Current Query: ' + frameDA.query)
        tableQuery = frameDA.dataFrame
