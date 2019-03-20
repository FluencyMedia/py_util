# -*- coding: utf-8 -*-
"""
Created on Thu Sep  13 18:03:00 2016

@author: lstanevich
"""

# import typing
import os

from py_file.file_manager import fManager
from config_main import strTimestamp


# %% Class ClsLogger

# noinspection PyTypeChecker
class ClsLogger:
    """
    Generates new instance of logging object

    Optional Attributes
    -------------------
        indentLevel: int
            Overrides default indentation level of 0
        indentSize: int
            Overrides default indentation size of 4 spaces
        loggingLevel: str
            Overrides default minimum loggingLevel of 'WARNING'
    """
    # %% Class constructor

    _loggingLevels = {'DEBUG': 0, 'INFO': 1, 'WARNING': 2, 'ERROR': 3, 'CRITICAL': 4}

    def __init__(self, **fargs):

        self._properties = {
            'indentLevel': 0,
            'indentSize': 4,
            'consoleMirror': False
        }

        self._loggingLevel = 'WARNING'

        self._currTime = strTimestamp

        self._fOpen = False

        for fArg in fargs:
            if fArg == 'loggingLevel':
                if fArg['loggingLevel'] in self._loggingLevels:
                    self._loggingLevel = self._loggingLevels[fArg["loggingLevel"]]
                else:
                    raise Exception("ERROR: Attempt to set unknown Log Level: " + fArg['loggingLevel'])
            else:
                self._properties[fArg] = fargs[fArg]

            if 'fileName' in fargs:
                self.open(**fargs)

    # %% Property management functions

    @property
    def indentLevel(self):
        """ Returns the current indentLevel """
        return self._properties['indentLevel']

    @indentLevel.setter
    def indentLevel(self, newval: int):
        """ Sets the current indentLevel """
        self._properties['indentLevel'] = newval

    @property
    def indentSize(self):
        """
        Assigns or returns the current indentSize
        """
        return self._properties['indentSize']

    @indentSize.setter
    def indentSize(self, new_val: int):
        """ Sets the current indentSize """
        self._properties['indentSize'] = new_val

    def indentRaise(self, *args):
        int_change = 1
        if args:
            if args[0] > 0:
                int_change = args[0]
            else:
                raise Exception("Attempt to raise indent level: " + args[0])
        newLevel = self.indentLevel + int_change
        self.indentLevel = newLevel

    def indentLower(self, int_lower=None):
        """
        Forcefully lowers the current level of indentation
        Arguments
        ---------
            int_lower: int
                Optional: The number of levels by which indentation should be lowered (if not provided, =1)
        """
        if not int_lower:
            intChange = 1
        else:
            intChange = abs(int_lower)
        if intChange > self.indentLevel:
            newLevel = 0
        else:
            newLevel = self.indentLevel - intChange

        self.indentLevel = newLevel

    def writeRaise(self, str_output=None, **kwargs):
        self.indentRaise()
        self.write(str_output, **kwargs)

    def writeLower(self, str_output=None, **kwargs):
        self.indentLower()
        self.write(str_output, **kwargs)

    def indent(self, **kwargs):
        """
        Returns the actual string of spaces that provides the correct indentation for the current line

        Optional Arguments
        ------------------
        myLevel: int
            Temporarily overrides the current indentation level
        mySize: int
            Temporarily overrides the current indentation size
        """
        if 'myLevel' in kwargs:
            indLevel = kwargs['myLevel']
        else:
            indLevel = self._properties['indentLevel']

        if 'mySize' in kwargs:
            indSize = kwargs['mySize']
        else:
            indSize = self._properties['indentSize']

        intIndent = indLevel * indSize

        return (" " * intIndent)

    @property
    def consoleMirror(self):
        """Sets a fixed boolean state for whether log output is mirrored to the console"""
        return self._properties['consoleMirror']

    @consoleMirror.setter
    def consoleMirror(self, newVal):
        self._properties['consoleMirror'] = newVal

    # %% File output functions

    def open(self, **kwargs):
        """
        Opens an actual file object for output.
        (If .open() is never called, then all log output is routed to the console.)

        Optional KW Arguments
        ---------------------
        fileName: string
        The name of the file to be opened. (If no extension is supplied, then '.log' is added.)

        strHeader: string
        Header string to be output at the top of the file
        """
        if not self._fOpen:

            if "root" in kwargs:
                myRoot = kwargs['root']
            else:
                myRoot = os.getcwd()
            if "relLoc" in kwargs:
                myRelLoc = kwargs['relLoc']
            else:
                myRelLoc = "logs\\"

            print("Attempting to open file")
            print("     myRoot: " + str(myRoot))
            print("     myRelLoc: " + str(myRelLoc))
            try:
                self._fM = fManager(myRoot, myRelLoc, **kwargs)
            except:
                print("ERROR: COULD NOT OPEN FILE")
                for kwarg in kwargs:
                    print("    " + kwarg + ": " + kwargs[kwarg])
                raise Exception(IOError)

            else:
                if 'strHeader' in kwargs:
                    self.write(kwargs['strHeader'])
                self._fOpen = True
                if not 'useHeader' in kwargs:
                    self.write("INITIATING LOG OUTPUT: " + self._currTime, padBefore=1, padAfter=1, console=True)
                else:
                    if kwargs['useHeader'] == "True":
                        self.write("INITIATING LOG OUTPUT: " + self._currTime, padBefore=1, padAfter=1, console=True)

    def write(self, strOutput=None, **kwargs):
        """
        Outputs one line directly to the log file, under the following conditions:
            - Prints directly to the log, without checking the current 'loggingLevel' threshold
            - Prints at the current indentation level (unless overridden with optional args)

        Optional Arguments
        ------------------
        padBefore, padAfter: int
            Cause x number of blank lines to be output before or after the current line is output
        console: boolean
            Causes the current line to also be printed to the console
        indentLevel, indentSize: int
            Locally override those settings for the current line
        prefix: str
            Will be added to the beginning of the current line before output, followed by ": "
        """

        if 'padBefore' in kwargs:
            try:
                for n in range(kwargs['padBefore']):
                    self._write()
            except:
                pass

        if 'indentLevel' in kwargs:
            self.indentLevel = kwargs['indentLevel']

        if 'indentSize' in kwargs:
            self.indentSize = kwargs['indentSize']

        if 'consoleMirror' in kwargs:
            self.consoleMirror = kwargs['consoleMirror']

        strIndent = self.indent(**kwargs)

        str_prefix = ""
        if 'prefix' in kwargs:
            str_prefix = kwargs['prefix'] + ": "

        tmp_str = ""
        if strOutput is not None:
            tmp_str = strIndent + str_prefix + strOutput

        self._write(tmp_str)

        try:
            if kwargs['console']:
                print(tmp_str)
        except:
            pass

        if 'padAfter' in kwargs:
            try:
                for n in range(kwargs['padAfter']):
                    self._write()
            except:
                pass

    def _write(self, str_out=None):
        if self._fOpen:
            if str_out is not None:
                self._fM.write(str_out)
                if self.consoleMirror:
                    print(str_out)
            else:
                self._fM.write()
                if self.consoleMirror:
                    print()
        else:
            if str_out is not None:
                print(str_out)
            else:
                print()

    # %% Logging level functions

    @property
    def loggingLevel(self):
        return self._loggingLevel

    @loggingLevel.setter
    def loggingLevel(self, new_val):
        # Check to see if an argument has been passed
        if new_val in self._loggingLevels:
            # If it is in the list, set this instance's new minimal logging threshold to the new value
            self._loggingLevel = new_val
        else:
            # If it's not in the list, raise and exception
            raise Exception("ERROR: Attempt to set log level to: " + new_val)

    def _lWrite(self, my_level, str_out=None, *args, **kwargs):
        if str_out is not None:
            if self._loggingLevels[my_level] >= self._loggingLevels[self._loggingLevel]:
                self.write(str_out, *args, **kwargs, prefix=my_level)

    def DEBUG(self, str_out=None, *args, **kwargs):
        """
        Will only log arguments at logging level:
            'DEBUG'
        """
        self._lWrite('DEBUG', str_out, *args, **kwargs)

    def INFO(self, str_out=None, *args, **kwargs):
        """
        Will log arguments at logging levels:
            'DEBUG', 'INFO'
        """
        self._lWrite('INFO', str_out, *args, **kwargs)

    def WARNING(self, str_out=None, *args, **kwargs):
        """
        Will log arguments at logging levels:
            'DEBUG', 'INFO', 'WARNING'
        """
        self._lWrite('WARNING', str_out, *args, **kwargs)

    def ERROR(self, str_out=None, *args, **kwargs):
        """
        Will log arguments at logging levels:
            'DEBUG', 'INFO', 'WARNING', 'ERROR'
        """
        self._lWrite('ERROR', str_out, *args, **kwargs)

    def CRITICAL(self, str_out=None, *args, **kwargs):
        """
        Will cause arguments to be logged at all logging levels:
            'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
        """
        self._lWrite('CRITICAL', str_out, *args, **kwargs)


# %% Shared objects

logMain = ClsLogger()

# %% Unit tests

if __name__ == '__main__':

    testBase = True
    testLevels = False
    testStress = False

    # %% Base tests

    if testBase:
        #        tmpLogger = ClsLogger(fileName = "log-test", fileExt = "log")
        tmpLogger = ClsLogger()
        tmpLogger.write()
        tmpLogger.write('Testing')
        tmpLogger.write('Indent 01', indentLevel=1)
        tmpLogger.write('Indent 02', indentLevel=2, padBefore=1, padAfter=2)
        tmpLogger.write('Testing Level 02')
        tmpLogger.write('Testing Temp Level', myLevel=0)
        tmpLogger.write('Testing Level 02')
        tmpLogger.indentLevel = 3
        tmpLogger.write('Testing Level 03')
        tmpLogger.indentSize = 10
        tmpLogger.write('Testing Level 03')

    # %% Logging level tests

    if testLevels:
        tmpLogger = ClsLogger(fileName="log-test", fileExt="log")

        tmpLogger.DEBUG("Test")
        tmpLogger.INFO("Test")
        tmpLogger.WARNING("Test")
        tmpLogger.ERROR("Test")
        tmpLogger.CRITICAL("Test")

        tmpLogger.write("New Threshold: " + tmpLogger.loggingLevel('DEBUG'), padBefore=1, padAfter=1)

        tmpLogger.DEBUG("Test")
        tmpLogger.INFO("Test")
        tmpLogger.WARNING("Test")
        tmpLogger.ERROR("Test")
        tmpLogger.CRITICAL("Test")

    # %% Stress tests

    if testStress:
        pass
