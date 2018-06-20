# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 09:20:29 2016

@author: lstanevich
"""

import os

from py_log import logMain
from py_log import dec_logEntryExit  # , dec_logDebugOverride


#%% File traversal modules


@dec_logEntryExit
def pathWalk(currFunct, currPath, *args, **kwargs):
    """
    Traverses all directories and files within a designated location, applying a specific function

    Required Arguments
    ------------------
    currFunct: function
    The function that will be applied to each file that is traversed

    currPath: string
    Absolute path to the directory that is meant to have its contents traversed

    Passthrough Arguments
    ---------------------
    *args and **kwargs will be passed through to the applied function
    """

    currStruct = os.walk(currPath)

    for root, dirs, files in currStruct:
        for dir in dirs:
            if dir[0] == '.':
                dirs.remove(dir)
            elif dir[:2] == '__':
                dirs.remove(dir)
            elif dir[:3] == 'ZZZ':
                dirs.remove(dir)
            for file in files:
                if file[0] == '.':
                    files.remove(file)
                elif '.ini' in file:
                    files.remove(file)
        currRelPath = root.replace(currPath, '') + '\\'

        logMain.INFO("Processing: " + currRelPath, padBefore=2, padAfter=1)
        print("Processing: " + currRelPath)

        logMain.DEBUG("Current Root" + os.path.basename(root))
        for currFile in files:
            currFunct(currRelPath, currFile, *args, **kwargs)

    return

#%% Main module


if __name__ == '__main__':

    logMain.open(filename = 'log-path')
    logMain.consoleMirror = True
    logMain.loggingLevel = "INFO"
