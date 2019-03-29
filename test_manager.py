import os

import pytest
import logger

import file_manager


def test_paths():
    tfm = file_manager.fManager(
        fileName="log-test.log", myRoot=os.getcwd(), myRelLoc="testsub\\"
    )

    print("Root: " + tfm.root)

    print("fileName: " + tfm.fileName)
    print("fileExt: " + tfm.fileExt)

    print("relPath: " + tfm.relPath)
    print("absPath: " + tfm.absPath)

    tfm.relLoc = "newtestdir\\newtestsub\\"
    print("New relLoc: " + tfm.relLoc)
    print("New relPath: " + tfm.relPath)
    print("New absLoc: " + tfm.absLoc)
    print("New absPath: " + tfm.absPath)

    assert True

    # %% Stress tests


def test_stress():
    tfm = file_manager.fManager(
        fileName="log-test.log", myRoot=os.getcwd(), myRelLoc="testsub\\"
    )

    tfm.relLoc = "\\test-left"
    print(tfm.relLoc)
    tfm.relLoc = "\\test-both\\"
    print(tfm.relLoc)
    tfm.relLoc = "test-right\\"
    print(tfm.relLoc)
    tfm.relLoc = "test-none"
    print(tfm.relLoc)
    tfm.relLoc = "test-parent\\test-child"
    print(tfm.relLoc)

    tfm.fileName = "log-test"
    print(tfm.fileName)
    tfm.fileName = "log-test.htm"
    print(tfm.fileName)
    tfm.fileExt = ".csv"
    print(tfm.fileExt)
    tfm.fileExt = "txt"
    print(tfm.fileExt)

    assert True


def test_file_out():
    tfm = file_manager.fManager(
        fileName="log-test.log", myRoot=os.getcwd(), myRelLoc="testsub\\"
    )

    tfm.write("sadasdasd")

    assert True


def testBase():
    tmpLogger = logger.ClsLogger(fileName="log-test", fileExt="log")
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

    assert True


def testLevels():
    tmpLogger = logger.ClsLogger(fileName="log-test", fileExt="log")

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

    assert True


if __name__ == "__main__":
    test_stress()
    # test_paths()
    testBase()
    testLevels()
    test_file_out()
