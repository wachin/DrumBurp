# DrumBurp Roadmap

This roadmap tracks follow-up work after the PyQt5 port, Windows MIDI work, and
Windows build validation. Use the checkboxes to mark progress as each item is
completed.

## File Handling

- [x] Add manual validation notes for `File -> Recent Scores...`.
- [ ] Confirm that only `.brp` score files are saved in `RecentFiles`.
- [ ] Confirm that dragging a `.brp` file into DrumBurp opens the score.
- [ ] Confirm that dragging unsupported files such as `.md`, `.txt`, `.pdf`, or
  images is ignored or rejected safely.
- [ ] Confirm that opening unsupported files from the command line is rejected
  safely.
- [ ] Confirm that `LastScoreDirectory` remembers the last folder used to open
  or save a score.

Manual validation notes:

1. Open DrumBurp with `run-drumburp.bat`.
2. Open a valid `.brp` score from `File -> Open`.
3. Close and reopen DrumBurp.
4. Confirm the score appears under `File -> Recent Scores...`.
5. Drag the same `.brp` score into the DrumBurp window and confirm it opens.
6. Drag unsupported files such as `.md`, `.txt`, `.pdf`, or an image into the
   DrumBurp window and confirm they are ignored or rejected safely.
7. Run `py .\src\DrumBurp.py README.md` and confirm DrumBurp does not load the
   Markdown file as a score.
8. Open a score from a different folder, then use `File -> Open` again and
   confirm the file dialog starts from the last score folder.

## Windows Launcher

- [x] Document `run-drumburp.bat` in `README.md`.
- [x] Document `run-drumburp.bat` in `README_ES.md`.
- [ ] Confirm that double-clicking `run-drumburp.bat` opens DrumBurp normally.
- [x] Confirm that `run-drumburp.bat --pyinstaller-test` exits with code `0`.
- [ ] Confirm that the launcher preserves normal settings and recent score
  behavior.

## Tests

- [x] Replace deprecated `self.assert_(...)` test calls with
  `self.assertTrue(...)`.
- [x] Confirm the full unit test suite passes locally on Python 3.13.
- [x] Add focused tests for valid and invalid score filename handling.
- [x] Add focused tests for recent score filtering.
- [x] Add focused tests for last score directory persistence.
- [x] Decide whether GitHub Actions should run tests on both Python 3.11 and
  Python 3.13.
- [x] If Python 3.13 is officially supported, add it to the CI test matrix.

## Python Modernization

- [x] Replace deprecated `optparse` usage with `argparse`.
- [x] Review remaining code for deprecated Python APIs.
- [x] Review whether the project should officially support Python 3.11 only,
  Python 3.13 only, or both.
- [x] Document the recommended Python version for development.
- [x] Document the recommended Python version for release builds.

## Line Endings

- [x] Add a `.gitattributes` file to reduce LF/CRLF warning noise.
- [x] Prefer LF for source files such as `.py`, `.md`, `.yml`, `.yaml`, `.ui`,
  `.qrc`, and translation files.
- [x] Prefer CRLF for Windows command files such as `.bat`, `.cmd`, and `.ps1`.
- [x] Re-normalize tracked files after adding `.gitattributes`.
- [ ] Confirm that future commits no longer produce avoidable LF/CRLF warnings.

## GitHub Actions

- [x] Confirm that the manual `workflow_dispatch` build passes on GitHub
  Actions.
- [x] Confirm that Windows, Linux, and macOS build jobs pass.
- [x] Confirm that Windows, Linux, and macOS smoke tests pass.
- [x] Confirm that the Windows `db_windows` artifact is generated.
- [ ] Download and test release artifacts after a tag-triggered release.
- [x] Review GitHub Actions Node.js 20 deprecation warnings.
- [x] Update GitHub Actions versions or configuration when Node.js 24 support is
  required.
- [x] Decide whether `windows-latest` should be pinned to a specific Windows
  runner image.

## Windows Build And Release

- [x] Confirm that `build/build_windows.ps1` creates the NSIS installer.
- [x] Confirm that the Windows installer can be installed silently.
- [x] Confirm that `DrumBurp.exe --pyinstaller-test` passes after installation.
- [ ] Test a real `vX.Y.Z` tag release.
- [ ] Confirm that the GitHub Release contains the Windows installer.
- [ ] Confirm that the GitHub Release contains the Linux binary.
- [ ] Confirm that the GitHub Release contains the macOS zip.
- [x] Document the release checklist in one place.

Release checklist:

1. Confirm `master` is clean and pushed.
2. Confirm the latest manual GitHub Actions build passes.
3. Confirm local Windows validation still passes:
   `run-drumburp.bat --pyinstaller-test`.
4. Confirm local unit tests pass:
   `py -m unittest discover -s src\test`.
5. Create a version tag such as `v1.1.4`.
6. Push the tag to GitHub.
7. Confirm the tag-triggered workflow completes.
8. Confirm the GitHub Release contains the Windows installer, Linux binary, and
   macOS zip.
9. Download the release assets and smoke-test them on the target platforms.

## MIDI

- [x] Confirm native Windows MIDI playback through WinMM.
- [x] Confirm `VirtualMIDISynth #1` works as a MIDI output device.
- [x] Confirm `MIDI -> Select MIDI out` works on Windows.
- [ ] Re-test MIDI output selection on Linux.
- [ ] Re-test MIDI output selection on macOS if MIDI devices are available.
- [x] Document any JACK or soundfont workflow that Linux users may need.

## Internationalization

- [x] Translate the measure context menu shown when right-clicking a tablature
  measure.
- [x] Translate the measure-line context menu shown when right-clicking a
  barline or row boundary (`Repeat End`, `Section End`, `Line Break`, and
  repeat count actions).
- [x] Translate the measure-count context menu and subdivision submenu shown
  when right-clicking count text.
- [x] Reuse bilingual count names in the simple-count and complex-count
  selectors used when creating or editing scores.
- [x] Widen the New Score dialog and count selector so bilingual rhythm names
  are not truncated.
- [x] Show bilingual translations for common section titles in the section
  navigator without modifying the titles stored in `.brp` files.
- [x] Reuse bilingual section titles in the `Insert -> Section Copy` submenu.
- [x] Correct the Spanish singular spelling `sección` in translated UI text.
- [x] Translate the Edit Colours dialog, including dynamic element names and
  border-style selectors, without changing saved colour-scheme values.
- [x] Update `drumburp_en.ts` and `drumburp_es.ts` after adding new
  translatable strings.
- [x] Compile updated `drumburp_en.qm` and `drumburp_es.qm`.
- [x] Confirm `drumburp_en.ts` and `drumburp_es.ts` have no unfinished
  translations.
- [ ] Manually review common Spanish UI paths before creating a release.
- [ ] Continue reviewing right-click menus for untranslated strings in other
  score areas.
- [ ] Review dialog titles, warning messages, and MIDI messages in Spanish.

## Qt And UI Warnings

- [x] Investigate the startup warning:
  `QWidget::setTabOrder: 'first' and 'second' must be in the same window`.
- [x] Fix the Qt tab-order warning if it is caused by the `.ui` file.
- [ ] Check whether startup console warnings can be reduced without hiding real
  errors.

## Documentation

- [x] Keep `README.md` and `README_ES.md` in sync for Windows launch
  instructions.
- [x] Document the VirtualMIDISynth setup clearly for Windows users.
- [x] Document supported score file extensions.
- [x] Document the recommended build environment for Windows.
- [x] Document how to run tests locally.
- [x] Document how to run the GitHub Actions workflow manually.
