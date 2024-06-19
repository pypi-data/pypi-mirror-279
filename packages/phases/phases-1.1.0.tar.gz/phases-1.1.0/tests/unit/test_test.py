import os
from unittest import TestCase, TestSuite, TextTestRunner
from unittest.loader import TestLoader
from unittest.mock import MagicMock, call, patch

from pyPhases.test import TestCase as PyPhaseTestCase
from pyPhases.test import TestCaseIntegration

from phases.commands.test import Test


class TestTest(TestCase):
    def test_parseRunOptions_default(self):
        """Test that the run options are parsed correctly"""
        test = Test({})

        self.assertEqual(test.testDir, "tests")
        self.assertEqual(test.testPattern, "test*.py")
        self.assertEqual(test.failFast, False)

    def test_parseRunOptions(self):
        """Test that the run options are parsed correctly"""
        test = Test({})
        test.options = {
            "<testdir>": "myTests",
            "<testpattern>": "*Test.py",
            "-f": "doesntmatter",
            # base options
            "-o": "output",
            "-p": "p",
            "-c": "c",
            "--set": "s",
            "-v": False,
        }

        test.parseRunOptions()

        self.assertEqual(test.outputDir, "output")
        self.assertEqual(test.testDir, "output/myTests")
        self.assertEqual(test.testPattern, "*Test.py")
        self.assertEqual(test.failFast, True)

    def test_wrapTest(self):
        """Test that the tests are wrapped in a suite"""
        test = Test({})

        wrap = MagicMock(return_value=True)
        test1 = MagicMock()

        tests = test.wrapTestsInSuite(test1, wrap)

        self.assertEqual(len(tests), 1)
        self.assertEqual(tests, [test1])
        wrap.assert_has_calls([call(test1)])

    def test_wrapTestsInSuite(self):
        """Test that the tests are wrapped in a suite"""
        test = Test({})

        wrap = MagicMock(return_value=True)
        test1, test2 = MagicMock(), MagicMock()
        testsuite = TestSuite([test1, test2])

        tests = test.wrapTestsInSuite(testsuite, wrap)

        self.assertEqual(len(tests), 2)
        self.assertEqual(tests, [test1, test2])
        wrap.assert_has_calls([call(test1), call(test2)])

    def getDefaultTestRun(self):
        test = Test({})

        test.testDir = "myTestDir"
        test.testPattern = "test*.py"
        test.failFast = True

        project = MagicMock()
        test.beforeRun = MagicMock()
        test.prepareConfig = MagicMock()
        test.createProjectFromConfig = MagicMock(return_value=project)

        class ExampleTest(TestCase):
            phase = MagicMock()

        test1, test2 = MagicMock(), ExampleTest()
        testSuite = TestSuite([test1, test2])
        TestLoader.loadTestsFromName = MagicMock(return_value=testSuite)
        TestLoader.discover = MagicMock(return_value=testSuite)
        TextTestRunner.failFast = MagicMock()
        TextTestRunner.run = MagicMock()

        return test, project

    @patch("os.chdir")
    @patch("os.path.isdir", return_value=True)
    def test_runTestsFromDir(self, chdirmock, isdirmock):
        """Test that the tests are run"""

        test, project = self.getDefaultTestRun()

        test.run()

        self.assertEqual(PyPhaseTestCase.project, project)
        test.beforeRun.assert_called_once()
        test.prepareConfig.assert_called_once()
        TestLoader.loadTestsFromName.assert_not_called()
        TestLoader.discover.assert_called_with("myTestDir", "test*.py")
        TextTestRunner.run.assert_called_once()
        chdirmock.assert_called_once_with("myTestDir")

    @patch("os.chdir")
    @patch("os.path.isdir", return_value=False)
    def test_runTestsFromName(self, chdirmock, isdirmock):
        """Test that the tests are run"""

        test, project = self.getDefaultTestRun()

        test.run()

        self.assertEqual(PyPhaseTestCase.project, project)
        test.beforeRun.assert_called_once()
        test.prepareConfig.assert_called_once()
        TestLoader.loadTestsFromName.assert_called_with("myTestDir")
        TestLoader.discover.assert_not_called()
        TextTestRunner.run.assert_called_once()
        chdirmock.assert_called_once_with("myTestDir")
