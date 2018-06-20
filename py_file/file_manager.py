# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 22:53:00 2016

@author: lstanevich
"""

import os

from py_file.path_manager import objLoc


class fWriter:
    """
    Base class to manage file output -- meant to be attached to 'fManager' class objects
    """

    def __init__(self, fManager):
        """
        Constructor for fWriter class objects

        Arguments
        ---------
        fManager: fManager()
            Parent fManager object
        """

        self._fM = fManager
#        print()
#        print(" ----- Constructing fWriter -----")
#
        if not os.path.isdir(self._fM.absLoc):
            print("CREATING ABSOLUTE LOCATION: " + self._fM.absLoc)

        # Ensure that the corresponding destination directory exists
        os.makedirs(self._fM.absLoc, exist_ok=True)

        print("     fileName: " + self._fM.fileName)

        try:
            self._fOut = open(self._fM.absPath, 'w', newline="\n")
        except:
            print('ERROR: COULD NOT OPEN FILE FOR OUTPUT')
            print('    ROOT: ' + self._fM.root)
            print('    RELPATH: ' + self._fM.relPath)
            print('    FILENAME: ' + self._fM.fileName)
            print('    ABS LOC: ' + self._fM.absLoc)
            print('    ABS PATH: ' + self._fM.absPath)
            raise Exception('ERROR: COULD NOT OPEN FILE FOR OUTPUT')
#        with open(self._fM.absLoc , self._fM.fileName, 'w', newline='') as _fOut:
#            _fOut.write("Test")

    def write(self, strOut=None):
        """
        Output method for 'fWriter' class objects

        Arguments
        ---------
        *args: fManager()
            Parent fManager object
        """

        if strOut is not None:
            self._fOut.write(strOut + '\n')
        else:
            self._fOut.write('\n')
        self._fOut.flush()

#%% CLASS


class fManager:
    """
    Base class to manage file interactions
    """


#%% Class constructor

    def __init__(self, myRoot, myRelLoc, **fileArgs):
        """
        Constructor for fManager class objects

        Required Arguments
        ---------
        myRoot: string
            Absolute base path for files
        myRelLoc: string
            Relative child path for files
            DEFAULT: 'logs'

        Optional KW Arguments
        ------------------
        fileName: string
            Log file name
            DEFAULT: 'log-main'
        fileExt: String
            File extension for log
            DEFAULT: 'log' / '.log'
        isMutable: Boolean
            Whether or not file information can be changed
            DEFAULT: False
        """

        # Create a per-instance dict to store local properties
        self._properties = {}
        self._location = objLoc(myRoot, myRelLoc)
        self._properties['fileName'] = "tempfile"
        self._properties['fileExt'] = ".log"
        self._isMutable = False

        # Traverse through any kw arguments that were passed
        for fileArg in fileArgs:

            # If it's a "known" argument, then process it
            if fileArg in self._properties:
                # Check if the property needs to be passed through its dedicated handler
                if fileArg == "fileName":
                    self.fileName = fileArgs[fileArg]
                elif fileArg == "fileExt":
                    self.fileExt = fileArgs[fileArg]
                else:
                    self._properties[fileArg] = fileArgs[fileArg]
            else:
                print(" UNKNOWN PROPERTY: [" + fileArg + "] --> " + fileArgs[fileArg])
                # raise Exception(" UNKNOWN PROPERTY: [" + fileArg + "] --> " + fileArgs[fileArg])

        self._fWriter = fWriter(self)


#%% Property interface functions

    @property
    def loc(self):
        return self._location

    # Dedicated method exposed to process root path property
    @property
    def root(self):
        """
        Returns 'root' property of attached objLoc
        """
        return str(self.loc.root)

    @root.setter
    def root(self, newRoot):
        self._properties['root'] = newRoot

    # Dedicated method exposed to process path property
    @property
    def relLoc(self):
        """
        Manages 'relPath' property (NOT including filename)
        """
        return str(self.loc.relPath)

    @relLoc.setter
    def relLoc(self, newRelLoc):
        """
        Arguments
        ---------
        newRelLoc: string
            Relative child path for log files ( under self.root )
        """
        self.loc.relPath = newRelLoc

    @property
    def fileName(self):
        """
        Manages 'fileName' property

        Arguments
        ---------
        fileName: string
            Log file name
            DEFAULT: 'log-main'
        """
        return self._properties['fileName'] + self.fileExt

    @fileName.setter
    def fileName(self, newFName):
        if '.' in newFName:
            self._properties['fileName'] = newFName.split('.')[0]
            self.fileExt = '.' + newFName.split('.')[1]
        else:
            self._properties['fileName'] = newFName

    @property
    def fileExt(self):
        """
        Manages 'fileExt' property

        Arguments
        ---------
        fileExt: String
            File extension for log
            DEFAULT: 'log' / '.log'
        """
        return self._properties['fileExt']

    @fileExt.setter
    def fileExt(self, newFExt):
        if not newFExt[0] == '.':
            newFExt = '.' + newFExt
        self._properties['fileExt'] = newFExt

    @property
    def relPath(self):
        """
        Returns complete relative path to file (including filename)

        Arguments
        ---------
        self.relLoc+self.fileName
        """
        return os.path.join(self.relLoc, self.fileName)

    @property
    def absLoc(self):
        """
        Returns complete absolute path to directory containing file (NOT including filename)

        Returns
        -------
        self.root+self.relLoc
        """
        return self.loc.path

    @property
    def absPath(self):
        """
        Returns complete absolute path to file (including filename)

        Returns
        -------
        self.root+self.relPath
        """
        return os.path.join(self.absLoc, self.fileName)


#%% File I/O functions

    def write(self, strOut=None):
        """
        Raises 'write' method from attached fWriter() object

        ARGUMENTS
        ---------
        strOut: string
            All args are passed directly through to self._fWriter()
        """
        self._fWriter.write(strOut)


#%% Unit tests

if __name__ == '__main__':

    testPaths = True
    testStress = True
    testFileOut = True

    tmpAbsLoc = os.getcwd()
    tmpRelLoc = "testsub\\"

#%% Path tests

    if testPaths:
        tmpPaths = fManager(tmpAbsLoc, tmpRelLoc, fileName="log-test.log")

        print("Root: " + tmpPaths.root)
        print("relLoc: " + tmpPaths.relLoc)
        print("absLoc: " + tmpPaths.absLoc)

        print("fileName: " + tmpPaths.fileName)
        print("fileExt: " + tmpPaths.fileExt)

        print("relPath: " + tmpPaths.relPath)
        print("absPath: " + tmpPaths.absPath)

        tmpPaths.relLoc = "newtestdir\\newtestsub\\"
        print("New relLoc: " + tmpPaths.relLoc)
        print("New relPath: " + tmpPaths.relPath)
        print("New absLoc: " + tmpPaths.absLoc)
        print("New absPath: " + tmpPaths.absPath)


#%% Stress tests

    if testStress:
        tmpPaths = fManager(tmpAbsLoc, tmpRelLoc, fileName="log-test")

        tmpPaths.relLoc = '\\test-left'
        print(tmpPaths.relLoc)
        tmpPaths.relLoc = '\\test-both\\'
        print(tmpPaths.relLoc)
        tmpPaths.relLoc = 'test-right\\'
        print(tmpPaths.relLoc)
        tmpPaths.relLoc = 'test-none'
        print(tmpPaths.relLoc)
        tmpPaths.relLoc = 'test-parent\\test-child'
        print(tmpPaths.relLoc)

        tmpPaths.fileName = 'log-test'
        print(tmpPaths.fileName)
        tmpPaths.fileName = 'log-test.htm'
        print(tmpPaths.fileName)
        tmpPaths.fileExt = '.csv'
        print(tmpPaths.fileExt)
        tmpPaths.fileExt = 'txt'
        print(tmpPaths.fileExt)


#%% File output tests

    if testFileOut:
        tmpWriteTest = fManager(tmpAbsLoc, tmpRelLoc, fileName='file-test')
        tmpWriteTest.write("sadasdasd")
