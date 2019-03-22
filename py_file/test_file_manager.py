import os
import unittest

import file_manager


class MyTestCase(unittest.TestCase):
    def test_paths(self):

        print("Root: " + test_file_manager.root)
        print("relLoc: " + test_file_manager.relLoc)
        print("absLoc: " + test_file_manager.absLoc)

        print("fileName: " + test_file_manager.fileName)
        print("fileExt: " + test_file_manager.fileExt)

        print("relPath: " + test_file_manager.relPath)
        print("absPath: " + test_file_manager.absPath)

        test_file_manager.relLoc = "newtestdir\\newtestsub\\"
        print("New relLoc: " + test_file_manager.relLoc)
        print("New relPath: " + test_file_manager.relPath)
        print("New absLoc: " + test_file_manager.absLoc)
        print("New absPath: " + test_file_manager.absPath)

        assert True

        # %% Stress tests

    def test_stress(self):
        test_file_manager.relLoc = "\\test-left"
        print(test_file_manager.relLoc)
        test_file_manager.relLoc = "\\test-both\\"
        print(test_file_manager.relLoc)
        test_file_manager.relLoc = "test-right\\"
        print(test_file_manager.relLoc)
        test_file_manager.relLoc = "test-none"
        print(test_file_manager.relLoc)
        test_file_manager.relLoc = "test-parent\\test-child"
        print(test_file_manager.relLoc)

        test_file_manager.fileName = "log-test"
        print(test_file_manager.fileName)
        test_file_manager.fileName = "log-test.htm"
        print(test_file_manager.fileName)
        test_file_manager.fileExt = ".csv"
        print(test_file_manager.fileExt)
        test_file_manager.fileExt = "txt"
        print(test_file_manager.fileExt)

        assert True

    def test_file_out(self):
        test_file_manager.write("sadasdasd")

        assert True


if __name__ == "__main__":
    tmpAbsLoc = os.getcwd()
    tmpRelLoc = "testsub\\"
    test_file_manager = file_manager.fManager(
        tmpAbsLoc, tmpRelLoc, fileName="log-test.log"
    )

    unittest.main()
