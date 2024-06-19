import unittest
from pathlib import Path

from phases.commands.create import Create
from phases.commands.run import Run
from tests.acceptance.test_create import TestCreate


class TestCompleteRun(unittest.TestCase):
    """create a project and run it"""

    projectFolder = "tests/data-gen"
    configFile = "tests/data/min.yaml"

    pass

    # @classmethod
    # def setUpClass(cls):
    #     testrun = Run({})
    #     path = Path(cls.projectFolder)
    #     if path.exists():
    #         return

    #     path = Path(cls.projectFolder)
    #     createCmd = Create(
    #         {
    #             "-p": cls.configFile,
    #             "-o": cls.projectFolder,
    #             "-f": True,
    #         }
    #     )
    #     createCmd.run()
    #     assert path.exists() is True

    #     TestCreate().testCreateProjectSimple()

    # def test_runProjectSimple(self):

    #     runCmd = Run(
    #         {
    #             "-p": self.configFile,
    #             "-o": self.projectFolder,
    #             "-v": False,
    #             "phaseName": None,
    #             "-c": None,
    #             "--set": None,
    #         }
    #     )
    #     runCmd.run()
