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
        indent_level: int
            Overrides default indentation level of 0
        indent_size: int
            Overrides default indentation size of 4 spaces
        logging_level: str
            Overrides default minimum logging_level of 'WARNING'
    """

    # %% Class constructor

    _loggingLevels = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3, "CRITICAL": 4}

    def __init__(self, **fargs):

        self._properties = {
            "indent_level": 0,
            "indent_size": 4,
            "console_mirror": False,
        }

        self._loggingLevel = "WARNING"

        self._currTime = strTimestamp

        self._fOpen = False

        for fArg in fargs:
            if fArg == "logging_level":
                if fArg["logging_level"] in self._loggingLevels:
                    self._loggingLevel = self._loggingLevels[fArg["logging_level"]]
                else:
                    raise Exception(
                        "ERROR: Attempt to set unknown Log Level: "
                        + fArg["logging_level"]
                    )
            else:
                self._properties[fArg] = fargs[fArg]

            if "fileName" in fargs:
                self.open(**fargs)

    # %% Property management functions

    @property
    def indent_level(self):
        """ Returns the current indent_level """
        return self._properties["indent_level"]

    @indent_level.setter
    def indent_level(self, newval: int):
        """ Sets the current indent_level """
        self._properties["indent_level"] = newval

    @property
    def indent_size(self):
        """
        Assigns or returns the current indent_size
        """
        return self._properties["indent_size"]

    @indent_size.setter
    def indent_size(self, new_val: int):
        """ Sets the current indent_size """
        self._properties["indent_size"] = new_val

    def indent_raise(self, *args):
        int_change = 1
        if args:
            if args[0] > 0:
                int_change = args[0]
            else:
                raise Exception("Attempt to raise indent level: " + args[0])
        new_level = self.indent_level + int_change
        self.indent_level = new_level

    def indent_lower(self, int_lower=None):
        """
        Forcefully lowers the current level of indentation
        Arguments
        ---------
            int_lower: int
                Optional: The number of levels by which indentation should be lowered (if not provided, =1)
        """
        if not int_lower:
            int_change = 1
        else:
            int_change = abs(int_lower)
        if int_change > self.indent_level:
            new_level = 0
        else:
            new_level = self.indent_level - int_change

        self.indent_level = new_level

    def write_raise(self, str_output=None, **kwargs):
        self.indent_raise()
        self.write(str_output, **kwargs)

    def write_lower(self, str_output=None, **kwargs):
        self.indent_lower()
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
        if "myLevel" in kwargs:
            ind_level = kwargs["myLevel"]
        else:
            ind_level = self._properties["indent_level"]

        if "mySize" in kwargs:
            ind_size = kwargs["mySize"]
        else:
            ind_size = self._properties["indent_size"]

        int_indent = ind_level * ind_size

        return " " * int_indent

    @property
    def console_mirror(self):
        """Sets a fixed boolean state for whether log output is mirrored to the console"""
        return self._properties["console_mirror"]

    @console_mirror.setter
    def console_mirror(self, new_val):
        self._properties["console_mirror"] = new_val

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
                my_root = kwargs["root"]
            else:
                my_root = os.getcwd()
            if "relLoc" in kwargs:
                my_rel_loc = kwargs["relLoc"]
            else:
                my_rel_loc = "logs\\"

            print("Attempting to open file")
            print("     my_root: " + str(my_root))
            print("     my_rel_loc: " + str(my_rel_loc))
            try:
                self._fM = fManager(my_root, my_rel_loc, **kwargs)
            except:
                print("ERROR: COULD NOT OPEN FILE")
                for kwarg in kwargs:
                    print("    " + kwarg + ": " + kwargs[kwarg])
                raise Exception(IOError)

            else:
                if "strHeader" in kwargs:
                    self.write(kwargs["strHeader"])
                self._fOpen = True
                if "useHeader" not in kwargs:
                    self.write(
                        "INITIATING LOG OUTPUT: " + self._currTime,
                        padBefore=1,
                        padAfter=1,
                        console=True,
                    )
                else:
                    if kwargs["useHeader"] == "True":
                        self.write(
                            "INITIATING LOG OUTPUT: " + self._currTime,
                            padBefore=1,
                            padAfter=1,
                            console=True,
                        )

    def write(self, str_output=None, **kwargs):
        """
        Outputs one line directly to the log file, under the following conditions:
            - Prints directly to the log, without checking the current 'logging_level' threshold
            - Prints at the current indentation level (unless overridden with optional args)

        Optional Arguments
        ------------------
        padBefore, padAfter: int
            Cause x number of blank lines to be output before or after the current line is output
        console: boolean
            Causes the current line to also be printed to the console
        indent_level, indent_size: int
            Locally override those settings for the current line
        prefix: str
            Will be added to the beginning of the current line before output, followed by ": "
        """

        if "padBefore" in kwargs:
            try:
                for n in range(kwargs["padBefore"]):
                    self._write()
            except:
                pass

        if "indent_level" in kwargs:
            self.indent_level = kwargs["indent_level"]

        if "indent_size" in kwargs:
            self.indent_size = kwargs["indent_size"]

        if "console_mirror" in kwargs:
            self.console_mirror = kwargs["console_mirror"]

        str_indent = self.indent(**kwargs)

        str_prefix = ""
        if "prefix" in kwargs:
            str_prefix = kwargs["prefix"] + ": "

        tmp_str = ""
        if str_output is not None:
            tmp_str = str_indent + str_prefix + str_output

        self._write(tmp_str)

        try:
            if kwargs["console"]:
                print(tmp_str)
        except:
            pass

        if "padAfter" in kwargs:
            try:
                for n in range(kwargs["padAfter"]):
                    self._write()
            except:
                pass

    def _write(self, str_out=None):
        if self._fOpen:
            if str_out is not None:
                self._fM.write(str_out)
                if self.console_mirror:
                    print(str_out)
            else:
                self._fM.write()
                if self.console_mirror:
                    print()
        else:
            if str_out is not None:
                print(str_out)
            else:
                print()

    # %% Logging level functions

    @property
    def logging_level(self):
        return self._loggingLevel

    @logging_level.setter
    def logging_level(self, new_val):
        # Check to see if an argument has been passed
        if new_val in self._loggingLevels:
            # If it is in the list, set this instance's new minimal logging threshold to the new value
            self._loggingLevel = new_val
        else:
            # If it's not in the list, raise and exception
            raise Exception("ERROR: Attempt to set log level to: " + new_val)

    def _lwrite(self, my_level, str_out=None, *args, **kwargs):
        if str_out is not None:
            if self._loggingLevels[my_level] >= self._loggingLevels[self._loggingLevel]:
                self.write(str_out, *args, **kwargs, prefix=my_level)

    # noinspection PyPep8Naming
    def DEBUG(self, str_out=None, *args, **kwargs):
        """
        Will only log arguments at logging level:
            'DEBUG'
        """
        self._lwrite("DEBUG", str_out, *args, **kwargs)

    # noinspection PyPep8Naming
    def INFO(self, str_out=None, *args, **kwargs):
        """
        Will log arguments at logging levels:
            'DEBUG', 'INFO'
        """
        self._lwrite("INFO", str_out, *args, **kwargs)

    # noinspection PyPep8Naming
    def WARNING(self, str_out=None, *args, **kwargs):
        """
        Will log arguments at logging levels:
            'DEBUG', 'INFO', 'WARNING'
        """
        self._lwrite("WARNING", str_out, *args, **kwargs)

    # noinspection PyPep8Naming
    def ERROR(self, str_out=None, *args, **kwargs):
        """
        Will log arguments at logging levels:
            'DEBUG', 'INFO', 'WARNING', 'ERROR'
        """
        self._lwrite("ERROR", str_out, *args, **kwargs)

    # noinspection PyPep8Naming
    def CRITICAL(self, str_out=None, *args, **kwargs):
        """
        Will cause arguments to be logged at all logging levels:
            'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
        """
        self._lwrite("CRITICAL", str_out, *args, **kwargs)


# %% Shared objects

logMain = ClsLogger()

# %% Unit tests

if __name__ == "__main__":

    testBase = True
    testLevels = False
    testStress = False

    # %% Base tests

    if testBase:
        #        tmpLogger = ClsLogger(fileName = "log-test", fileExt = "log")
        tmpLogger = ClsLogger()
        tmpLogger.write()
        tmpLogger.write("Testing")
        tmpLogger.write("Indent 01", indentLevel=1)
        tmpLogger.write("Indent 02", indentLevel=2, padBefore=1, padAfter=2)
        tmpLogger.write("Testing Level 02")
        tmpLogger.write("Testing Temp Level", myLevel=0)
        tmpLogger.write("Testing Level 02")
        tmpLogger.indent_level = 3
        tmpLogger.write("Testing Level 03")
        tmpLogger.indent_size = 10
        tmpLogger.write("Testing Level 03")

    # %% Logging level tests

    if testLevels:
        tmpLogger = ClsLogger(fileName="log-test", fileExt="log")

        tmpLogger.DEBUG("Test")
        tmpLogger.INFO("Test")
        tmpLogger.WARNING("Test")
        tmpLogger.ERROR("Test")
        tmpLogger.CRITICAL("Test")

        # tmpLogger.write("New Threshold: " + tmpLogger.logging_level('DEBUG'), padBefore=1, padAfter=1)

        tmpLogger.DEBUG("Test")
        tmpLogger.INFO("Test")
        tmpLogger.WARNING("Test")
        tmpLogger.ERROR("Test")
        tmpLogger.CRITICAL("Test")

    # %% Stress tests

    if testStress:
        pass
