import os
import platform
import unittest
from io import BytesIO
from unittest import mock

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

    def testPygameOutputChunksLargeEventLists(self):
        class FakeOutput(object):
            def __init__(self):
                self.batches = []

            def write(self, events):
                self.batches.append(list(events))

        output = DBMidi.PygameOutput()
        fakeOutput = FakeOutput()
        output._output = fakeOutput
        events = [
            [[0x99, 38, 96], index]
            for index in range(DBMidi._PYGAME_MAX_EVENT_BATCH * 2 + 3)
        ]

        output.write(events)

        self.assertFalse(output.supportsTimestamps)
        self.assertEqual([len(batch) for batch in fakeOutput.batches],
                         [1024, 1024, 3])

    @unittest.skipUnless(DBMidi._HAS_PYGAME,
                         "pygame mixer output requires pygame")
    def testPygameMixerOutputPlaysMidiData(self):
        calls = []

        def fakeStop():
            calls.append(("stop",))

        def fakeLoad(data, namehint=None):
            calls.append(("load", data.read(4), namehint))

        def fakePlay():
            calls.append(("play",))

        output = DBMidi.PygameMixerOutput()

        with mock.patch.object(DBMidi.pygame.mixer.music, "stop", fakeStop), \
                mock.patch.object(DBMidi.pygame.mixer.music, "load", fakeLoad), \
                mock.patch.object(DBMidi.pygame.mixer.music, "play", fakePlay):
            output.open(DBMidi._PYGAME_MIXER_DEVICE_ID)
            output.playMidiData(b"MThd\x00\x00\x00\x06")

        self.assertEqual(calls, [
            ("stop",),
            ("load", b"MThd", "mid"),
            ("play",),
        ])

    @unittest.skipIf(platform.system() == "Windows",
                     "Linux PortMidi device priority is not used on Windows")
    def testCandidateOutputIdsPreferSynthOverMidiThrough(self):
        oldDevices = list(DBMidi._OUTPUT_DEVICES)
        oldGetDefaultId = DBMidi.getDefaultId
        try:
            DBMidi._OUTPUT_DEVICES[:] = [
                DBMidi.MidiDevice(0, "Midi Through Port-0"),
                DBMidi.MidiDevice(2, "qjackctl"),
                DBMidi.MidiDevice(3, "Synth input port (5919:0)"),
            ]
            DBMidi._OUTPUT_DEVICES.sort(key=DBMidi._outputDeviceSortKey)
            DBMidi.getDefaultId = lambda: 0

            candidates = list(DBMidi._candidateOutputIds())

            self.assertEqual(candidates[0], 3)
            self.assertEqual(
                list(DBMidi._candidateOutputIds(preferred=0, fallback=False)),
                [0])
        finally:
            DBMidi._OUTPUT_DEVICES[:] = oldDevices
            DBMidi.getDefaultId = oldGetDefaultId

    @unittest.skipIf(platform.system() == "Windows",
                     "Linux pygame mixer output is not used on Windows")
    def testCandidateOutputIdsUsePygameMixerBeforeMidiThrough(self):
        oldDevices = list(DBMidi._OUTPUT_DEVICES)
        oldGetDefaultId = DBMidi.getDefaultId
        try:
            DBMidi._OUTPUT_DEVICES[:] = [
                DBMidi.MidiDevice(0, "Midi Through Port-0"),
                DBMidi.MidiDevice(
                    DBMidi._PYGAME_MIXER_DEVICE_ID,
                    DBMidi._PYGAME_MIXER_DEVICE_NAME,
                    DBMidi._PYGAME_MIXER_DRIVER),
            ]
            DBMidi._OUTPUT_DEVICES.sort(key=DBMidi._outputDeviceSortKey)
            DBMidi.getDefaultId = lambda: 0

            candidates = list(DBMidi._candidateOutputIds())

            self.assertEqual(candidates[0], DBMidi._PYGAME_MIXER_DEVICE_ID)
            self.assertEqual(candidates[1], 0)
        finally:
            DBMidi._OUTPUT_DEVICES[:] = oldDevices
            DBMidi.getDefaultId = oldGetDefaultId


if __name__ == "__main__":
    unittest.main()
