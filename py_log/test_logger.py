import pytest
import logger


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
