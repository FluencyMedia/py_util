# -*- coding: utf-8 -*-
"""
Created on Thu Jun 08 20:57:00 2017
@author: lstanevich
"""

# import json
import requests

from py_log.logger import logMain
from py_log.log_decorators import dec_log_entry_exit  # , dec_log_debug_override

# from urllib.parse import urlparse, urlunparse

#%% JSON import modules


@dec_log_entry_exit
def getJSONRest(srcURL):
    r = requests.get(srcURL)

    return r.json()

#%% Main


if __name__ == "__main__":
    logMain.open(fileName='rest-acquire')
    logMain.logging_level = "INFO"
    logMain.console_mirror = True

    testUnits = {}
    testUnits['getREST'] = True

    if testUnits['getREST']:
        srcURL = "https://jsonplaceholder.typicode.com/posts"
        r = getJSONRest(srcURL)
        tmpData = r
