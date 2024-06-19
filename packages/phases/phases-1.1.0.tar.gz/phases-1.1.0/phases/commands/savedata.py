"""
Create a new Project
"""

from distutils.file_util import copy_file
import os
import sys
from distutils.dir_util import copy_tree
from pathlib import Path

from phases.commands.Base import Base
from pyPhases import Project
from .run import Run


class Savedata(Run):
    """create a Phase-Project"""

    def parseRunOptions(self):
        super().parseRunOptions()
        self.dataname = self.options["<dataname>"]
        self.datafile = self.options["<datafile>"]
        self.datadir = "." if self.options["<datadir>"] is None else self.options["<datadir>"]


    def run(self):
        self.beforeRun()
        self.prepareConfig()

        project = self.createProjectFromConfig(self.config)
        self.copyData(project, self.dataname, self.datafile, self.datadir)

    def copyData(self, project: Project, dataname, dataFile, dataDir):
        """copy the data from the dataDir to the projectDir"""
        dataObj = project.getDataFromName(dataname)
        dataId = dataObj.getDataId()

        copy_file(dataFile, f"{dataDir}/{dataId}")
        self.logSuccess(f"Data {dataname} saved to {dataDir}/{dataId}")
