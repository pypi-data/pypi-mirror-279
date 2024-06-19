import unittest

from phases.commands.create import Create


class TestCreate(unittest.TestCase):
    def test_parseRunOptions_default(self):
        """Test that the options are parsed correctly"""
        create = Create({})

        self.assertEqual(create.forceWrite, False)

    def test_parseRunOptions(self):
        """Test that the options are parsed correctly"""
        create = Create({})
        create.options = {
            "-o": "o",
            "-p": "p",
            "-f": "f",
        }

        create.parseRunOptions()

        self.assertEqual(create.outputDir, "o")
        self.assertEqual(create.projectFileName, "p")
        self.assertEqual(create.forceWrite, True)
