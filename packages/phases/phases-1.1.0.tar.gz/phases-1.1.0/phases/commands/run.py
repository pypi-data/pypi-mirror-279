"""
Create a new Project
"""
import importlib
import sys

import pyPhases
from pyPhases import Data, Project, pdict

from phases.commands.Base import Base


class Run(Base):
    """create a Phase-Project"""

    config = None
    projectFileName = "project.yaml"
    forceWrite = False
    debug = False
    phaseName = None

    def run(self):
        self.beforeRun()
        self.prepareConfig()

        project = self.createProjectFromConfig(self.config)

        self.runProject(project)

    def runProject(self, project: Project):
        project.logLevel = pyPhases.util.Logger.Logger.verboseLevel
        project.run(self.phaseName)

    def parseRunOptions(self):
        if self.options["-o"]:
            self.outputDir = self.options["-o"]
            sys.path.insert(0, self.outputDir)
            self.logDebug("Set Outputdir: %s" % (self.outputDir))
        if self.options["-p"]:
            self.projectFileName = self.options["-p"]
            self.logDebug("Set Projectfile: %s" % (self.projectFileName))
        if self.options["-c"]:
            self.projectConfigFileName = self.options["-c"]
            self.logDebug("Set Config file(s): %s" % (self.projectFileName))
        if self.options["--set"]:
            self.customConfigValues = self.options["--set"]
            self.logDebug("Custom Values: %s" % (self.customConfigValues))
        if self.options["-v"]:
            self.debug = True
        if "<phaseName>" in self.options:
            self.phaseName = self.options["<phaseName>"]

    def beforeRun(self):
        self.parseRunOptions()

    def loadClass(self, classOptions, pythonPackage="", externalClasses=None, path="."):
        name = classOptions["name"]
        system = "system" in classOptions and classOptions["system"]
        options = classOptions["config"] if "config" in classOptions else {}
        leadingDot = "" if system else "."
        package = None if system else pythonPackage
        if externalClasses is not None and name in externalClasses:
            package = externalClasses[name]
        sys.path.insert(0, self.outputDir)
        module = importlib.import_module("%s%s.%s" % (leadingDot, path, name), package=package)
        classObj = getattr(module, name)

        if len(options) > 0:
            return classObj(options=options)
        else:
            return classObj()

    def getDataDefinition(self, dataObj, project):
        dependsOn = []
        if "dependsOn" in dataObj:
            for dependString in dataObj["dependsOn"]:
                dependsOn.append(dependString)

                if dependString not in project.config and dependString not in project.dataNames:
                    self.logWarning(
                        "Dependency '%s' for Data could not be found in any config or other defined data" % (dependString)
                    )

        return Data(dataObj["name"], project, dependsOn)

    def createProjectFromConfig(self, config) -> Project:
        self.logDebug("Load Project from Config")

        dataDefinitions = {}

        project = Project()
        project.debug = self.debug
        project.name = config["name"]
        project.namespace = config["namespace"] if "namespace" in config else ""
        project.config = pdict(config["config"])

        if "plugins" in config:
            for plugin in config["plugins"]:
                if not isinstance(plugin, dict):
                    plugin = {"name": plugin, "options": {}}

                self.logDebug("Load Plugins %s Default Config" % (plugin["name"]))

                self.logDebug("Add Plugin %s" % (plugin["name"]))
                project.addPlugin(plugin["name"], plugin["options"])

        for classObj in config["exporter"]:
            obj = self.loadClass(classObj, project.name, project.systemExporter, path="exporter")
            project.registerExporter(obj)

        for dataObj in config["data"]:
            data = self.getDataDefinition(dataObj, project)
            dataDefinitions[dataObj["name"]] = data

        for phaseConfig in config["phases"]:
            obj = self.loadClass(phaseConfig, project.name, path="phases")

            if not hasattr(obj, "exportData"):
                raise Exception(
                    "Phase %s was not initialized correctly, maybe you forgot to call the __init__ method after overwriting"
                )

            # add data
            if "exports" in phaseConfig:
                for dataName in phaseConfig["exports"]:
                    if dataName in dataDefinitions:
                        dataDef = dataDefinitions[dataName]
                    else:
                        dataDef = Data(dataName, project)

                    obj.exportData.append(dataDef)

            project.addPhase(obj)
        project.trigger("configChanged", None)
        project.prepareAllPhases()
        return project
