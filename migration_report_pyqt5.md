# Migration Report: PyQt4 -> PyQt5

**Project:** DrumBurp — drum notation editor in Python/PyQt  
**Repository:** https://github.com/Whatang/DrumBurp  
**Port by:** Washington Indacochea Delgado  
**Contact:** linuxfrontier@proton.me  
**Started:** 2026-03-28  
**Target system:** Debian 12 / UbuntuStudio, Python 3.11, PyQt5 5.15.x

> This document replaces and absorbs the file `informe_pyqt4.txt`, which was
> the starting point of the work: a dump of all original PyQt4 imports in the
> project. That file is no longer needed.

---

## Starting point — original PyQt4 imports

The following listing is the original content of `informe_pyqt4.txt`: all files
that imported PyQt4 before the migration began. It is preserved here as a
historical reference to understand the scope of the work carried out.

```
build/install_pyqt.ps1        from PyQt4 (Windows installer)
build/build_linux.sh          --hidden-import=PyQt4.QtGui
.github/workflows/build.yml   Cache PyQt4 / Install PyQt4 / Import PyQt4
pylintrc                      extension-pkg-whitelist=PyQt4

src/DrumBurp.py               from PyQt4.QtGui import QApplication
src/buttons_rc.py             from PyQt4 import QtCore
src/PyQt4/__init__.py         PyQt4->PyQt5 compatibility layer
src/PyQt4/QtCore.py           PyQt4->PyQt5 compatibility layer

src/Widgets/ScoreView.py      from PyQt4 import QtGui, QtCore
src/Widgets/ScoreView_plugin.py  from PyQt4.QtDesigner import QPyDesignerCustomWidgetPlugin
src/Widgets/measureTabs.py    from PyQt4.QtGui import QWidget
src/Widgets/measureTabs_plugin.py  from PyQt4.QtDesigner import QPyDesignerCustomWidgetPlugin
src/Widgets/buttons_rc.py     from PyQt4 import QtCore
src/Widgets/ui_measureTabs.py from PyQt4 import QtCore, QtGui

src/GUI/DBColourPicker.py     from PyQt4.QtGui import ...; from PyQt4 import QtCore
src/GUI/DBCommands.py         from PyQt4.QtGui import QUndoCommand
src/GUI/DBFonts.py            from PyQt4.Qt import QFontDatabase, QFont
src/GUI/DBFSM.py              from PyQt4 import QtCore
src/GUI/DBIcons.py            from PyQt4 import QtGui
src/GUI/DBInfoDialog.py       from PyQt4.QtGui import QDialog; from PyQt4.QtCore import pyqtSignature
src/GUI/DBLicense.py          from PyQt4.QtGui import QDialog
src/GUI/DBMainwindow.py       from PyQt4.QtCore import pyqtSignature, QSettings, QVariant, ...
src/GUI/DBMidi.py             from PyQt4.Qt import QThread; from PyQt4.QtCore import QTimer, ...
src/GUI/DBStartupDialog.py    from PyQt4.QtGui import QDialog
src/GUI/DrumBurp_rc.py        from PyQt4 import QtCore
src/GUI/LilypondExporter.py   from PyQt4.Qt import QThread
src/GUI/QAlternateDialog.py   from PyQt4 import QtGui
src/GUI/QAlternateWidget.py   from PyQt4.QtGui import QWidget
src/GUI/QComplexCountDialog.py  from PyQt4.QtGui import QDialog, QListWidgetItem; QVariant, pyqtSignature
src/GUI/QDefaultKitManager.py from PyQt4 import QtGui, QtCore
src/GUI/QDisplayProperties.py from PyQt4.QtCore import QObject, pyqtSignal; from PyQt4.QtGui import ...
src/GUI/QEditKitDialog.py     from PyQt4.QtGui import QDialog, QRadioButton, QFileDialog, ...
src/GUI/QEditMeasureDialog.py from PyQt4.QtGui import QDialog
src/GUI/QGraphicsListData.py  from PyQt4.QtGui import QGraphicsItem, QFontMetrics, QPen
src/GUI/QInsertMeasuresDialog.py  from PyQt4.QtGui import QDialog
src/GUI/QLilypondPreview.py   from PyQt4.QtCore import pyqtSignal, QTimeLine; from PyQt4.QtGui import ...
src/GUI/QLineLabel.py         from PyQt4 import QtGui, QtCore
src/GUI/QMeasure.py           from PyQt4 import QtGui, QtCore
src/GUI/QMeasureContextMenu.py  from PyQt4 import QtGui
src/GUI/QMeasureLine.py       from PyQt4 import QtGui, QtCore
src/GUI/QMenuIgnoreCancelClick.py  from PyQt4.QtGui import QMenu
src/GUI/QMetaDataDialog.py    from PyQt4.QtGui import QDialog
src/GUI/QNewScoreDialog.py    from PyQt4.QtGui import QDialog; from PyQt4.QtCore import QSettings, QVariant
src/GUI/QNotationScene.py     from PyQt4.QtGui import QGraphicsScene, QPixmap
src/GUI/QRepeatCountDialog.py from PyQt4.QtGui import QDialog
src/GUI/QScore.py             from PyQt4 import QtGui, QtCore; QGraphicsItem; QTransform
src/GUI/QSection.py           from PyQt4.QtGui import QGraphicsTextItem, QTextCursor
src/GUI/QStaff.py             from PyQt4 import QtGui, QtCore
src/GUI/QVersionDownloader.py from PyQt4.QtGui import QDialog; from PyQt4.QtCore import QTimer

src/GUI/ui_DBComplextCountDialog.py  from PyQt4 import QtCore, QtGui
src/GUI/ui_alternateRepeatWidget.py  from PyQt4 import QtCore, QtGui
src/GUI/ui_alternateRepeats.py       from PyQt4 import QtCore, QtGui
src/GUI/ui_asciiDialog.py            from PyQt4 import QtCore, QtGui
src/GUI/ui_dbColours.py              from PyQt4 import QtCore, QtGui
src/GUI/ui_dbInfo.py                 from PyQt4 import QtCore, QtGui
src/GUI/ui_dbLicense.py              from PyQt4 import QtCore, QtGui
src/GUI/ui_dbStartup.py              from PyQt4 import QtCore, QtGui
src/GUI/ui_defaultKitManager.py      from PyQt4 import QtCore, QtGui
src/GUI/ui_drumburp.py               from PyQt4 import QtCore, QtGui
src/GUI/ui_editKit.py                from PyQt4 import QtCore, QtGui
src/GUI/ui_insertMeasuresDialog.py   from PyQt4 import QtCore, QtGui
src/GUI/ui_measurePropertiesDialog.py  from PyQt4 import QtCore, QtGui
src/GUI/ui_newScoreDialog.py         from PyQt4 import QtCore, QtGui
src/GUI/ui_repeatCountDialog.py      from PyQt4 import QtCore, QtGui
src/GUI/ui_scorePropertiesDialog.py  from PyQt4 import QtCore, QtGui
src/GUI/ui_versionDownloader.py      from PyQt4 import QtCore, QtGui
```

All of these imports have been migrated to PyQt5. See the sections below for
the details of each file.

---

## Project context

DrumBurp is a desktop application for creating and editing drum music notation.
It uses PyQt for the graphical interface, QGraphicsScene/QGraphicsItem for the
visual editor, QThread for MIDI and Lilypond export, and QSettings for
persistence.

Relevant directory structure:

```
src/
  DrumBurp.py          # entry point
  Data/                # data models (Score, Measure, Drum, etc.)
  GUI/                 # main window, dialogs, graphics scene
  Widgets/             # custom widgets (ScoreView, measureTabs)
  Notation/            # ASCII and Lilypond export
  test/                # unit test suite
  buttons.qrc          # QRC resources (button icons and note heads)
  buttons_rc.py        # generated by pyrcc5 from buttons.qrc
build/                 # packaging scripts
.github/workflows/     # GitHub Actions CI
```

Main dependencies (see `requirements-debian12.txt`):

- Python 3.11+
- PyQt5 5.15.x — package `python3-pyqt5`
- pyqt5-dev-tools — package `pyqt5-dev-tools` (includes `pyuic5` and `pyrcc5`)
  Install: `sudo apt install pyqt5-dev-tools`
- python3-pyqt5.qtmultimedia — for MIDI
- lilypond 2.24.x — for score export (optional)

---

## Overall status — MIGRATION COMPLETE

The migration from PyQt4 to PyQt5 is complete. The program:

- [x] Starts without errors or tracebacks
- [x] Opens and edits `.brp` files
- [x] Plays back MIDI
- [x] Exports to PDF via LilyPond 2.24
- [x] Exports ASCII
- [x] Prints
- [x] 373 unit tests pass

---

## Migration strategy

- [x] 1. Keep `src/PyQt4` temporarily while fixing runtime errors.
- [x] 2. Migrate directly to `PyQt5` (no intermediate `GUI/QtCompat.py` layer).
- [x] 3. Regenerate `ui_*.py` files with `pyuic5`.
- [x] 4. Regenerate `*_rc.py` files with `pyrcc5`.
- [x] 5. Migrate manual code in groups: startup, dialogs, score/graphics,
         preferences, MIDI, export.
- [x] 6. Remove the temporary `src/PyQt4/` layer entirely.
- [x] 7. Verify that `grep -R PyQt4` returns no results in source code.

---

## General PyQt4 -> PyQt5 changes

Quick reference for any editor picking up this work:

- [x] `PyQt4.QtGui` split into `PyQt5.QtWidgets`, `PyQt5.QtGui` and `PyQt5.QtPrintSupport`.
- [x] `QApplication`, `QDialog`, `QWidget`, layouts, menus, actions, message boxes,
      `QGraphicsView`, `QGraphicsScene`, `QGraphicsItem`, `QUndoStack`,
      `QUndoCommand` → `QtWidgets`.
- [x] `QFont`, `QFontMetrics`, `QPixmap`, `QIcon`, `QColor`, `QPen`, `QTransform`,
      `QTextCursor` → `QtGui`.
- [x] `QPrinter`, `QPrinterInfo`, `QPrintPreviewDialog` → `QtPrintSupport`.
- [x] `QVariant` removed: Python values are used directly.
- [x] `.toInt()`, `.toBool()`, `.toString()`, `.toStringList()` replaced by
      Python conversions or `QSettings.value(..., type=...)`.
      Note: the `hasattr(value, "toString")` guards remaining in `_settingsValue`
      are defensive code for reading settings saved with PyQt4 — not a problem.
- [x] `QDesktopServices.storageLocation()` → `QStandardPaths.writableLocation()`.
- [x] `QtCore.SIGNAL(...)` / `QtCore.QObject.connect(...)` → `obj.signal.connect(slot)`.
- [x] `@pyqtSignature(...)` removed and replaced with `@pyqtSlot(...)`.
- [x] `QApplication.UnicodeUTF8` and `QtCore.QString.fromUtf8` removed.
- [x] `QLayout.setMargin()` → `setContentsMargins(...)`.
- [x] `QGraphicsItem.setAcceptsHoverEvents()` → `setAcceptHoverEvents()`.
- [x] `QGraphicsItemGroup` → `QGraphicsItem` with `setParentItem` (in `QStaff`).
- [x] `QFontMetrics.width(text)` → `horizontalAdvance(text)`.
- [x] `exec_()` → `exec()` in all dialogs and the main event loop.

---

## Python 2 -> Python 3 changes

- [x] `NotePosition.__cmp__`/`cmp()` → `__eq__`/`__lt__`/`__le__`/`__gt__`/`__ge__`/`__hash__`
      (`src/Data/NotePosition.py`).
- [x] `MeasureCount.counterMaker`: division `/` → `//` to avoid float
      (`src/Data/MeasureCount.py`).
- [x] `MeasureCount.iterMidiTicks`/`iterTimesMs`: `swing` argument made optional
      with default `0` (`src/Data/MeasureCount.py`).
- [x] `Drum.checkShortcuts`: `set.pop()` → `min()` for deterministic ordering
      (`src/Data/Drum.py`).
- [x] `fileUtils.Base64StringField`: Python 2 codec `str.encode('base64')` →
      Python 3 `base64` module (`src/Data/fileUtils.py`).
- [x] `dbfsv0.startBarlineString`/`endBarlineString`: fixed bitmask logic
      for `NO_BAR` (value 0 always passed `& 0 == 0`) (`src/Data/fileStructures/dbfsv0.py`).
- [x] `DBMidi.py`: integer division fixed in MIDI calculations:
      - `midiVolume / FLAM_VOLUME_CONSTANT` → `//` (MIDI volume must be integer)
      - `MIDITICKSPERBEAT / FLAM_TIME_CONSTANT` → `//` (ticks must be integers)
      - `divisionTicks / 2` → `//` (tick offset must be integer)
- [x] `Notation/lilypond.py`: integer division fixed in duration calculations:
      - `note / 2` and `restNote / 2` in tick comparisons → `//`
      - `headCount / 26` in name generation → `//` (argument to `chr()`)

---

## Files generated by pyuic4 → regenerated with pyuic5

Command: `pyuic5 file.ui -o ui_file.py`  
Status: all completed.

- [x] `src/GUI/ui_DBComplextCountDialog.py`
- [x] `src/GUI/ui_alternateRepeatWidget.py`
- [x] `src/GUI/ui_alternateRepeats.py`
- [x] `src/GUI/ui_asciiDialog.py`
- [x] `src/GUI/ui_dbColours.py`
- [x] `src/GUI/ui_dbInfo.py`
- [x] `src/GUI/ui_dbLicense.py`
- [x] `src/GUI/ui_dbStartup.py`
- [x] `src/GUI/ui_defaultKitManager.py`
- [x] `src/GUI/ui_drumburp.py`
- [x] `src/GUI/ui_editKit.py`
- [x] `src/GUI/ui_insertMeasuresDialog.py`
- [x] `src/GUI/ui_measurePropertiesDialog.py`
- [x] `src/GUI/ui_newScoreDialog.py`
- [x] `src/GUI/ui_repeatCountDialog.py`
- [x] `src/GUI/ui_scorePropertiesDialog.py`
- [x] `src/GUI/ui_versionDownloader.py`
- [x] `src/Widgets/ui_measureTabs.py`

Changes applied to each file:

- [x] Imports changed to `from PyQt5 import QtCore, QtGui, QtWidgets`.
- [x] Widget classes `QtGui.QWidget`, `QtGui.QLabel`, etc. → `QtWidgets.*`.
- [x] `QtCore.QString.fromUtf8` removed.
- [x] `QApplication.UnicodeUTF8` and 4-argument translate calls replaced.
- [x] `QtCore.QObject.connect(... SIGNAL(...))` → `.connect`.
- [x] `layout.setMargin(n)` → `layout.setContentsMargins(n, n, n, n)`.
- [x] Imports of `DrumBurp_rc` and `buttons_rc` re-enabled with real PyQt5 resources.
- [x] Orphaned lines `QtGui.QPixmap = _CompatQPixmap` removed from all files.

---

## QRC resources → regenerated with pyrcc5

Required package: `pyqt5-dev-tools`  
Install: `sudo apt install pyqt5-dev-tools`

Commands:

```bash
pyrcc5 src/GUI/DrumBurp.qrc    -o src/GUI/DrumBurp_rc.py
pyrcc5 src/buttons.qrc         -o src/buttons_rc.py
pyrcc5 src/Widgets/buttons.qrc -o src/Widgets/buttons_rc.py
```

- [x] `src/GUI/DrumBurp_rc.py` — regenerated with pyrcc5 (icons and fonts).
- [x] `src/buttons_rc.py` — regenerated with pyrcc5 (buttons and note heads).
- [x] `src/Widgets/buttons_rc.py` — regenerated with pyrcc5.

Resource map by file:

| File | Resources used | Required import |
|------|---------------|-----------------|
| `ui_drumburp.py` | `:/Icons/`, `:/fonts/` | `import GUI.DrumBurp_rc` |
| `ui_dbInfo.py` | `:/Icons/` | `import GUI.DrumBurp_rc` |
| `ui_dbLicense.py` | `:/Icons/` | `import GUI.DrumBurp_rc` |
| `ui_alternateRepeatWidget.py` | `:/Icons/` | `import GUI.DrumBurp_rc` |
| `ui_editKit.py` | `:/Icons/`, `:/buttons/` | `import GUI.DrumBurp_rc` + `import buttons_rc` |
| `QNotationScene.py` | `:/heads/` | `import buttons_rc` |

Note: `GUI/QtResourceCompat.py` was the temporary mechanism while the `*_rc.py`
files were no-op stubs. It is no longer used and can be removed in a future cleanup.

---

## Temporary compatibility layer src/PyQt4

- [x] `.py` files in `src/PyQt4/` removed.
- [x] `src/PyQt4/` directory removed completely.
- [x] No file in `src/`, `build/`, `.github/` or `pylintrc` imports PyQt4.

---

## Application code — status by file

### `src/DrumBurp.py`
- [x] `QApplication` from `PyQt5.QtWidgets`. `app.exec()` modernised.

### `src/GUI/DBMainwindow.py`
- [x] Widgets → `QtWidgets`; `QFont` → `QtGui`; `QPrinter` → `QtPrintSupport`.
- [x] `QVariant` removed from settings, combos and colour saving.
- [x] `QDesktopServices.storageLocation` → `QStandardPaths`.
- [x] `QFileDialog` adapted (PyQt5 returns a tuple).
- [x] `currentIndexChanged` signals connected to the `int` overload.
- [x] No-op `pyqtSignature` decorator removed; `pyqtSlot` imported.
- [x] All 35 `@pyqtSignature` → `@pyqtSlot` with correct signature.
- [x] 3 `@staticmethod` slots converted to regular instance methods.
- [x] `exec_()` → `exec()`.

### `src/GUI/QScore.py`
- [x] `QGraphicsScene`, `QGraphicsItem`, `QMessageBox`, `QUndoStack` → `QtWidgets`.
- [x] `exec_()` → `exec()`.

### `src/GUI/QStaff.py`
- [x] Inherits from `QGraphicsItem` (not `QGraphicsItemGroup`).
- [x] `setFiltersChildEvents(False)` instead of `setHandlesChildEvents(False)`.

### `src/GUI/QMeasure.py`
- [x] `setAcceptHoverEvents`; `horizontalAdvance`; integer division fixed.

### `src/GUI/QMeasureLine.py`
- [x] `QGraphicsItem` → `QtWidgets`; `QPen` in `QtGui`.

### `src/GUI/QLineLabel.py`
- [x] `setAcceptHoverEvents`.

### `src/GUI/QGraphicsListData.py`
- [x] `setAcceptHoverEvents`; `horizontalAdvance`.

### `src/GUI/QSection.py`
- [x] `QGraphicsTextItem` in `QtWidgets`; `QTextCursor` in `QtGui`.

### `src/GUI/QNotationScene.py`
- [x] `QGraphicsScene` → `QtWidgets`; `QPixmap` from `PyQt5.QtGui`.
- [x] `import buttons_rc` re-enabled with real PyQt5 resource.

### `src/GUI/QEditKitDialog.py`
- [x] `QVariant`, `toInt`, `setTextColor` fixed; `QStandardPaths`.
- [x] `exec_()` → `exec()`.

### `src/GUI/QComplexCountDialog.py`
- [x] `QVariant` removed; `pyqtSignature` → `pyqtSlot`.

### `src/GUI/QNewScoreDialog.py`
- [x] `QVariant` removed; settings protected against old PyQt4 values.

### `src/GUI/QDefaultKitManager.py`
- [x] `QVariant` removed; `pyqtSignature` → `pyqtSlot`.
- [x] `exec_()` → `exec()`.

### `src/GUI/DBColourPicker.py`
- [x] Widgets → `QtWidgets`; `QColor`, `QPen` → `QtGui`.
- [x] `exec_()` → `exec()`.

### `src/GUI/DBMidi.py`
- [x] `QThread`, `QObject`, `QTimer`, `pyqtSignal` in `QtCore`.
- [x] Integer division fixed in MIDI volume and tick calculations (`/` → `//`).

### `src/GUI/LilypondExporter.py`
- [x] `QThread` → `QtCore`; UTF-8 writing fixed for Python 3.

### `src/GUI/QLilypondPreview.py`
- [x] `QMessageBox`, `QGraphicsScene` → `QtWidgets`; `QTimeLine` in `QtCore`.

### `src/GUI/DBCommands.py`
- [x] `QUndoCommand` → `QtWidgets`.

### `src/GUI/DBFonts.py`
- [x] `QFontDatabase`, `QFont` → `QtGui`.

### `src/GUI/DBIcons.py`
- [x] `QIcon`, `QPixmap` → `QtGui`.

### `src/GUI/DBInfoDialog.py`
- [x] "Technologies" section updated: Python 3 + PyQt5 (previously said Python 2.7 + PyQt 4.8).
- [x] "PyQt4 → PyQt5 Port" section added with credit to the porter.
- [x] `exec_()` → `exec()`.

### Simple dialogs — all completed
- [x] `src/GUI/DBLicense.py`
- [x] `src/GUI/DBStartupDialog.py`
- [x] `src/GUI/QAlternateDialog.py` — `exec_()` → `exec()`.
- [x] `src/GUI/QAlternateWidget.py`
- [x] `src/GUI/QEditMeasureDialog.py`
- [x] `src/GUI/QInsertMeasuresDialog.py`
- [x] `src/GUI/QMenuIgnoreCancelClick.py`
- [x] `src/GUI/QMetaDataDialog.py` — `exec_()` → `exec()`.
- [x] `src/GUI/QRepeatCountDialog.py`
- [x] `src/GUI/QVersionDownloader.py`

### Context menus
- [x] `src/GUI/DBFSM.py`
- [x] `src/GUI/QMeasureContextMenu.py` — `exec_()` → `exec()`.

### Properties / display
- [x] `src/GUI/QDisplayProperties.py`

---

## Custom widgets

### `src/Widgets/ScoreView.py`
- [x] `QGraphicsView` → `QtWidgets`; `QTimeLine`, `QMutex`, `pyqtSlot`, `pyqtSignal` in `QtCore`.

### `src/Widgets/measureTabs.py`
- [x] `QWidget` → `QtWidgets`; `pyqtSignal` in `QtCore`.
- [x] `exec_()` → `exec()`.

### Qt Designer plugins
- [x] `src/Widgets/ScoreView_plugin.py` — migrated to `PyQt5.QtDesigner`.
- [x] `src/Widgets/measureTabs_plugin.py` — migrated to `PyQt5.QtDesigner`.

---

## Lilypond export — compatibility with LilyPond 2.24

- [x] Header version updated from `2.18.2` to `2.24.0`.
- [x] Percussion articulators in `dbdrums` table: `"open"`/`"stopped"` (quoted
      strings, invalid in LilyPond 2.22+) → `open`/`stopped` (Scheme symbols).
- [x] Integer division in tuplet calculation: `/` → `//`.
- [x] `note / 2` and `restNote / 2` in tick comparisons → `//`.
- [x] `headCount / 26` in instrument name generation → `//`.
- [x] PDF export verified with LilyPond 2.24.1: generates PDF without errors.

---

## Build, CI and configuration

- [x] `build/build_linux.sh` — hidden imports changed to PyQt5 modules.
- [x] `build/install_pyqt.ps1` — no longer downloads PyQt4 installers.
- [x] `.github/workflows/build.yml` — Linux and Windows CI updated to PyQt5/Python 3.
- [x] `pylintrc` — `extension-pkg-whitelist` changed from `PyQt4` to `PyQt5`.

---

## Python 3 test suite — all fixed

Command: `PYTHONPATH=src python3 -m unittest discover -s src/test`  
Result: **373 tests, all OK**

- [x] `testNotePosition.py` — `__cmp__`/`cmp()` → Python 3 comparison methods.
- [x] `testMeasureCount.py` — integer division; `swing` made optional.
- [x] `testCounter.py` — `testIter` updated to 23 counters.
- [x] `testScore.py` — `range(...)` → `list(range(...))` in asserts.
- [x] `testLilypond.py` — `\times 2/3` → `\tuplet 3/2`; integer division.
- [x] `testdbfsv0.py` — `NO_BAR` bitmask logic; BARLINE flag order.
- [x] `testdbfsv1.py` — `Base64StringField` migrated to Python 3 `base64` module.
- [x] `testDrum.py` — `checkShortcuts` uses `min()` for deterministic ordering.
- [x] `testAsciiExport.py` — passes after fixing `counterMaker`.

---

## Final verification

All of these commands should run without errors or warnings:

```bash
# No results = no PyQt4 imports
grep -R "from PyQt4\|import PyQt4" -n src build .github pylintrc --exclude-dir=__pycache__

# No errors = everything compiles
python3 -m py_compile $(find src -name '*.py' -not -path '*/__pycache__/*')

# 373 tests OK
PYTHONPATH=src python3 -m unittest discover -s src/test

# App starts without traceback
./run-drumburp.sh
```

---

## Minor pending items (do not block usage)

- [ ] Remove `src/GUI/QtResourceCompat.py` — no longer used, dead code.
- [ ] Extended manual testing: kit editing, MIDI export, printing on physical
      paper, opening `.brp` files from older versions.

---

## Maintenance commands

If `.ui` or `.qrc` files are modified, regenerate with:

```bash
# Regenerate UI
pyuic5 src/GUI/file.ui -o src/GUI/ui_file.py
# Then restore the corresponding _rc import according to the resource map above.

# Regenerate resources
pyrcc5 src/GUI/DrumBurp.qrc    -o src/GUI/DrumBurp_rc.py
pyrcc5 src/buttons.qrc         -o src/buttons_rc.py
pyrcc5 src/Widgets/buttons.qrc -o src/Widgets/buttons_rc.py
```
