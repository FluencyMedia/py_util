# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 09:20:29 2016

@author: lstanevich
"""

import os

from py_log.logger import logMain
from py_log.log_decorators import dec_log_entry_exit  # , dec_log_debug_override


# %% File traversal modules


@dec_log_entry_exit
def path_walk(curr_func, curr_path: str, *args, **kwargs):
    """
    Traverses all directories and files within a designated location, applying a specific function.

    Required Arguments
    ------------------
    curr_func: function
    The function that will be applied to each file that is traversed

    curr_path: string
    Absolute path to the directory that is meant to have its contents traversed

    Passthrough Arguments
    ---------------------
    *args and **kwargs will be passed through to the applied function
    """

    curr_struct = os.walk(curr_path)

    for root, dirs, files in curr_struct:
        for d in dirs:
            if d[0] == ".":
                dirs.remove(d)
            elif d[:2] == "__":
                dirs.remove(d)
            elif d[:3] == "ZZZ":
                dirs.remove(d)
            for file in files:
                if file[0] == ".":
                    files.remove(file)
                elif ".ini" in file:
                    files.remove(file)
        curr_rel_path = root.replace(curr_path, "") + "\\"

        logMain.INFO("Processing: " + curr_rel_path, padBefore=2, padAfter=1)
        print("Processing: " + curr_rel_path)

        logMain.DEBUG("Current Root" + os.path.basename(root))
        for currFile in files:
            curr_func(curr_rel_path, currFile, *args, **kwargs)

    return


# %% Main module


if __name__ == "__main__":

    logMain.open("log-path")
    logMain.console_mirror = True
    logMain.logging_level = "INFO"
