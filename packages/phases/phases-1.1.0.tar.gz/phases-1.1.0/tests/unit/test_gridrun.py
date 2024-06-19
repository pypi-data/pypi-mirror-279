import unittest
from unittest import mock
from unittest.mock import MagicMock, call

from pyPhases import CSVLogger, pdict

from phases.commands.gridrun import Gridrun


class TestGridRun(unittest.TestCase):
    def test_parseRunOptions_defaults(self):

        gridrun = Gridrun({})

        self.assertEqual(gridrun.projectGridFile, None)
        self.assertEqual(gridrun.csvLogFile, "output.csv")
        self.assertEqual(gridrun.resume, True)

    def test_parseRunOptions(self):

        gridrun = Gridrun({})
        gridrun.options = {
            "<gridfile>": "g",
            "--csv": "c",
            "-r": "doesntmatter",
            "-o": "o",
            "-p": "p",
            "-c": "c",
            "--set": "s",
            "-v": "doesntmatter",
            "<phaseName>": "myPhase",
        }

        gridrun.parseRunOptions()

        self.assertEqual(gridrun.projectGridFile, "g")
        self.assertEqual(gridrun.csvLogFile, "c")
        self.assertEqual(gridrun.resume, False)
        self.assertEqual(gridrun.phaseName, "myPhase")

    def test_getGrid_constant(self):
        gridrun = Gridrun({})

        config = {
            "field1": [1, 2],
            "nestedfield": {"field2": [1, 2], "const": 4, "single": [1]},
        }

        self.assertRaises(Exception, gridrun.getGrid, config)

    def test_getGrid_single(self):
        gridrun = Gridrun({})

        config = {"field1": [1, 2], "nestedfield": {"field2": [1, 2], "single": [1]}}

        grid = gridrun.getGrid(config)

        self.assertEqual(
            grid,
            [
                (["field1"], [1, 2]),
                (["nestedfield", "field2"], [1, 2]),
                (["nestedfield", "single"], [1]),
            ],
        )

    def test_prepareGridFile_noGridValue(self):
        gridrun = Gridrun({})
        fileData = "{}"
        with mock.patch("builtins.open", mock.mock_open(read_data=fileData)) as m:

            self.assertRaises(Exception, gridrun.prepareGridFile)

    def test_prepareGridFile_falseOptions(self):
        gridrun = Gridrun({})
        fileData = '{"foo": 0, "grid": {"field1": [1,2]}}'
        with mock.patch("builtins.open", mock.mock_open(read_data=fileData)) as m:

            grid = gridrun.prepareGridFile()
            self.assertEqual(grid, [(["field1"], [1, 2])])

    def test_prepareGridFile(self):
        gridrun = Gridrun({})
        fileData = '{"parallel": true, "grid": {"field1": [1,2]}}'
        with mock.patch("builtins.open", mock.mock_open(read_data=fileData)) as m:

            grid = gridrun.prepareGridFile()
            self.assertEqual(grid, [(["field1"], [1, 2])])
            self.assertEqual(gridrun.runSettings["parallel"], True)

    def test_flattenGrid(self):
        grids = [
            [("p0", [0])],
            [["p0", [0]], ["p1", [1]]],
            [["p0", [0]], ["p1", [1, 2]]],
            [["p0", [0, 1]], ["p1", [0, 1, 2]]],
        ]

        run = Gridrun({})
        self.assertEqual(run.flattenGrid(grids[0]), [[("p0", 0)]])
        self.assertEqual(run.flattenGrid(grids[1]), [[("p0", 0), ("p1", 1)]])
        self.assertEqual(run.flattenGrid(grids[2]), [[("p0", 0), ("p1", 1)], [("p0", 0), ("p1", 2)]])
        self.assertEqual(
            run.flattenGrid(grids[3]),
            [
                [("p0", 0), ("p1", 0)],
                [("p0", 1), ("p1", 0)],
                [("p0", 0), ("p1", 1)],
                [("p0", 1), ("p1", 1)],
                [("p0", 0), ("p1", 2)],
                [("p0", 1), ("p1", 2)],
            ],
        )

    @mock.patch("pyPhases.CSVLogger.getRowsAsList", return_value=[])
    def test_getNextEntryIndexEmpty(self, _):
        gridrun = Gridrun({})
        gridrun.csvLogger = CSVLogger("test.csv")

        self.assertEqual(gridrun.getNextEntryIndex(), 0)

    @mock.patch("pyPhases.CSVLogger.getRowsAsList", return_value=[1])
    def test_getNextEntryIndex1(self, _):
        gridrun = Gridrun({})
        gridrun.csvLogger = CSVLogger("test.csv")

        self.assertEqual(gridrun.getNextEntryIndex(), 1)

    @mock.patch("pyPhases.CSVLogger.getRowsAsList", return_value=[1, 2, 3])
    def test_getNextEntryIndexMutli(self, _):
        gridrun = Gridrun({})
        gridrun.csvLogger = CSVLogger("test.csv")

        self.assertEqual(gridrun.getNextEntryIndex(), 3)

    @mock.patch("pyPhases.CSVLogger.getRowsAsList", return_value=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    def test_getNextEntryIndex10(self, _):
        gridrun = Gridrun({})
        gridrun.csvLogger = CSVLogger("test.csv")

        self.assertEqual(gridrun.getNextEntryIndex(), 10)

    @mock.patch(
        "pyPhases.CSVLogger.getRowsAsList",
        return_value=[[0], [1], [2], [3], [5], [6], [7], [8], [9]],
    )
    def test_getUnusedIndexes(self, _):
        gridrun = Gridrun({})
        gridrun.csvLogger = CSVLogger("test.csv")

        self.assertEqual(gridrun.getUnusedIndexes(10), {4})

    @mock.patch(
        "pyPhases.CSVLogger.getRowsAsList",
        return_value=[[0], [1], [2], [3], [4], [5], [6], [7], [8], [9]],
    )
    def test_getUnusedIndexesFull(self, _):
        gridrun = Gridrun({})
        gridrun.csvLogger = CSVLogger("test.csv")

        self.assertEqual(gridrun.getUnusedIndexes(10), set())

    @mock.patch("pyPhases.CSVLogger.getRowsAsList", return_value=[])
    def test_getUnusedIndexesEmpty(self, _):
        gridrun = Gridrun({})
        gridrun.csvLogger = CSVLogger("test.csv")
        self.assertEqual(gridrun.getUnusedIndexes(10), {0, 1, 2, 3, 4, 5, 6, 7, 8, 9})

    @mock.patch(
        "pyPhases.CSVLogger.getRowsAsList",
        return_value=[[0], [1], [2], [3], [5], [6], [7], [8], [9]],
    )
    def test_getNextFreeIndexOneLeft(self, _):
        gridrun = Gridrun({})
        gridrun.csvLogger = CSVLogger("test.csv")
        self.assertEqual(gridrun.getNextFreeIndex(10), 4)

    @mock.patch(
        "pyPhases.CSVLogger.getRowsAsList",
        return_value=[[0], [1], [2], [3], [4], [5], [6], [7], [8], [9]],
    )
    def test_getNextFreeIndexFull(self, _):
        gridrun = Gridrun({})
        gridrun.csvLogger = CSVLogger("test.csv")
        CSVLogger.getRowsAsList = MagicMock(return_value=[[0], [1], [2], [3], [4], [5], [6], [7], [8], [9]])

        self.assertRaises(IndexError, gridrun.getNextFreeIndex, 10)

    @mock.patch(
        "pyPhases.CSVLogger.getRowsAsList",
        return_value=[[0], [1], [2], [3], [4], [5], [6], [7]],
    )
    def test_getNextFree(self, _):
        gridrun = Gridrun({})
        gridrun.csvLogger = CSVLogger("test.csv")

        self.assertEqual(gridrun.getNextFreeIndex(10, seed=5), 9)

    def getRunSetup(self):
        CSVLogger.cleanCsv = MagicMock()
        CSVLogger.getNextEntryIndex = MagicMock(return_value=0)
        CSVLogger.addCsvRow = MagicMock()
        gridrun = Gridrun({})
        gridrun.prepareGridFile = MagicMock(return_value=[(["foo"], [0, 1])])
        gridrun.options = {}
        gridrun.runSettings = {"random": False, "maxruns": 0}
        gridrun.grid = [[("p0", 0), ("p1", 1)]]
        gridrun.csvLogFile = "myLogfile.csv"
        gridrun.projectGridFile = "gridfile.yaml"
        return gridrun

    def test_runProject_noresume(self):
        gridrun = self.getRunSetup()
        gridrun.resume = False
        project = MagicMock()

        gridrun.runProject(project)

        CSVLogger.cleanCsv.assert_called_once()

    def test_runProject_resume(self):
        gridrun = self.getRunSetup()
        gridrun.resume = True
        project = MagicMock()

        gridrun.runProject(project)

        CSVLogger.cleanCsv.assert_not_called()

    def test_runProject_random(self):
        gridrun = self.getRunSetup()
        gridrun.resume = False
        gridrun.runSettings = {"random": True, "seed": 4, "maxruns": 0}
        gridrun.getNextFreeIndex = MagicMock(return_value=1)
        project = MagicMock()

        gridrun.runProject(project)
        gridrun.getNextFreeIndex.assert_has_calls([call(2, 4), call(2, 4)])  # 2 is the number of entries in the grid

    def test_runProject_run(self):
        gridrun = self.getRunSetup()
        gridrun.resume = False
        gridrun.phaseName = "phase1"
        project = MagicMock()
        project.config = pdict({"foo": -1})
        project.gridOutput = {"succeess": 1}

        def side_effect(phaseName):
            self.assertEqual(phaseName, "phase1")
            self.assertEqual(project.config["foo"], side_effect.index)
            side_effect.index += 1
            project.gridOutput = {"succeess": 1}

        side_effect.index = 0

        project.run = MagicMock(side_effect=side_effect)

        gridrun.runProject(project)

        self.assertEqual(project.run.call_count, 2)
        self.assertEqual(project.prepareAllPhases.call_count, 2)
        CSVLogger.addCsvRow.assert_has_calls(
            [
                call({"run": 1, "foo": "0", "succeess": 1}),
                call({"run": 2, "foo": "1", "succeess": 1}),
            ]
        )
