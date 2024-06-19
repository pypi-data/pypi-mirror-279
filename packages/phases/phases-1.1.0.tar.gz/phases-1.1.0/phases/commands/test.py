import os
import sys
from pathlib import Path
from unittest import TextTestRunner
from unittest.loader import TestLoader
from unittest.suite import TestSuite

from pyPhases.test import TestCase, TestCaseIntegration

from phases.commands.run import Run


class Test(Run):
    """test a Phase-Project by wrapping TestCases from pyPhase with the project and a configfile specified in project.test.yaml"""

    def __init__(self, options, *args, **kwargs):
        super().__init__(options, *args, **kwargs)
        self.testDir = "tests"
        self.failFast = False
        self.testPattern = "test*.py"

    def parseRunOptions(self):
        super().parseRunOptions()
        if self.options["<testdir>"]:
            self.testDir = Path(self.outputDir).joinpath(self.options["<testdir>"]).as_posix()
            sys.path.insert(0, self.testDir)
            self.logDebug(f"Set Testdir: {self.testDir}")
        if self.options["<testpattern>"]:
            self.testPattern = self.options["<testpattern>"]
        if self.options["-f"]:
            self.failFast = True

    def wrapTestsInSuite(self, testOrSuite, wrapMethod):
        tests = []
        if isinstance(testOrSuite, TestSuite):
            for subTestOrSuite in testOrSuite._tests:
                tests += self.wrapTestsInSuite(subTestOrSuite, wrapMethod)
        elif wrapMethod(testOrSuite):
            tests = [testOrSuite]
        return tests

    def run(self):
        self.beforeRun()
        self.prepareConfig()

        project = self.createProjectFromConfig(self.config)
        TestCase.project = project

        loader = TestLoader()
        self.logDebug(f"Discover Tests in {self.testDir} for pattern {self.testPattern} (Basedir: {self.outputDir})")
        os.chdir(self.outputDir)

        if os.path.isdir(self.testDir):
            suite = loader.discover(self.testDir, self.testPattern)
        else:
            suite = loader.loadTestsFromName(self.testDir)

        self.logDebug(f"Found Tests: {suite._tests}")

        def wrapTestsInSuite(test):
            return not isinstance(test, TestCaseIntegration)

        noIntegrationTests = self.wrapTestsInSuite(suite, wrapTestsInSuite)

        suite = TestSuite()
        suite.addTests(noIntegrationTests)
        runner = TextTestRunner()
        runner.failfast = self.failFast
        result = runner.run(suite)

        print(result)
        if len(result.errors) > 0 or len(result.failures):
            sys.exit("Test failed")
