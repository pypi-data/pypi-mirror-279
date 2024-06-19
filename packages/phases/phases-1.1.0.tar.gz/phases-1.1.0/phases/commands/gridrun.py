import random
from math import floor

import pyPhases
import yaml
from pyPhases import Project, pdict, CSVLogger

from phases.commands.run import Run


class Gridrun(Run):
    """run a grid search"""

    def __init__(self, options, *args, **kwargs):
        super().__init__(options, *args, **kwargs)
        self.resume = True
        self.writer = None
        self.runSettings = None
        self.csvLogFile = "output.csv"

    def parseRunOptions(self):
        super().parseRunOptions()
        if self.options["<gridfile>"]:
            self.projectGridFile = self.options["<gridfile>"].strip()
            self.logDebug("Set Gridfile file: %s" % (self.projectGridFile))
        if self.options["--csv"]:
            self.csvLogFile = self.options["--csv"]
            self.logDebug("Set CSV log file: %s" % (self.csvLogFile))
        if self.options["-r"]:
            self.resume = False

    def getGrid(self, config, path=None, grid=None):
        path = path or []
        grid = [] if grid is None else grid
        config = pdict(config)
        for field in config:
            value = config[field]
            p = path + [field]
            key = field

            if isinstance(value, dict):
                self.getGrid(config[key], p, grid)
            elif isinstance(value, list):
                grid.append((p, value))
            else:
                raise Exception("grid value (%s) not well formed, the first non-dict value needs to be an array" % (path))

        return grid

    def prepareGridFile(self):
        gridFile = open(self.projectGridFile, "r")
        yamlContent = gridFile.read()
        gridFile.close()

        gridConfig = yaml.load(yamlContent, Loader=yaml.SafeLoader)
        if "grid" not in gridConfig:
            raise Exception("The gridfile needs to have the value 'grid' specified")

        self.runSettings = {"parallel": False, "random": False, "seed": 5, "maxruns": 0}

        for _, field in enumerate(gridConfig):
            if field != "grid":
                if field not in self.runSettings:
                    self.logWarning("The run option %s is unknown and will be ignored" % field)
                else:
                    self.runSettings[field] = gridConfig[field]

        return self.getGrid(gridConfig["grid"], [], [])

    def flattenGrid(self, grid):

        stackSize = 1
        parameterStackingSizes = []
        flattenGrid = []

        # iterate of all Arrays, get the total count of method calls, and update non-array parameter to arrays

        for configPath, gridArray in grid:
            configValues = gridArray
            parameterStackingSizes.append(stackSize)
            stackSize *= len(configValues)

        for i in range(stackSize):

            parameterStack = []
            # get the current Index
            for valueIndex, (configPath, configValues) in enumerate(grid):
                arrayLength = len(configValues)

                # divide be previous stack size, so that it only increase if the prev. stack is finished
                prevStackSize = parameterStackingSizes[valueIndex]
                x = i if prevStackSize == 0 else floor(i / prevStackSize)

                useIndex = x % arrayLength
                parameterValue = configValues[useIndex]
                parameterStack.append((configPath, parameterValue))
            flattenGrid.append(parameterStack)

        return flattenGrid

    def getNextEntryIndex(self):
        return len(self.csvLogger.getRowsAsList())

    def getUnusedIndexes(self, gridLength):
        allIndexes = set(range(gridLength))
        usedIndexes = []
        rows = self.csvLogger.getRowsAsList()
        for i, row in enumerate(rows):
            usedIndexes.append(int(row[0]))

        return allIndexes - set(usedIndexes)

    def getNextFreeIndex(self, gridLength, seed=5):
        random.seed(seed)
        unusedIndexes = self.getUnusedIndexes(gridLength)
        return random.choice(list(unusedIndexes))

    def runProject(self, project: Project):
        project.logLevel = pyPhases.util.Logger.Logger.verboseLevel
        startWith = 0
        self.csvLogger = CSVLogger(self.csvLogFile)

        if self.resume:
            startWith = self.getNextEntryIndex()
        else:
            self.csvLogger.cleanCsv()

        grid = self.prepareGridFile()
        configs = self.flattenGrid(grid)
        runCount = len(configs)
        self.log("Grid loaded with %s runs, starting with %i" % (runCount, startWith))

        for rangeIndex in range(startWith, runCount):
            if self.runSettings["maxruns"] > 0 and rangeIndex >= self.runSettings["maxruns"]:
                break
            runIndex = rangeIndex
            if self.runSettings["random"]:
                runId = self.getNextFreeIndex(runCount, self.runSettings["seed"])
                runIndex = runId - 1
            else:
                runId = runIndex + 1
                
            self.log("Current run id: %i" % (runId))
            configArray = configs[runIndex]
            outputDics = {"run": runId}
            for configPath, parameterValue in configArray:
                self.log("set config %s: %s" % (configPath, parameterValue))
                outputDics["/".join(configPath)] = str(parameterValue)
                project.config[configPath] = parameterValue
            project.prepareAllPhases()
            project.run(self.phaseName)
            self.log("Run (index: %i / Runid: %i) Finished: %i/%i" % (runIndex, runId, rangeIndex + 1, runCount))
            if project.gridOutput:
                self.log("Result: %s" % (project.gridOutput))
                project.gridOutput["run"] = runId
                outputDics.update(project.gridOutput)
                self.csvLogger.addCsvRow(outputDics)
                project.gridOutput = {}
