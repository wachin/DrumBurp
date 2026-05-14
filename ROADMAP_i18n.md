# Internationalization (i18n) Roadmap — DrumBurp

**Goal:** Full Qt Linguist support for all user-visible strings, starting with
English (reference) and Spanish, with a clean path to add more languages.

**Approach:** Phased — infrastructure first, then the heaviest files, then the
long tail of smaller dialogs, then translation, then runtime polish.

**Total strings extracted so far:** 612 (across 24 translation contexts)  
**Languages planned:** English (built-in), Spanish (`es`)

---

## Phase 0 — Infrastructure

- [x] Create `src/i18n/` directory
- [x] Create `src/i18n/i18n.py` — translation loader (`QTranslator` + `installTranslator`)
- [x] Add `--language` CLI option to `src/DrumBurp.py`
- [x] Add `LANGUAGE` environment variable support to `i18n.py`
- [x] Install translator in `DrumBurp.py` before any UI is created
- [x] Create `drumburp.pro` — Qt project file for `pylupdate5`
- [x] Run `pylupdate5 drumburp.pro` — generates `drumburp_en.ts` and `drumburp_es.ts`
- [x] Verify `.ts` files contain all 612 strings from UI files and Python code
- [ ] Add `lrelease` step to build scripts (`build/build_linux.sh`, `build/build_windows.ps1`)
- [ ] Add `lrelease` step to GitHub Actions workflow (`.github/workflows/build.yml`)
- [ ] Add `src/i18n/*.qm` to PyInstaller hidden data in build scripts
- [ ] Write developer i18n section in `README.md` and `README_ES.md`

---

## Phase 1 — Wrap strings: heaviest files

These three files account for **444 of 612 strings (72%)**.

### `src/GUI/DBMainwindow.py` — 240 strings in context `DrumBurpWindow` + `DrumBurp`

- [x] Wrap `statusbar.showMessage(...)` calls with `self.tr()`
- [x] Wrap all `QMessageBox` titles and messages with `self.tr()`
- [x] Wrap `updateStatus(...)` string arguments with `self.tr()`
- [x] Wrap `QFileDialog` caption and filter strings with `self.tr()`
- [x] Wrap window title strings with `self.tr()`
- [x] Wrap undo/redo dynamic text with `self.tr()`
- [x] Wrap multi-line informational texts (update splash, backup dialog) with `self.tr()`
- [x] Wrap Lilypond path dialog text with `self.tr()`
- [ ] Wrap `checkLilypondPath()` full info message (currently partially done)
- [ ] Wrap MIDI error messages in `_midiInitFinished()` and related methods
- [ ] Wrap version check result messages
- [ ] Re-run `pylupdate5` after all wrapping is complete

### `src/GUI/QEditKitDialog.py` — 147 strings in context `editKitDialog`

- [x] Wrap `QMessageBox` strings: "Kit saved", "Successfully saved drumkit"
- [ ] Wrap remaining dialog labels set dynamically in Python code
- [ ] Wrap `QFileDialog` captions
- [ ] Wrap status/error messages in kit editing operations
- [ ] Re-run `pylupdate5` after wrapping

### `src/GUI/QScore.py` — 57 strings in context `DrumBurp`

- [x] Wrap "Score load error" / "Error loading DrumBurp file %s"
- [x] Wrap "Score save error" / "Error saving DrumBurp file: %s"
- [x] Wrap "Apply kit changes?" dialog
- [x] Wrap "Editing the kit cannot be undone. Proceed?"
- [ ] Audit remaining strings (section titles, measure labels set in Python)
- [ ] Re-run `pylupdate5` after wrapping

---

## Phase 2 — Wrap strings: medium dialogs

These files have 19–57 strings each.

### `src/GUI/QMeasureContextMenu.py` — 6 strings in context `QMeasureContextMenu`

- [x] Wrap "Really delete this staff?" / "Delete Staff?"
- [x] Wrap "Really delete this section?" / "Delete Section?"
- [x] Wrap "This will delete all empty trailing measures.\nContinue?" / "Delete Empty Measures"

### `src/GUI/QLilypondPreview.py` — 10 strings in context `QLilypondPreview`

- [x] Wrap all `QMessageBox` titles and messages
- [x] Wrap "Still previewing" / "Cannot preview now..."
- [x] Wrap "Build failed!" and all sub-messages

### `src/GUI/QDefaultKitManager.py` — 6 strings in context `QDefaultKitManager`

- [x] Wrap "Duplicate kit name!" / "That kit name already exists."
- [x] Wrap "Kit name" / "Enter a name for the new default kit"
- [x] Wrap "Default kit" / "Cannot overwrite default kits!"

### `src/GUI/DBStartupDialog.py` — 2 strings in context `dbStartup`

- [ ] Wrap `setWindowTitle("Welcome to DrumBurp v" + version)` with `self.tr()`

### `src/GUI/DBInfoDialog.py` — 10 strings in context `InfoDialog`

- [ ] Wrap port credit label text added dynamically in `_addPortCredit()`
- [ ] Wrap "PyQt4 → PyQt5 Port" section title

### `src/GUI/QNewScoreDialog.py` — 6 strings in context `newScoreDialog`

- [ ] Audit for any dynamically set strings not covered by the `.ui` file

### `src/GUI/QComplexCountDialog.py` — 14 strings in context `complexCountDialog`

- [ ] Audit for dynamically set strings

### `src/Widgets/measureTabs.py` — 15 strings in context `measureTabs`

- [ ] Audit for dynamically set strings not covered by the `.ui` file

---

## Phase 3 — Wrap strings: small dialogs (long tail)

Each of these has fewer than 10 strings. Most are fully covered by their `.ui`
files and need no Python wrapping — just audit to confirm.

| File | Context | Strings | Status |
|------|---------|---------|--------|
| `src/GUI/DBColourPicker.py` | `ColourPicker` | 6 | [ ] audit |
| `src/GUI/QAlternateDialog.py` | `AlternateDialog` | 4 | [ ] audit |
| `src/GUI/QAlternateWidget.py` | `AlternateWidget` | 6 | [ ] audit |
| `src/GUI/QInsertMeasuresDialog.py` | `InsertMeasuresDialog` | 9 | [ ] audit |
| `src/GUI/QRepeatCountDialog.py` | `repeatCountDialog` | 3 | [ ] audit |
| `src/GUI/QVersionDownloader.py` | `VersionDownloader` | 3 | [ ] audit |
| `src/GUI/DBLicense.py` | `dbLicense_dialog` | 3 | [ ] audit |
| `src/GUI/QEditMeasureDialog.py` | `measurePropertiesDialog` | 2 | [ ] audit |
| `src/GUI/QMetaDataDialog.py` | `ScoreDialog` | 19 | [ ] audit |

---

## Phase 4 — English translation file (`drumburp_en.ts`)

The English `.ts` file is the **reference** file. Its translations should be
identical to the source strings (or slightly improved for clarity). This is
what translators use as the base.

- [x] `drumburp_en.ts` generated by `pylupdate5`
- [ ] Open `drumburp_en.ts` in Qt Linguist
- [ ] Mark all 612 strings as "Accepted" (Ctrl+Enter on each, or use
      Edit → Translation → Mark All as Accepted)
- [ ] Save and run `lrelease src/i18n/drumburp_en.ts -qm src/i18n/drumburp_en.qm`
- [ ] Verify `drumburp_en.qm` loads correctly with `--language en`

---

## Phase 5 — Spanish translation (`drumburp_es.ts`)

Work through the 612 strings in order of user impact.

### 5a — Core UI (highest visibility, ~240 strings)

Context: `DrumBurpWindow` — the main window toolbar, menus, panels.

- [ ] Translate all menu names: File, Edit, Score, View, MIDI, Help
- [ ] Translate all menu items: New, Open, Save, Save As, Print, Export...
- [ ] Translate all toolbar tooltips and status tips
- [ ] Translate all panel labels: Score Properties, Actions, Lilypond Output...
- [ ] Translate all WhatsThis help texts

### 5b — Dialogs (medium visibility, ~200 strings)

Contexts: `editKitDialog`, `newScoreDialog`, `ScoreDialog`, `DefaulKitManager`,
`complexCountDialog`, `measureTabs`, `asciiDialog`, `InsertMeasuresDialog`.

- [ ] `editKitDialog` — 147 strings (kit editor: drum names, MIDI settings, note heads)
- [ ] `newScoreDialog` — 6 strings (new score wizard)
- [ ] `ScoreDialog` — 19 strings (score properties: title, artist, BPM, swing)
- [ ] `DefaulKitManager` — 17 strings (default kit manager)
- [ ] `complexCountDialog` — 14 strings (complex beat count editor)
- [ ] `measureTabs` — 15 strings (measure count tabs widget)
- [ ] `asciiDialog` — 19 strings (ASCII export options)
- [ ] `InsertMeasuresDialog` — 9 strings (insert measures dialog)

### 5c — Messages and small dialogs (~170 strings)

Contexts: `DrumBurp`, `QLilypondPreview`, `QMeasureContextMenu`,
`QDefaultKitManager`, `QScore`, `QEditKitDialog`, `InfoDialog`,
`AlternateDialog`, `AlternateWidget`, `ColourPicker`, `repeatCountDialog`,
`VersionDownloader`, `dbLicense_dialog`, `dbStartup`, `measurePropertiesDialog`.

- [ ] All `QMessageBox` titles and messages (errors, warnings, confirmations)
- [ ] All `QFileDialog` captions and filters
- [ ] Status bar messages
- [ ] Window titles set dynamically

### 5d — Compile and test

- [ ] Run `lrelease src/i18n/drumburp_es.ts -qm src/i18n/drumburp_es.qm`
- [ ] Test with `LANGUAGE=es ./run-drumburp.sh`
- [ ] Test with `./run-drumburp.sh --language es`
- [ ] Verify all menus, dialogs and messages appear in Spanish
- [ ] Fix any missing or broken strings, re-run `pylupdate5` + `lrelease`

---

## Phase 6 — Runtime language switching (optional, future)

- [ ] Add language selector to Preferences dialog
- [ ] Save selected language to `QSettings`
- [ ] Load language from `QSettings` on startup (before `install_translator`)
- [ ] Allow switching language without restarting (requires `retranslateUi()` calls)

---

## Phase 7 — Additional languages (future)

To add a new language (e.g. French `fr`):

1. Add `src/i18n/drumburp_fr.ts` to `drumburp.pro` under `TRANSLATIONS`
2. Run `pylupdate5 drumburp.pro` — creates the new `.ts` file
3. Open `src/i18n/drumburp_fr.ts` in Qt Linguist and translate
4. Run `lrelease src/i18n/drumburp_fr.ts -qm src/i18n/drumburp_fr.qm`
5. Test with `LANGUAGE=fr ./run-drumburp.sh`

Candidate languages: French (`fr`), German (`de`), Portuguese (`pt`),
Italian (`it`), Japanese (`ja`).

---

## Quick reference — key commands

```bash
# Extract/update strings from source code into .ts files
pylupdate5 drumburp.pro

# Compile a .ts file into a binary .qm file
lrelease src/i18n/drumburp_en.ts -qm src/i18n/drumburp_en.qm
lrelease src/i18n/drumburp_es.ts -qm src/i18n/drumburp_es.qm

# Open Qt Linguist GUI to translate
linguist src/i18n/drumburp_es.ts

# Test the program in Spanish
LANGUAGE=es ./run-drumburp.sh
./run-drumburp.sh --language es

# Test in English explicitly
./run-drumburp.sh --language en

# Count untranslated strings remaining
grep -c 'type="unfinished"' src/i18n/drumburp_es.ts
```

---

## File map

```
drumburp.pro                  Qt project file — lists all source and .ui files
                              for pylupdate5

src/i18n/
  i18n.py                     Translation loader — call install_translator(app)
  drumburp_en.ts              English reference .ts (source of truth)
  drumburp_es.ts              Spanish .ts (work in progress)
  drumburp_en.qm              Compiled English binary (generated by lrelease)
  drumburp_es.qm              Compiled Spanish binary (generated by lrelease)
```

---

## Progress summary

| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Infrastructure (loader, .pro file, .ts generation) | 🟡 Mostly done — build integration pending |
| 1 | Wrap strings: DBMainwindow, QEditKitDialog, QScore | 🟡 Partially done |
| 2 | Wrap strings: medium dialogs | 🟡 Partially done |
| 3 | Wrap strings: small dialogs (audit) | ⬜ Not started |
| 4 | English .ts — mark all as accepted | ⬜ Not started |
| 5 | Spanish translation (612 strings) | ⬜ Not started |
| 6 | Runtime language switching | ⬜ Future |
| 7 | Additional languages | ⬜ Future |
