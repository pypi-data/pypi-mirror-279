import importlib
from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock

from pyPhases import Data, Phase, Project, pdict
from pyPhases.test import mockLogger

from phases.commands.run import Run


# @mockLocker
class TestRun(TestCase):
    def getDefaultConfig(self):
        return pdict(
            {
                "name": "test",
                "namespace": "testns",
                "phases": [],
                "config": {},
                "exporter": [],
                "data": [],
            }
        )

    def test_createProjectFromConfig_default(self):
        """Test that a project is created from a config file"""

        config = self.getDefaultConfig()

        run = Run({})
        run.debug = True
        Project.trigger = MagicMock()
        Project.prepareAllPhases = MagicMock()

        project = run.createProjectFromConfig(config)

        self.assertEqual(project.debug, True)
        self.assertEqual(project.name, "test")
        self.assertEqual(project.namespace, "testns")
        Project.trigger.assert_called_once_with("configChanged", None)
        Project.prepareAllPhases.assert_called_once()

    def test_createProjectFromConfig_phases(self):
        """Test that a project is created from a config file"""

        config = self.getDefaultConfig()
        config["phases"] = [{"name": "phase1"}]

        run = Run({})

        phase = Phase()
        phase.name = "phase1"
        run.loadClass = MagicMock(return_value=phase)

        project = run.createProjectFromConfig(config)

        self.assertEqual(len(project.phases), 1)
        self.assertEqual(project.phases[0].name, "phase1")
        run.loadClass.assert_called_with({"name": "phase1"}, "test", path="phases")

    def test_createProjectFromConfig_plugins(self):
        """Test that a project is created from a config file"""

        config = self.getDefaultConfig()
        config["plugins"] = ["myPlugin"]

        run = Run({})
        moduleMock = MagicMock()
        moduleMock.__file__ = "root/pluginpath"
        importlib.import_module = MagicMock(return_value=moduleMock)
        Path.exists = MagicMock(return_value=True)
        run.loadConfig = MagicMock(return_value={"config": {"foo": "bar"}})
        Project.addPlugin = MagicMock()

        run.createProjectFromConfig(config)

        Project.addPlugin.assert_called_with("myPlugin", {})

    def test_createProjectFromConfig_exporter(self):
        """Test that a project is created from a config file"""

        config = self.getDefaultConfig()
        config["exporter"] = ["myExporter"]

        run = Run({})
        myExporter = MagicMock()
        run.loadClass = MagicMock(return_value=myExporter)

        project = run.createProjectFromConfig(config)

        run.loadClass.assert_called_with("myExporter", "test", project.systemExporter, path="exporter")
        self.assertEqual(project.exporters, [myExporter])

    def test_createProjectFromConfig_data(self):
        """Test that a project is created from a config file"""

        config = self.getDefaultConfig()
        config["config"] = {"foo": "bar"}
        config["phases"] = [
            {
                "name": "phase1",
                "exports": ["myData"],
            }
        ]
        config["data"] = [
            {
                "name": "myData",
                "dependsOn": ["foo", "myData"],
            }
        ]

        run = Run({})

        phase = Phase()
        phase.name = "phase1"
        phase.exportData = []
        run.loadClass = MagicMock(return_value=phase)

        project = run.createProjectFromConfig(config)

        self.assertEqual(len(project.phases[0].exportData), 1)
        self.assertEqual(project.phases[0].exportData[0].name, "myData")
        self.assertEqual(project.phases[0].exportData[0].project, project)
        self.assertEqual(project.getDataFromName("myData").dataTags, ["foo", "myData"])

    def test_getDataDefinition(self):
        """Test that the data definitions are returned from the config file"""

        config = {
            "name": "data1",
            "dependsOn": ["a"],
        }

        config = pdict(config)

        run = Run({})
        run.config = {"config": {"a": 1}}
        run.debug = True

        project = Project()
        data = run.getDataDefinition(config, project)
        self.assertIsInstance(data, Data)
        self.assertEqual(data.name, "data1")
        self.assertEqual(data.dataTags, ["a"])
        self.assertEqual(project.dataNames["data1"], data)

    @mockLogger
    def test_getDataDefinitionDependingonData(self, mockLog):
        """Test that the data definitions are returned from the config file"""

        config = {
            "name": "data1",
            "description": "test",
            "dependsOn": ["a"],
        }
        dataDef2 = {
            "name": "data2",
            "dependsOn": ["a", "data1"],
        }

        config = pdict(config)

        run = Run({})
        run.config = {"config": {"a": 1}}
        run.debug = True

        project = Project()

        run.getDataDefinition(dataDef2, project)
        # self.assertWarningLike("Dependency 'data1' for Data could not be found in any config or other defined data")
        mockLog.assertWarningLike("Dependency 'data1' for Data could not be found in any config or other defined data")

        run.getDataDefinition(config, project)
        data = run.getDataDefinition(dataDef2, project)

        self.assertIsInstance(data, Data)
        self.assertEqual(data.name, "data2")
        self.assertEqual(data.dataTags, ["a", "data1"])

    def test_parseRunOptions_default(self):
        run = Run({})

        self.assertEqual(run.outputDir, None)
        self.assertEqual(run.projectFileName, "project.yaml")
        self.assertEqual(run.projectConfigFileName, None)
        self.assertEqual(run.customConfigValues, [])
        self.assertEqual(run.debug, False)
        self.assertEqual(run.phaseName, None)

        self.options = {}

    def test_parseRunOptions(self):
        run = Run({})
        run.options = {
            "-o": "o",
            "-p": "p",
            "-c": "c",
            "--set": "s",
            "-v": "doesntmatter",
            "<phaseName>": "myPhase",
        }

        run.parseRunOptions()

        self.assertEqual(run.outputDir, "o")
        self.assertEqual(run.projectFileName, "p")
        self.assertEqual(run.projectConfigFileName, "c")
        self.assertEqual(run.customConfigValues, "s")
        self.assertEqual(run.debug, True)
        self.assertEqual(run.phaseName, "myPhase")

    def test_runProject(self):
        run = Run({})
        run.phaseName = "myPhase"

        project = MagicMock()

        run.runProject(project)

        project.run.assert_called_once_with("myPhase")

    def test_run(self):
        run = Run({})

        run.beforeRun = MagicMock()
        run.prepareConfig = MagicMock()
        run.createProjectFromConfig = MagicMock(return_value="project")
        run.runProject = MagicMock()

        run.run()

        run.beforeRun.assert_called_once()
        run.prepareConfig.assert_called_once()
        run.createProjectFromConfig.assert_called_once()
        run.runProject.assert_called_once_with("project")
