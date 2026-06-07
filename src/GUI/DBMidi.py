# Copyright 2011-2015 Michael Thomas
#
# See www.whatang.org for more information.
#
# This file is part of DrumBurp.
#
# DrumBurp is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DrumBurp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DrumBurp.  If not, see <http://www.gnu.org/licenses/>
'''
Created on 17 Sep 2011

@author: Mike Thomas

'''
import copy
import ctypes
from io import BytesIO
import platform
from ctypes import wintypes

HAS_MIDI = False
_MIDI_INITIALIZED = False
_PERCUSSION_CHANNEL = 0x09
_NOTE_ON = 0x90
_NOTE_OFF = 0x80
_CHOKE = 0xB0
_CHOKE_MSG = 120
_CHOKE_VELOCITY = 0
_PERCUSSION_NOTE_ON = _PERCUSSION_CHANNEL | _NOTE_ON
_PERCUSSION_NOTE_OFF = _PERCUSSION_CHANNEL | _NOTE_OFF
_PERCUSSION_CHOKE = _PERCUSSION_CHANNEL | _CHOKE
_BUFSIZE = 1024
_LATENCY = 1
_PYGAME_MAX_EVENT_BATCH = 1024

_FREQ = 44100  # audio CD quality
_BITSIZE = -16  # unsigned 16 bit
_CHANNELS = 2  # 1 is mono, 2 is stereo
_NUMSAMPLES = 4096  # number of samples

FLAM_TIME_CONSTANT = 32
FLAM_VOLUME_CONSTANT = 2
DRAG_TIME_CONSTANT = 96
_IS_WINDOWS = platform.system() == "Windows"
_PYGAME_DRIVER = "pygame"
_PYGAME_MIXER_DRIVER = "pygame mixer"
_PYGAME_MIXER_DEVICE_ID = -2
_PYGAME_MIXER_DEVICE_NAME = "Pygame MIDI Player"
_WINMM_DRIVER = "Windows MM"
_SCHEDULER_INTERVAL_MS = 5
_SCHEDULER_LOOKAHEAD_MS = 2
_PREFERRED_OUTPUT_HINTS = (
    "virtualmidisynth",
    "fluidsynth",
    "fluid synth",
    "qsynth",
    "synth input",
    "timidity",
)
_LOW_PRIORITY_OUTPUT_HINTS = (
    "midi through",
    "qjackctl",
)


def _decodeMidiName(name):
    if isinstance(name, bytes):
        return name.decode("utf-8", "replace")
    if name is None:
        return None
    return str(name)

from PyQt5.QtCore import QThread, QTimer, pyqtSignal, QObject, Qt
import atexit
import time

try:
    if _IS_WINDOWS:
        raise ImportError("Windows MIDI uses WinMM")
    import pygame
    import pygame.midi
    _HAS_PYGAME = True

    def getDefaultId():
        return pygame.midi.get_default_output_id()

    def iterDeviceIds():
        return range(pygame.midi.get_count())

    def getDeviceInfo(deviceId):
        int_, name, isIn, isOut, isOpen = pygame.midi.get_device_info(deviceId)
        name = _decodeMidiName(name)
        return name, isIn == 1, isOut == 1, isOpen == 1

    def cleanup():
        _PLAYER.cleanup()
        pygame.mixer.quit()
        pygame.midi.quit()
        pygame.quit()  # IGNORE:no-member

except ImportError:
    _HAS_PYGAME = False

    def getDefaultId():
        return -1

    def iterDeviceIds():
        return iter([])

    def getDeviceInfo(deviceId_):
        return None, False, False, False

    def cleanup():
        if _PLAYER is not None:
            _PLAYER.cleanup()


_MAXPNAMELEN = 32
_CALLBACK_NULL = 0
_MMSYSERR_NOERROR = 0
_MMSYSERR_STILLPLAYING = 65
_MIDI_MAPPER = 0xFFFFFFFF


class MIDIHDR(ctypes.Structure):
    _fields_ = [
        ("lpData", ctypes.c_char_p),
        ("dwBufferLength", wintypes.DWORD),
        ("dwBytesRecorded", wintypes.DWORD),
        ("dwUser", ctypes.c_size_t),
        ("dwFlags", wintypes.DWORD),
        ("lpNext", ctypes.c_void_p),
        ("reserved", ctypes.c_size_t),
        ("dwOffset", wintypes.DWORD),
        ("dwReserved", ctypes.c_size_t * 8),
    ]


class MIDIOUTCAPSW(ctypes.Structure):
    _fields_ = [
        ("wMid", wintypes.WORD),
        ("wPid", wintypes.WORD),
        ("vDriverVersion", wintypes.UINT),
        ("szPname", wintypes.WCHAR * _MAXPNAMELEN),
        ("wTechnology", wintypes.WORD),
        ("wVoices", wintypes.WORD),
        ("wNotes", wintypes.WORD),
        ("wChannelMask", wintypes.WORD),
        ("dwSupport", wintypes.DWORD),
    ]


class WinMMError(RuntimeError):
    pass


if _IS_WINDOWS:
    _WINMM = ctypes.WinDLL("winmm")
    _WINMM.midiOutGetNumDevs.restype = wintypes.UINT
    _WINMM.midiOutGetDevCapsW.argtypes = [
        ctypes.c_size_t, ctypes.POINTER(MIDIOUTCAPSW), wintypes.UINT]
    _WINMM.midiOutGetDevCapsW.restype = wintypes.UINT
    _WINMM.midiOutOpen.argtypes = [
        ctypes.POINTER(ctypes.c_void_p), ctypes.c_size_t, ctypes.c_size_t,
        ctypes.c_size_t, wintypes.DWORD]
    _WINMM.midiOutOpen.restype = wintypes.UINT
    _WINMM.midiOutShortMsg.argtypes = [ctypes.c_void_p, wintypes.DWORD]
    _WINMM.midiOutShortMsg.restype = wintypes.UINT
    _WINMM.midiOutPrepareHeader.argtypes = [
        ctypes.c_void_p, ctypes.POINTER(MIDIHDR), wintypes.UINT]
    _WINMM.midiOutPrepareHeader.restype = wintypes.UINT
    _WINMM.midiOutLongMsg.argtypes = [
        ctypes.c_void_p, ctypes.POINTER(MIDIHDR), wintypes.UINT]
    _WINMM.midiOutLongMsg.restype = wintypes.UINT
    _WINMM.midiOutUnprepareHeader.argtypes = [
        ctypes.c_void_p, ctypes.POINTER(MIDIHDR), wintypes.UINT]
    _WINMM.midiOutUnprepareHeader.restype = wintypes.UINT
    _WINMM.midiOutReset.argtypes = [ctypes.c_void_p]
    _WINMM.midiOutReset.restype = wintypes.UINT
    _WINMM.midiOutClose.argtypes = [ctypes.c_void_p]
    _WINMM.midiOutClose.restype = wintypes.UINT
    _WINMM.midiOutGetErrorTextW.argtypes = [
        wintypes.UINT, wintypes.LPWSTR, wintypes.UINT]
    _WINMM.midiOutGetErrorTextW.restype = wintypes.UINT
else:
    _WINMM = None


def _winmm_error_text(error):
    if not _IS_WINDOWS:
        return str(error)
    buffer = ctypes.create_unicode_buffer(256)
    result = _WINMM.midiOutGetErrorTextW(error, buffer, len(buffer))
    if result == _MMSYSERR_NOERROR and buffer.value:
        return buffer.value
    return "WinMM error %s" % error


def _check_winmm(error, action):
    if error != _MMSYSERR_NOERROR:
        raise WinMMError("%s: %s" % (action, _winmm_error_text(error)))


def _winmm_device_name(deviceId):
    caps = MIDIOUTCAPSW()
    result = _WINMM.midiOutGetDevCapsW(
        ctypes.c_size_t(deviceId), ctypes.byref(caps), ctypes.sizeof(caps))
    if result != _MMSYSERR_NOERROR:
        return None
    return caps.szPname


def list_winmm_output_ports():
    if not _IS_WINDOWS:
        return []
    ports = []
    mapperName = _winmm_device_name(_MIDI_MAPPER)
    if mapperName:
        ports.append(MidiDevice(_MIDI_MAPPER, mapperName, _WINMM_DRIVER))
    for deviceId in range(_WINMM.midiOutGetNumDevs()):
        name = _winmm_device_name(deviceId)
        if name:
            ports.append(MidiDevice(deviceId, name, _WINMM_DRIVER))
    return ports


class BackendManager(object):
    @staticmethod
    def output_drivers():
        drivers = []
        if _IS_WINDOWS:
            drivers.append("winmm")
            drivers.append(_WINMM_DRIVER)
        if _HAS_PYGAME:
            drivers.append(_PYGAME_DRIVER)
            if not _IS_WINDOWS:
                drivers.append(_PYGAME_MIXER_DRIVER)
        return drivers


class MidiOutput(QObject):
    supportsTimestamps = True

    def open(self, deviceId):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()

    def write(self, events):
        raise NotImplementedError()

    def abort(self):
        self.close()


class PygameOutput(MidiOutput):
    supportsTimestamps = False

    def __init__(self, parent=None):
        super(PygameOutput, self).__init__(parent)
        self._output = None

    def open(self, deviceId):
        self._output = pygame.midi.Output(deviceId, _LATENCY, _BUFSIZE)
        self.write([[[_PERCUSSION_NOTE_ON, 38, 0], pygame.midi.time()]])

    def abort(self):
        # PortMidi's ALSA abort path only prints a warning; Qt scheduling
        # keeps future events out of the pygame queue.
        pass

    def close(self):
        if self._output is not None:
            try:
                self._output.close()
            except Exception:
                pass
            self._output = None

    def write(self, events):
        if self._output is None:
            raise RuntimeError("MIDI output is not open")
        for offset in range(0, len(events), _PYGAME_MAX_EVENT_BATCH):
            self._output.write(events[offset:offset + _PYGAME_MAX_EVENT_BATCH])


class PygameMixerOutput(MidiOutput):
    supportsTimestamps = False
    playsMidiFiles = True

    def __init__(self, parent=None):
        super(PygameMixerOutput, self).__init__(parent)
        self._midiData = None

    def open(self, deviceId):
        if deviceId != _PYGAME_MIXER_DEVICE_ID:
            raise RuntimeError("Invalid pygame mixer device ID")
        self._midiData = None

    def close(self):
        self.abort()
        self._midiData = None

    def abort(self):
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass

    def write(self, events):
        pass

    def playMidiData(self, midiData):
        self.abort()
        self._midiData = BytesIO(midiData)
        try:
            pygame.mixer.music.load(self._midiData, "mid")
        except TypeError:
            self._midiData.seek(0, 0)
            pygame.mixer.music.load(self._midiData)
        pygame.mixer.music.play()


class WinMMOutput(MidiOutput):
    supportsTimestamps = False

    def __init__(self, parent=None):
        super(WinMMOutput, self).__init__(parent)
        self._handle = ctypes.c_void_p()

    def open(self, deviceId):
        self.close()
        result = _WINMM.midiOutOpen(
            ctypes.byref(self._handle), ctypes.c_size_t(deviceId),
            0, 0, _CALLBACK_NULL)
        _check_winmm(result, "midiOutOpen")
        self.send_short_message(_PERCUSSION_NOTE_ON, 38, 0)

    def close(self):
        if self._handle:
            try:
                _WINMM.midiOutReset(self._handle)
            finally:
                _WINMM.midiOutClose(self._handle)
                self._handle = ctypes.c_void_p()

    def abort(self):
        if self._handle:
            _WINMM.midiOutReset(self._handle)

    def write(self, events):
        for event in events:
            message = event[0]
            if len(message) == 1 and isinstance(message[0], (bytes, bytearray)):
                self.send_sysex(message[0])
            elif message and message[0] != 0xFF:
                data1 = message[1] if len(message) > 1 else 0
                data2 = message[2] if len(message) > 2 else 0
                self.send_short_message(message[0], data1, data2)

    def send_short_message(self, status, data1=0, data2=0):
        if not self._handle:
            raise WinMMError("MIDI output is not open")
        packed = status | (data1 << 8) | (data2 << 16)
        result = _WINMM.midiOutShortMsg(self._handle, packed)
        _check_winmm(result, "midiOutShortMsg")

    def send_sysex(self, data):
        if not self._handle:
            raise WinMMError("MIDI output is not open")
        buffer = ctypes.create_string_buffer(bytes(data))
        header = MIDIHDR()
        header.lpData = ctypes.cast(buffer, ctypes.c_char_p)
        header.dwBufferLength = len(data)
        size = ctypes.sizeof(header)
        _check_winmm(_WINMM.midiOutPrepareHeader(
            self._handle, ctypes.byref(header), size), "midiOutPrepareHeader")
        try:
            _check_winmm(_WINMM.midiOutLongMsg(
                self._handle, ctypes.byref(header), size), "midiOutLongMsg")
            while True:
                result = _WINMM.midiOutUnprepareHeader(
                    self._handle, ctypes.byref(header), size)
                if result != _MMSYSERR_STILLPLAYING:
                    _check_winmm(result, "midiOutUnprepareHeader")
                    break
                time.sleep(0.01)
        except Exception:
            _WINMM.midiOutUnprepareHeader(self._handle, ctypes.byref(header), size)
            raise


class MidiDevice(object):
    def __init__(self, deviceId, name=None, driver=_PYGAME_DRIVER):
        self.deviceId = deviceId
        self.driver = driver
        if name is None:
            self.name, in_, self._isOutput, self._isOpen = getDeviceInfo(deviceId)
        else:
            self.name = name
            self._isOutput = True
            self._isOpen = False
        self.name = _decodeMidiName(self.name)
        self._isValid = self.name is not None

    def isValid(self):
        return self._isValid

    def isOutput(self):
        return self._isOutput

    def isOpen(self):
        if self.driver in (_WINMM_DRIVER, _PYGAME_MIXER_DRIVER):
            return False
        return getDeviceInfo(self.deviceId)[3]


_OUTPUT_DEVICES = []


def _outputDevicePriority(device):
    name = (device.name or "").lower()
    if any(hint in name for hint in _PREFERRED_OUTPUT_HINTS):
        return 0
    if any(hint in name for hint in _LOW_PRIORITY_OUTPUT_HINTS):
        return 2
    return 1


def _outputDeviceSortKey(device):
    if _IS_WINDOWS:
        name = device.name or ""
        lowerName = name.lower()
        return (0 if "virtualmidisynth" in lowerName else
                1 if device.deviceId != _MIDI_MAPPER else 2,
                lowerName)
    return (_outputDevicePriority(device),
            (device.name or "").lower(),
            device.deviceId)


def refreshOutputDevices():
    while _OUTPUT_DEVICES:
        _OUTPUT_DEVICES.pop()
    if _IS_WINDOWS:
        _OUTPUT_DEVICES.extend(list_winmm_output_ports())
        _OUTPUT_DEVICES.sort(key=_outputDeviceSortKey)
        return
    try:
        deviceIds = iterDeviceIds()
    except RuntimeError:
        return
    for devId in deviceIds:
        try:
            device = MidiDevice(devId)
        except Exception as exc:
            print("MIDI device unavailable on %s: %s" % (devId, exc))
            continue
        if device.isOutput():
            _OUTPUT_DEVICES.append(device)
    if _HAS_PYGAME:
        _OUTPUT_DEVICES.append(MidiDevice(
            _PYGAME_MIXER_DEVICE_ID,
            _PYGAME_MIXER_DEVICE_NAME,
            _PYGAME_MIXER_DRIVER))
    _OUTPUT_DEVICES.sort(key=_outputDeviceSortKey)


def iterMidiDevices():
    return iter(_OUTPUT_DEVICES)


def _candidateOutputIds(preferred=None, fallback=True):
    if not _OUTPUT_DEVICES:
        refreshOutputDevices()
    usedPorts = set()
    if preferred is not None:
        if preferred != -1:
            usedPorts.add(preferred)
            yield preferred
        if not fallback:
            return
    if _IS_WINDOWS:
        for dev in _OUTPUT_DEVICES:
            if dev.deviceId not in usedPorts:
                usedPorts.add(dev.deviceId)
                yield dev.deviceId
        return
    defaultId = getDefaultId()
    defaultDevice = next(
        (dev for dev in _OUTPUT_DEVICES if dev.deviceId == defaultId), None)
    if (defaultId != -1 and defaultId not in usedPorts and
            defaultDevice is not None and _outputDevicePriority(defaultDevice) == 0):
        usedPorts.add(defaultId)
        yield defaultId
    for dev in _OUTPUT_DEVICES:
        if dev.deviceId not in usedPorts:
            usedPorts.add(dev.deviceId)
            yield dev.deviceId


def _openOutput(preferred=None, fallback=True):
    for port in _candidateOutputIds(preferred, fallback):
        midiOut = None
        try:
            if _IS_WINDOWS:
                midiOut = WinMMOutput()
            elif port == _PYGAME_MIXER_DEVICE_ID:
                midiOut = PygameMixerOutput()
            else:
                midiOut = PygameOutput()
            midiOut.open(port)
            return port, midiOut
        except Exception as exc:
            name = _deviceName(port)
            print("MIDI output unavailable on %s (%s): %s" %
                  (port, name, exc))
            _closeOutput(midiOut)
    return -1, None


def _deviceName(deviceId):
    if _IS_WINDOWS:
        name = _winmm_device_name(deviceId)
        return name if name is not None else deviceId
    if deviceId == _PYGAME_MIXER_DEVICE_ID:
        return _PYGAME_MIXER_DEVICE_NAME
    try:
        name, unusedIsIn, unusedIsOut, unusedIsOpen = getDeviceInfo(deviceId)
    except Exception:
        return deviceId
    return name


def _closeOutput(midiOut):
    if midiOut is None:
        return
    try:
        midiOut.abort()
    except Exception:
        pass
    try:
        midiOut.close()
    except Exception:
        pass


def _midi_time():
    if _HAS_PYGAME and not _IS_WINDOWS:
        return pygame.midi.time()
    return int(round(time.perf_counter() * 1000))


def _stopTimer(timer):
    try:
        timer.stop()
    except RuntimeError:
        pass


from Data.DBConstants import MIDITICKSPERBEAT


class _midi(QObject):
    def __init__(self):
        super(_midi, self).__init__()
        self._port = None
        self._midiOut = None
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self._measureDetails = []
        self._measureTimer = QTimer()
        self._measureTimer.setSingleShot(True)
        self._measureTimer.timeout.connect(self._highlight)
        self._playbackTimer = QTimer(self)
        self._playbackTimer.setTimerType(Qt.PreciseTimer)
        self._playbackTimer.timeout.connect(self._dispatchOutputEvents)
        self._playbackEvents = []
        self._playbackEventIndex = 0
        self._playbackStartTime = 0
        self._songStart = None
        self._mute = False
        self._musicPlaying = False
        self.kit = None

    def initialize(self):
        if not _MIDI_INITIALIZED:
            raise RuntimeError("MIDI not initialized yet!")
        selectedPort = self._port
        self._port = -1
        self._midiOut = None
        self._port, self._midiOut = _openOutput(
            selectedPort, fallback=selectedPort is None)

    def setPort(self, port):
        oldPort = self._port
        oldMidiOut = self._midiOut
        newPort, newMidiOut = _openOutput(port, fallback=False)
        if newMidiOut is None:
            _closeOutput(oldMidiOut)
            if oldPort is not None and oldPort != -1:
                self._port, self._midiOut = _openOutput(
                    oldPort, fallback=True)
            else:
                self._port = oldPort
                self._midiOut = None
            return
        self._port = newPort
        self._midiOut = newMidiOut
        _closeOutput(oldMidiOut)

    def port(self):
        return self._port

    def isGood(self):
        return self._port != -1 and self._midiOut is not None

    def setMute(self, onOff):
        self._mute = onOff

    def isMuted(self):
        return self._mute

    highlightMeasure = pyqtSignal(int, int)

    def playNote(self, drumIndex, head):
        if self.kit is None or self._mute:
            return
        headData = self.kit[drumIndex].headData(head)
        self.playHeadData(headData)

    def playHeadData(self, headData, when=None):
        if not self._midiOut:
            return
        if when is None:
            when = _midi_time()
        if headData.effect == "flam":
            self._midiOut.write([[[_PERCUSSION_NOTE_ON,
                                   headData.midiNote,
                                   headData.midiVolume // FLAM_VOLUME_CONSTANT],
                                  when]])
            self._midiOut.write([[[_PERCUSSION_NOTE_ON,
                                   headData.midiNote,
                                   headData.midiVolume],
                                  when + FLAM_TIME_CONSTANT]])
        elif headData.effect == "drag":
            self._midiOut.write([[[_PERCUSSION_NOTE_ON,
                                   headData.midiNote,
                                   headData.midiVolume],
                                  when]])
            self._midiOut.write([[[_PERCUSSION_NOTE_ON,
                                   headData.midiNote,
                                   headData.midiVolume],
                                  when + DRAG_TIME_CONSTANT]])
        elif headData.effect == "choke":
            self._midiOut.write([[[_PERCUSSION_NOTE_ON,
                                   headData.midiNote,
                                   headData.midiVolume],
                                  when]])
            self._midiOut.write([[[_PERCUSSION_CHOKE,
                                   _CHOKE_MSG,
                                   _CHOKE_VELOCITY],
                                  when + DRAG_TIME_CONSTANT]])
        else:
            self._midiOut.write([[[_PERCUSSION_NOTE_ON,
                                   headData.midiNote,
                                   headData.midiVolume],
                                  when]])

    def playScore(self, score):
        measureList = list(score.iterMeasuresWithRepeats())
        self._playMIDINow(measureList, score)

    def _playMIDINow(self, measureList, score):
        if self.kit is None or self._mute or not self._midiOut:
            return
        baseTime = 0
        bpm = score.scoreData.bpm
        swing = score.scoreData.swing
        msPerBeat = 60000.0 / bpm
        self._measureDetails = []
        lastMeasureIndex = None
        try:
            for measure, measureIndex in measureList:
                if lastMeasureIndex is None or measureIndex != lastMeasureIndex + 1:
                    bpm = score.bpmAtMeasureByIndex(measureIndex)
                elif measure.newBpm > 0 and bpm != measure.newBpm:
                    bpm = measure.newBpm
                if bpm == 0:
                    bpm = 120
                lastMeasureIndex = measureIndex
                msPerBeat = 60000.0 / bpm
                times = list(measure.counter.iterTimesMs(msPerBeat, swing))
                baseTime += times[-1]
                self._measureDetails.append((measureIndex, baseTime))
            self._measureDetails.reverse()
            self._songStart = time.perf_counter()
            self._musicPlaying = True
            if getattr(self._midiOut, "playsMidiFiles", False):
                midi = BytesIO()
                exportMidi(measureList, score, midi)
                self._midiOut.playMidiData(midi.getvalue())
            else:
                notes, unusedBaseTicks = _calculateMidiTimes(measureList, score)
                startTime = _midi_time()
                events = _makeOutputEvents(notes, startTime)
                if self._midiOut.supportsTimestamps:
                    self._midiOut.write(events)
                else:
                    self._scheduleOutputEvents(events, startTime)
        except Exception as exc:
            global HAS_MIDI
            print("MIDI playback failed: %s" % exc)
            HAS_MIDI = False
            self.cleanup()
            self.timer.timeout.emit()
            return
        self.timer.start(int(round(baseTime + 500)))
        self._measureTimer.start(0)

    def _scheduleOutputEvents(self, events, startTime):
        self._stopOutputScheduler()
        self._playbackEvents = events
        self._playbackEventIndex = 0
        self._playbackStartTime = startTime
        self._dispatchOutputEvents()
        if self._playbackEventIndex < len(self._playbackEvents):
            self._playbackTimer.start(_SCHEDULER_INTERVAL_MS)

    def _dispatchOutputEvents(self):
        if not self._musicPlaying or not self._midiOut:
            self._stopOutputScheduler()
            return
        now = _midi_time()
        dueTime = now + _SCHEDULER_LOOKAHEAD_MS
        batch = []
        while self._playbackEventIndex < len(self._playbackEvents):
            event = self._playbackEvents[self._playbackEventIndex]
            if event[1] > dueTime:
                break
            batch.append(event)
            self._playbackEventIndex += 1
        if batch:
            try:
                self._midiOut.write(batch)
            except Exception as exc:
                print("MIDI playback failed: %s" % exc)
                self.cleanup()
                self.timer.timeout.emit()
                return
        if self._playbackEventIndex >= len(self._playbackEvents):
            _stopTimer(self._playbackTimer)

    def _stopOutputScheduler(self):
        _stopTimer(self._playbackTimer)
        self._playbackEvents = []
        self._playbackEventIndex = 0
        self._playbackStartTime = 0

    def loopBars(self, measureIterator, score, loopCount=100):
        measureList = [(measure, measureIndex) for
                       (measure, measureIndex, unused)
                       in measureIterator] * loopCount
        for index, (measure, measureIndex) in enumerate(measureList):
            if measure.simileDistance > 0:
                measure = score.getReferredMeasure(measureIndex)
                measureList[index] = (measure, measureIndex)
        self._playMIDINow(measureList, score)

    def shutUp(self):
        if self._musicPlaying:
            _stopTimer(self.timer)
            self._measureDetails = []
            _stopTimer(self._measureTimer)
            self._stopOutputScheduler()
            self.highlightMeasure.emit(-1, -1)
            if self._midiOut:
                if self._midiOut.supportsTimestamps:
                    _closeOutput(self._midiOut)
                    self._midiOut = None
                    if self._port is not None and self._port != -1:
                        self._port, self._midiOut = _openOutput(self._port)
                else:
                    try:
                        self._midiOut.abort()
                    except Exception:
                        pass
            self._musicPlaying = False

    def cleanup(self):
        self._stopOutputScheduler()
        self._musicPlaying = False
        if self._midiOut is not None:
            _closeOutput(self._midiOut)
            self._midiOut = None

    def _highlight(self):
        delay = -1
        measureIndex = None
        nextMeasure = -1
        while delay < 0 and self._measureDetails:
            measureIndex, measureEnd = self._measureDetails.pop()
            if self._measureDetails:
                nextMeasure = self._measureDetails[-1][0]
            delay = (measureEnd - 1000 * (time.perf_counter() - self._songStart))
        if measureIndex is not None:
            self.highlightMeasure.emit(measureIndex, nextMeasure)
        else:
            self.highlightMeasure.emit(-1, -1)
        if delay > 0:
            self._measureTimer.start(int(round(delay)))


_PLAYER = _midi()
SONGEND_SIGNAL = _PLAYER.timer.timeout
HIGHLIGHT_SIGNAL = _PLAYER.highlightMeasure


def setKit(drumKit):
    _PLAYER.kit = drumKit


def playNote(drumIndex, head):
    _PLAYER.playNote(drumIndex, head)


def playHeadData(headData):
    _PLAYER.playHeadData(headData)


def playScore(score):
    _PLAYER.playScore(score)


def loopBars(measureIterator, score, loopCount=100):
    _PLAYER.loopBars(measureIterator, score, loopCount)


def shutUp():
    _PLAYER.shutUp()


def setMute(onOff):
    _PLAYER.setMute(onOff)


def isMuted():
    return _PLAYER.isMuted()


def encodeSevenBitDelta(delta, midiData):
    delta = int(round(delta))
    values = []
    lastByte = True
    if delta <= 0:
        midiData.append(0)
        return
    while delta:
        thisValue = (delta & 0x7F)
        delta >>= 7
        if lastByte:
            lastByte = False
        else:
            thisValue |= 0x80
        values.append(thisValue)
    values.reverse()
    midiData.extend(values)


def _makeMidiStart(score):
    signature = "Created with DrumBurp"
    midiData = []
    midiData.extend([0, 0xff, 0x1, len(signature)])
    midiData.extend([ord(ch) for ch in signature])
    return midiData


def _writeMidiNotes(midiObjects, baseTime):
    lastNoteTime = 0
    midiData = []
    for midiEvent in midiObjects:
        deltaTime = midiEvent.time - lastNoteTime
        lastNoteTime = midiEvent.time
        encodeSevenBitDelta(deltaTime, midiData)
        midiData.extend(midiEvent.write())
    # Turn off drum notes
    deltaTime = baseTime - lastNoteTime
    # Insert a delay before the end of the track.
    encodeSevenBitDelta(deltaTime + 4 * MIDITICKSPERBEAT, midiData)
    midiData.extend([_PERCUSSION_NOTE_OFF, 38, 0])
    encodeSevenBitDelta(0, midiData)
    midiData.extend([0xFF, 0x2F, 0])
    return midiData


def _finishMidiData(midiData):
    numBytes = len(midiData)
    lenBytes = [((numBytes >> i) & 0xff) for i in range(24, -8, -8)]
    return lenBytes + midiData


class MidiObject(object):
    def __init__(self, eventTime):
        self.time = int(round(eventTime))

    def _sortKey(self):
        return (self.time, self.__class__.__name__)

    def __lt__(self, other):
        return self._sortKey() < other._sortKey()

    def write(self):
        raise NotImplementedError()


class MidiTempoChange(MidiObject):
    def __init__(self, eventTime, bpm):
        super(MidiTempoChange, self).__init__(eventTime)
        self.bpm = bpm

    def write(self):
        msPerBeat = int(60000000 / self.bpm)
        return [0xff, 0x51, 0x03, (msPerBeat >> 16) & 0xff,
                (msPerBeat >> 8) & 0xff, msPerBeat & 0xff]


class MidiNote(MidiObject):
    def __init__(self, noteTime, headData):
        super(MidiNote, self).__init__(noteTime)
        self.headData = headData

    def write(self):
        return [_PERCUSSION_NOTE_ON, self.headData.midiNote,
                int(self.headData.midiVolume)]


class MidiChoke(MidiObject):
    def write(self):
        return [_PERCUSSION_CHOKE, _CHOKE_MSG, _CHOKE_VELOCITY]


def _makeOutputEvents(midiObjects, startTime):
    events = []
    bpm = 120
    lastTick = 0
    currentMs = 0.0
    sortedObjects = sorted(
        midiObjects,
        key=lambda obj: (obj.time, 0 if isinstance(obj, MidiTempoChange) else 1))
    for midiEvent in sortedObjects:
        currentMs += ((midiEvent.time - lastTick) * 60000.0 /
                      (bpm * MIDITICKSPERBEAT))
        lastTick = midiEvent.time
        if isinstance(midiEvent, MidiTempoChange):
            bpm = midiEvent.bpm
        else:
            events.append([midiEvent.write(), int(round(startTime + currentMs))])
    return events


def _calculateMidiTimes(measureIterator, score):
    notes = []
    baseTime = 1
    lastBpm = None
    lastMeasureIndex = None
    swing = score.scoreData.swing
    for measure, measureIndex in measureIterator:
        measureNotes = []
        times = list(measure.counter.iterMidiTicks(swing))
        if lastMeasureIndex is None or measureIndex != lastMeasureIndex + 1:
            bpm = score.bpmAtMeasureByIndex(measureIndex)
        elif measure.newBpm > 0 and bpm != measure.newBpm:
            bpm = measure.newBpm
        lastMeasureIndex = measureIndex
        if bpm == 0:
            bpm = 120
        if bpm != lastBpm:
            notes.append(MidiTempoChange(baseTime + times[0], bpm))
            lastBpm = bpm
        for notePos, head in measure:
            drumData = score.drumKit[notePos.drumIndex]
            headData = drumData.headData(head)
            if headData is not None:
                noteTime = baseTime + times[notePos.noteTime]
                divisionTicks = times[notePos.noteTime +
                                      1] - times[notePos.noteTime]
                if headData.effect == "flam":
                    headCopy = copy.copy(headData)
                    headCopy.midiVolume = headData.midiVolume // FLAM_VOLUME_CONSTANT
                    measureNotes.append(
                        MidiNote(noteTime - (MIDITICKSPERBEAT // FLAM_TIME_CONSTANT), headCopy))
                elif headData.effect == "drag":
                    measureNotes.append(
                        MidiNote(noteTime + divisionTicks // 2, headData))
                elif headData.effect == "choke":
                    measureNotes.append(
                        MidiChoke(noteTime + divisionTicks // 2))
                measureNotes.append(MidiNote(noteTime, headData))
        baseTime += times[-1]
        measureNotes.sort()
        notes.extend(measureNotes)
    return notes, baseTime


def exportMidi(measureIterator, score, handle):
    handle.write(b"MThd\x00\x00\x00\x06\x00\x00\x00\x01")
    handle.write(bytes([(MIDITICKSPERBEAT >> 8) & 0xFF]))
    handle.write(bytes([(MIDITICKSPERBEAT >> 0) & 0xFF]))
    notes, baseTime = _calculateMidiTimes(measureIterator, score)
    midiData = _makeMidiStart(score)
    midiData += _writeMidiNotes(notes, baseTime)
    midiData = _finishMidiData(midiData)
    handle.write(b"MTrk")
    handle.write(bytes(midiData))


def selectMidiDevice(dev):
    global HAS_MIDI
    _PLAYER.cleanup()
    _PLAYER.setPort(dev.deviceId)
    HAS_MIDI = _PLAYER.isGood() if _IS_WINDOWS else _HAS_PYGAME and _PLAYER.isGood()
    return HAS_MIDI and _PLAYER.port() == dev.deviceId


def currentDevice():
    for dev in _OUTPUT_DEVICES:
        if dev.deviceId == _PLAYER.port():
            return dev
    return None


def _initialize():
    global HAS_MIDI, _MIDI_INITIALIZED
    if _MIDI_INITIALIZED:
        return
    try:
        if _HAS_PYGAME and not _IS_WINDOWS:
            pygame.init()  # IGNORE:no-member
            pygame.midi.init()
            pygame.mixer.init(_FREQ, _BITSIZE, _CHANNELS, _NUMSAMPLES)
            pygame.mixer.music.set_volume(0.8)
        _MIDI_INITIALIZED = True
        _PLAYER.initialize()
        HAS_MIDI = _PLAYER.isGood() if _IS_WINDOWS else _HAS_PYGAME and _PLAYER.isGood()
    except Exception as exc:
        print("MIDI unavailable: %s" % exc)
        HAS_MIDI = False
        _MIDI_INITIALIZED = True
    atexit.register(cleanup)


class MidiInit(QThread):
    def run(self):  # IGNORE:no-self-use
        _initialize()


def main():
    _initialize()
    refreshOutputDevices()
    for device in iterMidiDevices():
        print(device.name)


if __name__ == "__main__":
    main()
