import os
import sys
from pathlib import Path

import yaml

from pyPhases import pdict, classLogger

try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader as SafeLoader


class Misconfigured(Exception):
    pass


@classLogger
class Base(object):
    outputDir = None
    """A base command."""

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs
        self.config = {}
        self.projectFileName = "project.yaml"
        self.projectGridFile = None
        self.projectConfigFileName = None
        self.config = None
        self.customConfigValues = []

    def run(self):
        raise NotImplementedError("You must implement the run() method yourself!")

    def overwriteConfigByEnviroment(self, config, path=None):
        path = path or []
        config = pdict(config)
        for field in config:
            value = config[field]
            p = path + [str(field)]

            if isinstance(value, dict):
                config[field] = self.overwriteConfigByEnviroment(value, p)
            else:
                v = os.environ.get("PHASE_CONFIG_" + "_".join(p))
                if v is not None:
                    self.logDebug("overwrite config %s by env: %s" % (p, v))
                    config[field] = v

        return config

    def importConfigsByImportValue(self, key, baseConfig, filePath):
        importedConfigs = []
        if key in baseConfig:
            for relPath in baseConfig[key]:
                path = Path(Path(filePath).parent, relPath)
                importedConfig = self.loadConfig(path)
                importedConfigs.append(importedConfig)
            del baseConfig[key]
        return importedConfigs

    def loadConfig(self, filePath, root=False):
        loadedConfig = pdict()

        with open(filePath, "r") as configFile:
            yamlContent = configFile.read()
            fileConfig = yaml.load(yamlContent, Loader=SafeLoader)

        if fileConfig is None:
            return {}

        isFullConfig = True if root or "isFullConfig" in fileConfig and fileConfig["isFullConfig"] else False

        importedConfigsBefore = self.importConfigsByImportValue("importBefore", fileConfig, filePath)
        importedConfigsAfter = self.importConfigsByImportValue("importAfter", fileConfig, filePath)

        if not isFullConfig:
            fileConfig = pdict({"config": fileConfig})

        for subConfig in importedConfigsBefore:
            loadedConfig.update(subConfig)

        self.logDebug("parse user config: %s" % filePath)
        loadedConfig.update(fileConfig)

        for subConfig in importedConfigsAfter:
            loadedConfig.update(subConfig)

        return loadedConfig

    def overwriteConfigByEnviromentByCliParameter(self, config):
        for s in self.customConfigValues:
            field, value = s.split("=")
            field = field.split(".")
            config[field] = value
        return config

    def prepareConfig(self):
        projectConfig = self.loadConfig(self.projectFileName, root=True)

        if self.projectConfigFileName is not None:
            configFiles = self.projectConfigFileName.split(",")
            for configFile in configFiles:
                subConfig = self.loadConfig(configFile)
                projectConfig.update(subConfig)

        projectConfig["config"] = self.overwriteConfigByEnviroment(projectConfig["config"])
        projectConfig["config"] = self.overwriteConfigByEnviromentByCliParameter(projectConfig["config"])

        self.validateConfig(projectConfig)
        if self.outputDir is None:
            self.outputDir = projectConfig["name"]
        self.config = projectConfig
        self.normalizeConfigArrays()

        self.preparePhases()

    def validateConfig(self, config):
        # check required fields
        required = ["name", "phases"]
        for field in required:
            if field not in config:
                raise Misconfigured("%s is required in the project yaml file" % (field))

        # set default values
        defaultValues = {
            "exporter": [],
        }

        # for field in defaultValues:
        config.setdefaults(defaultValues)

    def preparePhases(self):
        self.config["userPhases"] = []
        self.config["phaseClasses"] = []
        lastPhase = None
        for phaseName in self.config["phases"]:
            phases = [phaseName]

            for phase in phases:
                self.config["userPhases"].append(phase)
                if lastPhase is not None:
                    lastPhase["next"] = phase
                lastPhase = phase

        self.config["phases"] = self.config["userPhases"]

    def normalizeDict(self, dictObj):
        arrayForTemplate = []

        for name, value in dictObj.items():
            arrayForTemplate.append({"name": name, "value": value})
        return arrayForTemplate

    def normalizeDataArray(self, objectOrString):
        if isinstance(objectOrString, str):
            return {"name": objectOrString, "description": ""}

        if "name" not in objectOrString:
            raise Exception("One Object does not have a name")

        if "config" in objectOrString:
            objectOrString["config"]["items"] = self.normalizeDict(objectOrString["config"])

        return objectOrString

    def normalizeConfigArrays(self):
        arrayFields = ["exporter", "data"]
        for field in arrayFields:
            if field not in self.config:
                self.config[field] = []
            for index, arrayOrString in enumerate(self.config[field]):
                obj = self.normalizeDataArray(arrayOrString)
                self.config[field][index] = obj
