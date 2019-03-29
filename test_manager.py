import os

# noinspection PyUnresolvedReferences
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


def test_base():
    tmp_logger = logger.ClsLogger(fileName="log-test", fileExt="log")
    tmp_logger.write()
    tmp_logger.write("Testing")
    tmp_logger.write("Indent 01", indentLevel=1)
    tmp_logger.write("Indent 02", indentLevel=2, padBefore=1, padAfter=2)
    tmp_logger.write("Testing Level 02")
    tmp_logger.write("Testing Temp Level", myLevel=0)
    tmp_logger.write("Testing Level 02")
    tmp_logger.indent_level = 3
    tmp_logger.write("Testing Level 03")
    tmp_logger.indent_size = 10
    tmp_logger.write("Testing Level 03")

    assert True


def test_levels():
    tmp_logger = logger.ClsLogger(fileName="log-test", fileExt="log")

    tmp_logger.DEBUG("Test")
    tmp_logger.INFO("Test")
    tmp_logger.WARNING("Test")
    tmp_logger.ERROR("Test")
    tmp_logger.CRITICAL("Test")

    # tmp_logger.write("New Threshold: " + tmp_logger.logging_level('DEBUG'), padBefore=1, padAfter=1)

    tmp_logger.DEBUG("Test")
    tmp_logger.INFO("Test")
    tmp_logger.WARNING("Test")
    tmp_logger.ERROR("Test")
    tmp_logger.CRITICAL("Test")

    assert True


if __name__ == "__main__":
    test_stress()
    test_paths()
    test_base()
    test_levels()
    test_file_out()
