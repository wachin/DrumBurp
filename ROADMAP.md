# DrumBurp Roadmap

This roadmap tracks follow-up work after the PyQt5 port, Windows MIDI work, and
Windows build validation. Use the checkboxes to mark progress as each item is
completed.

## File Handling

- [ ] Add manual validation notes for `File -> Recent Scores...`.
- [ ] Confirm that only `.brp` score files are saved in `RecentFiles`.
- [ ] Confirm that dragging a `.brp` file into DrumBurp opens the score.
- [ ] Confirm that dragging unsupported files such as `.md`, `.txt`, `.pdf`, or
  images is ignored or rejected safely.
- [ ] Confirm that opening unsupported files from the command line is rejected
  safely.
- [ ] Confirm that `LastScoreDirectory` remembers the last folder used to open
  or save a score.

## Windows Launcher

- [ ] Document `run-drumburp.bat` in `README.md`.
- [ ] Document `run-drumburp.bat` in `README_ES.md`.
- [ ] Confirm that double-clicking `run-drumburp.bat` opens DrumBurp normally.
- [ ] Confirm that `run-drumburp.bat --pyinstaller-test` exits with code `0`.
- [ ] Confirm that the launcher preserves normal settings and recent score
  behavior.

## Tests

- [x] Replace deprecated `self.assert_(...)` test calls with
  `self.assertTrue(...)`.
- [x] Confirm the full unit test suite passes locally on Python 3.13.
- [ ] Add focused tests for valid and invalid score filename handling.
- [ ] Add focused tests for recent score filtering.
- [ ] Add focused tests for last score directory persistence.
- [ ] Decide whether GitHub Actions should run tests on both Python 3.11 and
  Python 3.13.
- [ ] If Python 3.13 is officially supported, add it to the CI test matrix.

## Python Modernization

- [x] Replace deprecated `optparse` usage with `argparse`.
- [ ] Review remaining code for deprecated Python APIs.
- [ ] Review whether the project should officially support Python 3.11 only,
  Python 3.13 only, or both.
- [ ] Document the recommended Python version for development.
- [ ] Document the recommended Python version for release builds.

## Line Endings

- [ ] Add a `.gitattributes` file to reduce LF/CRLF warning noise.
- [ ] Prefer LF for source files such as `.py`, `.md`, `.yml`, `.yaml`, `.ui`,
  `.qrc`, and translation files.
- [ ] Prefer CRLF for Windows command files such as `.bat`, `.cmd`, and `.ps1`.
- [ ] Re-normalize tracked files after adding `.gitattributes`.
- [ ] Confirm that future commits no longer produce avoidable LF/CRLF warnings.

## GitHub Actions

- [x] Confirm that the manual `workflow_dispatch` build passes on GitHub
  Actions.
- [x] Confirm that Windows, Linux, and macOS build jobs pass.
- [x] Confirm that Windows, Linux, and macOS smoke tests pass.
- [x] Confirm that the Windows `db_windows` artifact is generated.
- [ ] Download and test release artifacts after a tag-triggered release.
- [ ] Review GitHub Actions Node.js 20 deprecation warnings.
- [ ] Update GitHub Actions versions or configuration when Node.js 24 support is
  required.
- [ ] Decide whether `windows-latest` should be pinned to a specific Windows
  runner image.

## Windows Build And Release

- [x] Confirm that `build/build_windows.ps1` creates the NSIS installer.
- [x] Confirm that the Windows installer can be installed silently.
- [x] Confirm that `DrumBurp.exe --pyinstaller-test` passes after installation.
- [ ] Test a real `vX.Y.Z` tag release.
- [ ] Confirm that the GitHub Release contains the Windows installer.
- [ ] Confirm that the GitHub Release contains the Linux binary.
- [ ] Confirm that the GitHub Release contains the macOS zip.
- [ ] Document the release checklist in one place.

## MIDI

- [x] Confirm native Windows MIDI playback through WinMM.
- [x] Confirm `VirtualMIDISynth #1` works as a MIDI output device.
- [x] Confirm `MIDI -> Select MIDI out` works on Windows.
- [ ] Re-test MIDI output selection on Linux.
- [ ] Re-test MIDI output selection on macOS if MIDI devices are available.
- [ ] Document any JACK or soundfont workflow that Linux users may need.

## Qt And UI Warnings

- [ ] Investigate the startup warning:
  `QWidget::setTabOrder: 'first' and 'second' must be in the same window`.
- [ ] Fix the Qt tab-order warning if it is caused by the `.ui` file.
- [ ] Check whether startup console warnings can be reduced without hiding real
  errors.

## Documentation

- [ ] Keep `README.md` and `README_ES.md` in sync for Windows launch
  instructions.
- [ ] Document the VirtualMIDISynth setup clearly for Windows users.
- [ ] Document supported score file extensions.
- [ ] Document the recommended build environment for Windows.
- [ ] Document how to run tests locally.
- [ ] Document how to run the GitHub Actions workflow manually.

