"""
Create a new Project
"""
from copy import deepcopy
from pathlib import Path

from phases.commands.run import Run
from pyPhases import Project


class Updatedatafilenames(Run):
    """create a Phase-Project"""

    def parseRunOptions(self):
        super().parseRunOptions()
        self.version = "current"
        self.dataFolder = "data"
        if "<dataid>" in self.options:
            self.what = self.options["<dataid>"]

        if self.options["-ver"]:
            self.version = self.options["<version>"]

    def run(self):
        self.parseRunOptions()
        self.prepareConfig()

        project = self.createProjectFromConfig(self.config)
        self.backupConfig = deepcopy(project.config)

        dataNames = project.dataNames if self.what is None else [self.what]

        dataOverview = {}
        for dataName in dataNames:
            dataId = project.getDataFromName(dataName, self.version).getDataId()

            path = Path(self.dataFolder) / dataId
            self.log(f"Checking {path}")
            if Path(path).exists():
                dataOverview[dataName] = {"old": dataId}
                
        
        if len(dataOverview) == 0:
            self.log("No data requires updates.")
            return
        
        self.log("Following data files exist:")
        for dataName, dataId in dataOverview.items():
            self.log(f"{dataName}: {dataId['old']}")

        # ask the user to change the config files and press enter
        self.log("Please change the config files and make sure that all listed datanames exist in the changed project. Press enter to continue and show potential changes.")

        input()

        self.prepareConfig()
        project2 = self.createProjectFromConfig(self.config)
        
        for dataName in dataNames:
            dataId = project2.getDataFromName(dataName, self.version).getDataId()

            path = Path(self.dataFolder) / dataId
            existInNew = Path(path).exists()

            if dataName not in dataOverview:
                continue

            if existInNew:
                del dataOverview[dataName]
            else:
                dataOverview[dataName]["new"] = dataId

        self.log("Following data files will be moved:")
        for dataName, dataId in dataOverview.items():
            self.log(f"{dataName}: {dataId['old']} -> {dataId['new']}")
        
        # ask the user to confirm the changes
        self.log("Please confirm the changes. Type y to move the files.")
        if input() == "y":
            for dataName, dataId in dataOverview.items():
                path = Path(self.dataFolder) / dataId["old"]
                newPath = Path(self.dataFolder) / dataId["new"]
                path.rename(newPath)
                self.log(f"Moved {path} to {newPath}")
        else:
            self.log("No changes were made.")