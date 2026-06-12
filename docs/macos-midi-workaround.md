# macOS MIDI initialization workaround

Date: 2026-06-12

## Problem

DrumBurp crashes during startup on macOS.

Observed environment:

- macOS Big Sur 11.7.1
- VMware Workstation 17
- Python 3.12.9
- PyQt5 5.15.11
- pygame 2.5.2 and 2.6.1

Crash report:

- EXC_BAD_INSTRUCTION (SIGILL)
- Crashed Thread: MidiInit

## Root cause

pygame/SDL MIDI initialization was being executed from
a background thread.

macOS requires parts of SDL initialization to run on
the main thread.

## Workaround

On macOS:

    if sys.platform == "darwin":
        DBMidi._initialize()
        self._midiInitFinished()
    else:
        self._midiInitThread.start()

On Windows/Linux:

    self._midiInitThread.start()

## Revert procedure

Restore the original code:

    self._midiInitThread.start()

and retest on:

- Windows
- Linux
- macOS

before merging.