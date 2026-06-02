import os
import platform
import unittest
from io import BytesIO

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

from Data.Drum import HeadData
from Data.ScoreSerializer import ScoreSerializer
from GUI import DBMidi


TESTDATA_DIR = os.path.join(os.path.dirname(__file__), "testdata")


class TestMidiExport(unittest.TestCase):
    def testWindowsBackendManagerIncludesWinmm(self):
        drivers = DBMidi.BackendManager.output_drivers()

        if platform.system() == "Windows":
            self.assertIn("winmm", drivers)
            self.assertIn("Windows MM", drivers)
        else:
            self.assertNotIn("winmm", drivers)

    def testWinmmPortListIsPlatformSafe(self):
        ports = DBMidi.list_winmm_output_ports()

        if platform.system() != "Windows":
            self.assertEqual(ports, [])
        else:
            for port in ports:
                self.assertEqual(port.driver, "Windows MM")
                self.assertTrue(port.name)

    def testExportMidiFromFixture(self):
        score = ScoreSerializer.loadScore(
            os.path.join(TESTDATA_DIR, "v1", "Example Song.brp"))
        midi = BytesIO()

        DBMidi.exportMidi(score.iterMeasuresWithRepeats(), score, midi)
        data = midi.getvalue()

        self.assertGreater(len(data), 22)
        self.assertEqual(data[:4], b"MThd")
        self.assertEqual(data[14:18], b"MTrk")

    def testOutputEventsUseTempoChanges(self):
        headData = HeadData(midiNote=38, midiVolume=96)
        midiObjects = [
            DBMidi.MidiTempoChange(0, 120),
            DBMidi.MidiNote(DBMidi.MIDITICKSPERBEAT, headData),
            DBMidi.MidiTempoChange(DBMidi.MIDITICKSPERBEAT, 60),
            DBMidi.MidiNote(2 * DBMidi.MIDITICKSPERBEAT, headData),
        ]

        events = DBMidi._makeOutputEvents(midiObjects, startTime=1000)

        self.assertEqual(events[0], [[0x99, 38, 96], 1500])
        self.assertEqual(events[1], [[0x99, 38, 96], 2500])


if __name__ == "__main__":
    unittest.main()
