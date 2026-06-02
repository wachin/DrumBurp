import os
import unittest
from types import SimpleNamespace
from unittest import mock

from GUI.DBMainwindow import DrumBurp, _isScoreFilename


class TestScoreFilenameHandling(unittest.TestCase):
    def testScoreFilenameExtensions(self):
        self.assertTrue(_isScoreFilename("score.brp"))
        self.assertTrue(_isScoreFilename("score.BRP"))
        self.assertFalse(_isScoreFilename("README.md"))
        self.assertFalse(_isScoreFilename("notes.txt"))
        self.assertFalse(_isScoreFilename(None))

    def testLoadableScoreRequiresExistingBrpFile(self):
        score = os.path.join("scores", "score.brp")
        markdown = os.path.join("scores", "README.md")
        missing = os.path.join("scores", "missing.brp")
        fake = SimpleNamespace()

        with mock.patch("GUI.DBMainwindow.os.path.exists",
                        side_effect=lambda path: path != missing):
            self.assertTrue(DrumBurp._isLoadableScore(fake, score))
            self.assertFalse(DrumBurp._isLoadableScore(fake, markdown))
            self.assertFalse(DrumBurp._isLoadableScore(fake, missing))


class TestLastScoreDirectory(unittest.TestCase):
    def testRememberScoreDirectory(self):
        score = os.path.join("scores", "score.brp")
        fake = SimpleNamespace(lastScoreDirectory=None)

        with mock.patch("GUI.DBMainwindow.os.path.isdir", return_value=True):
            DrumBurp._rememberScoreDirectory(fake, score)

        self.assertEqual(fake.lastScoreDirectory,
                         os.path.abspath("scores"))

    def testScoreDialogDirectoryPrefersCurrentFilename(self):
        score = os.path.join("scores", "score.brp")
        fake = SimpleNamespace(
            filename=score,
            lastScoreDirectory=None,
            recentFiles=[])

        with mock.patch("GUI.DBMainwindow.os.path.isdir", return_value=True):
            self.assertEqual(DrumBurp._scoreDialogDirectory(fake),
                             os.path.abspath("scores"))

    def testScoreDialogDirectoryFallsBackToLastScoreDirectory(self):
        directory = os.path.abspath("last-scores")
        fake = SimpleNamespace(
            filename=None,
            lastScoreDirectory=directory,
            recentFiles=[])

        with mock.patch("GUI.DBMainwindow.os.path.isdir", return_value=True):
            self.assertEqual(DrumBurp._scoreDialogDirectory(fake), directory)

    def testScoreDialogDirectoryFallsBackToRecentScores(self):
        score = os.path.join("recent-scores", "score.brp")
        fake = SimpleNamespace(
            filename=None,
            lastScoreDirectory=None,
            recentFiles=[score])

        with mock.patch("GUI.DBMainwindow.os.path.isdir", return_value=True):
            self.assertEqual(DrumBurp._scoreDialogDirectory(fake),
                             os.path.abspath("recent-scores"))


if __name__ == "__main__":
    unittest.main()
