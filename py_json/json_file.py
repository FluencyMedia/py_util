# -*- coding: utf-8 -*-
"""
Created on 2017-06-16T21:04:37.594Z

@author: lstanevich
"""

import json

from py_log.logger import logMain
from py_log.log_decorators import dec_logEntryExit  # , dec_logDebugOverride


@dec_logEntryExit
def getJSONFile(srcPathJSON, srcFilename):  # , destPages, strTimestamp):

    # Assumes all input files are one directory level down
    with open(srcPathJSON + "\\" + srcFilename, encoding='utf-8') as data_file:
        data = json.load(data_file)

    return data


if __name__ == '__main__':
    logMain.open(fileName='json-file')
    logMain.loggingLevel = "INFO"
    logMain.consoleMirror = True

    testUnits = {}
    testUnits['testFileIn'] = True

    if testUnits['testFileIn']:
        logMain.INFO("Testing JSON file load")
        jsonFileTest = getJSONFile('C:\Dev\cdp_app\cdp_samples', 'bulk_offerings.json')
        logMain.INFO(json.dumps(jsonFileTest, ensure_ascii = False, indent=4))
