import os
import unittest
from pathlib import Path
from unittest.mock import MagicMock, call, mock_open, patch

from pyPhases import pdict

from phases.commands.Base import Base, Misconfigured


class TestBase(unittest.TestCase):
    def test_run(self):
        b = Base({})
        self.assertRaises(NotImplementedError, b.run)

    def test_overwriteConfigByEnviroment(self):
        b = Base({})
        config = {"foo": "bar", "foobar": {"foo2": "bar2"}}
        os.environ["PHASE_CONFIG_foo"] = "Test1"
        os.environ["PHASE_CONFIG_foo2"] = "doesnotexist"
        os.environ["PHASE_CONFIG_foobar_foo2"] = "Test2"
        os.environ["PHASE_CONFIG_foobar_foo3"] = "doesnotexist"

        updatedConfig = b.overwriteConfigByEnviroment(config)

        self.assertEqual(updatedConfig, {"foo": "Test1", "foobar": {"foo2": "Test2"}})

    def test_importConfigsByImportValue(self):
        b = Base({})
        b.loadConfig = MagicMock(return_value={"foo": "bar"})
        config = {"import": ["myConfig.yaml"]}

        imported = b.importConfigsByImportValue("import", config, "/configs/mainConfig.yaml")

        b.loadConfig.assert_called_with(Path("/configs/myConfig.yaml"))
        self.assertNotIn("import", config)
        self.assertEqual(imported, [{"foo": "bar"}])

    def test_loadConfig(self):
        b = Base({})
        b.importConfigsByImportValue = MagicMock()
        fileData = '{"foo":"bar"}'
        with patch("builtins.open", mock_open(read_data=fileData)) as m:

            config = b.loadConfig("test.config")

            m.assert_called_with("test.config", "r")
            b.importConfigsByImportValue.assert_has_calls(
                [
                    call("importBefore", {"foo": "bar"}, "test.config"),
                    call("importAfter", {"foo": "bar"}, "test.config"),
                ]
            )
            self.assertEqual(config, {"config": {"foo": "bar"}})

    def test_overwriteConfigByEnviromentByCliParameter(self):
        b = Base({})

        config = pdict({"foo": "bar"})
        b.customConfigValues = ["foo=bar2", "foo2=bar"]

        b.overwriteConfigByEnviromentByCliParameter(config)

        self.assertEqual(config, {"foo": "bar2", "foo2": "bar"})

    def test_prepareConfig(self):
        b = Base({})
        config = {"config": {"foo": "bar"}, "name": "myProject"}
        b.projectFileName = "p.yaml"
        b.loadConfig = MagicMock(return_value=config)
        b.projectConfigFileName = "conf1,conf2"
        b.overwriteConfigByEnviroment = MagicMock(return_value={"foo": "bar", "foo2": "bar2"})
        b.overwriteConfigByEnviromentByCliParameter = MagicMock(return_value={"foo": "bar2", "foo2": "bar2"})
        b.validateConfig = MagicMock()
        b.normalizeConfigArrays = MagicMock()
        b.preparePhases = MagicMock()

        b.prepareConfig()

        fullConfig = {"config": {"foo": "bar2", "foo2": "bar2"}, "name": "myProject"}
        b.loadConfig.assert_has_calls(
            [
                call("p.yaml", root=True),
                call("conf1"),
                call("conf2"),
            ]
        )
        b.overwriteConfigByEnviroment.assert_called_once_with({"foo": "bar"})
        b.overwriteConfigByEnviromentByCliParameter.assert_called_once_with({"foo": "bar", "foo2": "bar2"})
        b.validateConfig.assert_called_once_with(fullConfig)
        self.assertEqual(b.outputDir, "myProject")
        self.assertEqual(b.config, config)
        b.normalizeConfigArrays.assert_called_once()
        b.preparePhases.assert_called_once()

    def test_validateConfigMisconfigured(self):
        b = Base({})

        self.assertRaises(Misconfigured, b.validateConfig, {"name": "myname"})
        self.assertRaises(Misconfigured, b.validateConfig, {"phases": []})

    def test_validateConfig(self):
        b = Base({})

        config = {"name": "p", "namespace": "n", "phases": []}
        config = pdict(config)

        b.validateConfig(config)

        self.assertEqual(config, {"name": "p", "namespace": "n", "phases": [], "exporter": []})

    def test_validateConfigDontOverwrite(self):
        b = Base({})

        config = pdict({"name": "p", "namespace": "n", "phases": [], "exporter": ["myExporter"]})

        b.validateConfig(config)

        self.assertEqual(
            config,
            {"name": "p", "namespace": "n", "phases": [], "exporter": ["myExporter"]},
        )

    def test_normalizeDict(self):
        b = Base({})

        normalized = b.normalizeDict({"foo": "bar"})

        self.assertEqual(normalized, [{"name": "foo", "value": "bar"}])

    def test_normalizeDataArray_noName(self):
        b = Base({})

        self.assertRaises(Exception, b.normalizeDataArray, {"data": {"foo": "bar"}})

    def test_normalizeDataArray_str(self):
        b = Base({})

        normalized = b.normalizeDataArray("myData")

        self.assertEqual(normalized, {"name": "myData", "description": ""})

    def test_normalizeDataArray(self):
        b = Base({})

        normalized = b.normalizeDataArray({"name": "test", "config": {"foo": "bar"}})

        self.assertEqual(
            normalized,
            {
                "name": "test",
                "config": {"foo": "bar", "items": [{"name": "foo", "value": "bar"}]},
            },
        )

    def test_normalizeConfigArrays(self):
        b = Base({})

        b.config = pdict({"exporter": ["myExporter"]})
        b.normalizeConfigArrays()

        self.assertEqual(
            b.config,
            {"exporter": [{"name": "myExporter", "description": ""}], "data": []},
        )
