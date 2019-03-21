"""
Created on Mon Sep 26 19:08:00 2016

@author: lstanevich
"""

# import os

import pandas as pd

from py_log.logger import logMain
# from py_log.log_decorators import  dec_log_entry_exit  # , dec_log_debug_override

from path_manager import objLoc

from py_sheet.url_manager import urlHandler
from py_frame.frame_manager import objFrame

from py_dev import myDevice

recPaths = ['1j-ic8K3ijarZR_fiKChPzpoiYeIZW6ZejvL94-u70H4',
            '329635327',
            {'index_col': 'Channel'}]
urlPaths = urlHandler(recPaths)

recDevices = ['1j-ic8K3ijarZR_fiKChPzpoiYeIZW6ZejvL94-u70H4',
            '1880061717',
            {'index_col': 'Device'}]
urlDevices = urlHandler(recDevices)


class objLocMgr(objFrame):
    """
    Manages multiple locations
    Subclass of 'objFrame()'

    Requred Arguments
    -----------------
    myDF: DataFrame
    Base DataFrame that the location manager will be wrapped around

    myEnv: string
    Default environment (usually "Dev" or "Client")

    myPaths: dict
    Dictionary of absolute local paths to use as base on current machine
    """
    def __init__(self, myDF, myPaths, myEnv, myDevice, *args, **kwargs):
        super(objLocMgr, self).__init__(myDF, args, kwargs)
        # self.arg = arg
        self._location = ""
        self._env = ""
        self.env = myEnv
        self._devices = pd.read_csv(myPaths.url, **myPaths.kwargs)
        self._device = ""
        self.device = myDevice

    @property
    def env(self):
        """
        Defines the current environment (usually "Dev" or "Client")
        """
        return self._env

    @env.setter
    def env(self, newEnv):
        if newEnv in self.envs:
            self._env = newEnv
        else:
            logMain.WARNING("Attempt to set non-existent environment: " + newEnv)

    @property
    def envs(self):
        """
        Returns the list of available environments
        """
        return self.dataFrame.columns

    def relLoc(self, myLoc):
        """
        Returns the relative path for the specified location
        Usually "input", "output", "json", etc.
        """
        if myLoc in self.locations:
            return self.dataFrame[self.env][myLoc]
        else:
            logMain.WARNING("Attempt to retrieve non-existent location: " + myLoc)

    @property
    def locations(self):
        """
        Returns list of available locations
        """
        return self.dataFrame.index

    @property
    def devices(self):
        """
        Returns list of available devices
        """
        return self._devices.index

    @property
    def device(self):
        """
        Manages identity of current device
        """
        return self._device

    @device.setter
    def device(self, newDevice):
        if newDevice in self.devices:
            self._device = newDevice
        else:
            logMain.WARNING("Attempt to set non-existent device: " + newDevice)

    @property
    def absLoc(self):
        """
        Returns the absolute 'parent' path within the current device's file system
        """
        return self._devices[self.env][self.device]

    def path(self, myLoc):
        """
        Returns the current complete path for the specified location's files on the current device
        self.absLoc + self.relLoc(myLoc)

        Required Argument
        -----------------
        myLoc: string
        The name of the desired location
        """
        # tmpLoc = objLoc(self.absLoc, self.relLoc(myLoc))
        return objLoc(self.absLoc, self.relLoc(myLoc)).path


locManager = objLocMgr(pd.read_csv(urlPaths.url, **urlPaths.kwargs), urlDevices, "Dev", myDevice)


if __name__ == "__main__":

    logMain.open(fileName='log-loc-mgr.log')
    logMain.logging_level = "INFO"
    logMain.console_mirror = True

    framePaths = locManager.dataFrame
    fieldsPaths = locManager.fields
    frameDevices = locManager._devices

    for e in locManager.envs:
        locManager.env = e
        logMain.INFO("Device: " + locManager.device)
        logMain.INFO("Environment: " + locManager.env, padBefore=1)
        logMain.indent_raise()
        logMain.INFO("Device Path: " + locManager.absLoc)
        for l in locManager.locations:
            logMain.INFO("'" + l + "': " + locManager.path(l))
        logMain.indent_lower()
