import os

from pathlib import PurePosixPath, PureWindowsPath

# from py_log.log_decorators import dec_log_entry_exit


def isPosixPath(myPath):
    return ("/" in str(myPath))


# @dec_log_entry_exit
class objPath():
    def __init__(self, myPath, isPosix=False):
        self._isPosix = isPosix
        self._parts = None
        self.path = myPath

    @property
    def isPosix(self):
        return self._isPosix

    @property
    def path(self):
        if self.isPosix:
            # logMain.DEBUG("OS: Posix")
            return str(PurePosixPath(*self._parts))
        else:
            # logMain.DEBUG("OS: Windows")
            return str(PureWindowsPath(*self._parts))

    @path.setter
    def path(self, newPath):
        if isPosixPath(newPath):
            self._parts = PurePosixPath(newPath).parts
        else:
            self._parts = PureWindowsPath(newPath).parts

        # logMain.DEBUG(("New Path Assigned: " + newPath), padBefore=1)
        # logMain.indent_raise()
        # for p in self._parts:
        #     logMain.DEBUG(p)
        # logMain.indent_lower()


# @dec_log_entry_exit
class objLoc():
    def __init__(self, myRoot, myPath):
        self._isPosix = isPosixPath(myRoot)
        if self.isPosix:
            self._root = PurePosixPath(myRoot)
        else:
            self._root = PureWindowsPath(myRoot)
        self._relpath = objPath(myPath, self.isPosix)
        pass

    @property
    def isPosix(self):
        return self._isPosix

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, newRoot):
        self._root = newRoot

    @property
    def relPath(self):
        return self._relpath.path

    @relPath.setter
    def relPath(self, newRelPath):
        self._relpath.path = newRelPath

    @property
    def path(self):
        return os.path.join(self.root, self.relPath)


if __name__ == "__main__":

    from py_log.logger import logMain

    # logMain.open(fileName='path-log')
    logMain.console_mirror = True
    logMain.logging_level = 'DEBUG'

    testUnits = {}
    testUnits['baseTest'] = False
    testUnits['multiTest'] = True

    if testUnits['baseTest']:
        tmpLoc = "Dev\\TestLoc\\Test"
        tmpPath = objPath(tmpLoc)
        logMain.INFO("Output Path: " + tmpPath.path)

        tmpLoc = "Dev/TestLoc/Test"
        tmpPath = objPath(tmpLoc)
        logMain.INFO("Output Path: " + tmpPath.path)

    if testUnits['multiTest']:
        # @dec_log_entry_exit
        def testPath(strRoot, strLoc):
            """
            Tests various flavors of base string

            Arguments
            ---------
            pathTemp: string
            Path to be used for testing
            """
            myLoc = objLoc(strRoot, strLoc)
            logMain.write("Base Path: " + str(myLoc.root), padBefore=1)
            logMain.write("Location: " + myLoc.path)

        tmpLoc = "Dev\\TestLoc"
        testPath("C:\\Users\\lstanevich\\Dropbox (Fluency Media)\\Fluency - Beaumont Content\\Beaumont.org Content Migration", tmpLoc)
        testPath("/Users/lstanevich/Dropbox (Fluency Media)/Fluency - Beaumont Content/Beaumont.org Content Migration", tmpLoc)
        # testPath(str(PurePath.cwd()), tmpLoc)
        # myTest = objPath("C:\\Users\\lstanevich\\Dropbox (Fluency Media)\\Fluency - Beaumont Content\\Beaumont.org Content Migration")
