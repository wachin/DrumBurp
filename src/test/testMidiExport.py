import os
import unittest
from io import BytesIO

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

from Data.ScoreSerializer import ScoreSerializer
from GUI import DBMidi


TESTDATA_DIR = os.path.join(os.path.dirname(__file__), "testdata")


class TestMidiExport(unittest.TestCase):
    def testExportMidiFromFixture(self):
        score = ScoreSerializer.loadScore(
            os.path.join(TESTDATA_DIR, "v1", "Example Song.brp"))
        midi = BytesIO()

        DBMidi.exportMidi(score.iterMeasuresWithRepeats(), score, midi)
        data = midi.getvalue()

        self.assertGreater(len(data), 22)
        self.assertEqual(data[:4], b"MThd")
        self.assertEqual(data[14:18], b"MTrk")


if __name__ == "__main__":
    unittest.main()
