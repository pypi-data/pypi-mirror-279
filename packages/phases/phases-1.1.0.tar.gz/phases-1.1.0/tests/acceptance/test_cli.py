import sys
import unittest
from unittest.mock import patch

import pyPhases
from pyPhases import Logger
from pyPhases.test import mockLogger

import phases
import phases.commands
from phases.cli import main


class TestPhasesModule(unittest.TestCase):
    @patch("phases.commands.run.Run.run")
    @patch("phases.commands.Base.Base.run")
    @patch.object(sys, "exit")
    @mockLogger
    def test_version(self, mockLogger, exitmock, basemock, runmock):
        # Arrange
        sys.argv = ["phases", "--version"]
        expected_output = "Phases %s with pyPhases %s (Log level: %s)" % (
            phases.__version__,
            pyPhases.__version__,
            Logger.verboseLevel,
        )

        main()

        mockLogger.assertLogMessageLike(expected_output)
        runmock.assert_not_called()
        # exitmock.assert_not_called()
        # basemock.assert_not_called()

    @patch("phases.commands.run.Run.run")
    @patch("phases.commands.Base.Base.run")
    @patch.object(sys, "exit")
    @mockLogger
    def test_run(self, mockLogger, exitmock, basemock, runmock):
        # Arrange
        sys.argv = ["phases", "run", "test"]

        main()

        mockLogger.assertLogMessageLike("Run Command Run")
        runmock.assert_called_once()
        exitmock.assert_called_once()
        basemock.assert_not_called()
