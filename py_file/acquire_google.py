# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 17:48:39 2016

@author: lstanevich
"""

import requests
import codecs

from py_log.logger import logMain
from py_log.log_decorators import dec_log_entry_exit  # , dec_log_debug_override


#%% Input routines


@dec_log_entry_exit
def dictify(lstSource, keyPrimary, **kwargs):
    newDict = {}
    strSplit = ','

    if 'strSplit' in kwargs:
        strSplit = kwargs['strSplit']

    listKeys = codecs.decode(lstSource[0]).split(strSplit)

    index = 1
    for i in lstSource[1:]:
        # Explode the current record row into separate fields
        listValues = codecs.decode(i).split(strSplit)

        # Zip the record's values into a single dict
        tmpRec = dict(zip(listKeys, listValues))
        tmpRec['index'] = '{0:05d}'.format(index)

        if len(tmpRec[keyPrimary]) > 0:
            # Insert the record's dict into the master dict, based on the primary key
            newDict[tmpRec[keyPrimary]] = tmpRec

            # Remove the redundant primary key field from within the record dict
            # del newDict[tmpRec[keyPrimary][keyPrimary]]
        else:
            print('No [' + keyPrimary + '] on row : ' + str(index))
            logMain.WARNING('No [' + keyPrimary + '] value on row : ' + str(index))

        index = index + 1
    return newDict


@dec_log_entry_exit
def loadSheet(srcUrl, keyPrimary, *args, **kwargs):
    """
    Loads table from Google Spreadsheet

    *Args
    -----
        [0] 'urlName': Full URL to desired sheet
        xczxczxc

    **KWargs
    ---------------------
       **key:** Define primary key field

       strSplit (Optional): Override for 'strSplit' of ','


    Requirements
    ------------
    - Source sheet must be publicly published as CSV

    """

    if not keyPrimary:
        raise Exception('ERROR: No Primary Key Specified')

    srcTable = requests.get(srcUrl).content.splitlines()

    return dictify(srcTable, keyPrimary, **kwargs)


#%% Main routines

if __name__ == '__main__':

    logMain.open(fileName='csv-test')
    logMain.open(loggingLevel='INFO')

    urlDA = 'https://docs.google.com/spreadsheets/d/1gYfWH2YraNia61cCAPKhsGudApyES7CqTSydcPvFl0w/pub?gid=1787259869&single=true&output=csv'
    urlSources = 'https://docs.google.com/spreadsheets/d/1koHUvWRovwoW53nclnkYnLTUze4G9aEXL_fYkRJVhcc/pub?gid=953166969&single=true&output=csv'
    urlMap = 'https://docs.google.com/spreadsheets/d/1koHUvWRovwoW53nclnkYnLTUze4G9aEXL_fYkRJVhcc/pub?gid=1617683662&single=true&output=csv'

    testUnits = {}
    testUnits['loadSheet'] = True

    if testUnits['loadSheet']:

        tableDA = loadSheet(urlDA, keyPrimary='Page ID')
        tableSource = loadSheet(urlSources, keyPrimary='Source ID')
        tableMap = loadSheet(urlMap, keyPrimary='index')
